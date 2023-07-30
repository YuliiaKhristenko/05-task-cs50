import json
# from pickle import FALSE, NONE
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import math

from .models import User, Post, Followers, Following
from .forms import PostForm

N = 5


def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                addinfo = form.save(commit=False)
                addinfo.author = request.user
                addinfo.save()
        else:
            return render(request, "network/login.html")
        
    posts = Post.objects.all().order_by('-timestamp')
    followingUserList = []
    if request.user.is_authenticated:
        followings = Following.objects.filter(user = request.user)
        if followings:
            for extractList in followings:
                for unit in extractList.who.all():
                    followingUserList.append(unit.username)
                    
    forrange = math.ceil(len(posts)/N)+1
    paginator = Paginator(posts, N)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "form": PostForm(),
        "range": range(1, forrange),
        "followings": followingUserList,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        if not username:
            return render(request, "network/register.html", {
                "message": "Username must be filled!"
            })

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def profile(request, name):
    otherUser = User.objects.get(username=name)
    myOwn = request.user
    statusFollow = False
    
    followers = Followers.objects.filter(user=otherUser)
    if followers:
        for extractList in followers:
            lenFollowList = len(extractList.who.all())
            for unit in extractList.who.all():
                if unit == myOwn:
                    statusFollow = True
                    break
    else:
        lenFollowList = 0
        
    followings = Following.objects.filter(user=otherUser)
    if followings:
        for extractList in followings:
            lenFollowingList = len(extractList.who.all())
    else:
        lenFollowingList = 0
    
    posts = Post.objects.filter(author=otherUser).order_by('-timestamp')
    forrange = math.ceil(len(posts)/N)+1
    paginator = Paginator(posts, N)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "page_obj": page_obj,
        "range": range(1, forrange),
        "guest": name,
        "statusFollow": statusFollow,
        "followersCount": lenFollowList,
        "followingCount": lenFollowingList
    })
    
@login_required
def following(request):
    followings = Following.objects.filter(user = request.user)
    followingUserList = []
    if followings:
        postList = []
        for extractList in followings:
            for unit in extractList.who.all():
                tempPost = Post.objects.filter(author=unit)
                if tempPost:
                    postList.append(tempPost)
                    followingUserList.append(unit.username)
        if len(postList) > 0:
            posts = postList[0]
            for unit in postList:
                if unit != unit[0]:
                    posts = posts|unit
            posts = posts.order_by('-timestamp')
        else:
            posts = []
    else:
        posts = []
        
    forrange = math.ceil(len(posts)/N)+1
    paginator = Paginator(posts, N)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "range": range(1, forrange),
        "followings": followingUserList
    })
    
@login_required
def subscribe(request, author):
    author = User.objects.get(username=author)
    followings = Following.objects.filter(user=request.user)
    if followings:
        for extractList in followings:
            if author in extractList.who.all():
                deleteFrom(followings, author)
            else:
                saveInfo(followings, author)
    else:
        mark = 'Following'
        saveNew(mark, author, request.user)
        
    followers = Followers.objects.filter(user=author)
    if followers:
        for extractList in followers:
            if request.user in extractList.who.all():
                deleteFrom(followers, request.user)
            else:
                saveInfo(followers, request.user)
    else:
        mark = 'Followers'
        saveNew(mark, author, request.user)
    return HttpResponse(status=204)

# API func

@login_required
def like(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == "PUT":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
        else:
            post.likes.add(request.user)
            post.save()
        return HttpResponse(status=204)
 
@login_required   
def editpost(request, post_id):
    post = Post.objects.get(id = post_id)
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body", "")
        post.textarea = body
        if len(post.textarea) == 0:
            post.delete()
        else:
            post.save()
        return HttpResponse(status=204)
        
# Tech func

def saveInfo(where, who):
    for extractList in where:
        extractList.who.add(who)
        extractList.save()
        
def saveNew(mark, toWho, who):
    if mark == 'Followers':
        newUserTo = Followers.objects.create(user=toWho)
        newUserTo.who.add(who)
    else:
        newUserTo = Following.objects.create(user=who)
        newUserTo.who.add(toWho)
    newUserTo.save()
    
def deleteFrom(where, who):
    for extractList in where:
        extractList.who.remove(who)
        if len(extractList.who.all()) > 0:
            extractList.save()
        else:
            where.delete()
