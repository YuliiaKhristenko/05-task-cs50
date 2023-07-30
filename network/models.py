from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authorUser")
    textarea = models.TextField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    
    def __str__(self):
        return f"{self.id}: {self.author} {self.textarea} {self.timestamp}"
    
class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    who = models.ManyToManyField(User, blank=True, related_name="myFollowers")    
    
    def __str__(self):
        listofwho = []
        for unit in self.who.all():
            listofwho.append(unit.username)
        return f"{self.user} followers: {listofwho}"
    
class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    who = models.ManyToManyField(User, blank=True, related_name="myFollowing")   
    
    def __str__(self):
        listofwho = []
        for unit in self.who.all():
            listofwho.append(unit.username)
        return f"{self.user} following: {listofwho}"
     
