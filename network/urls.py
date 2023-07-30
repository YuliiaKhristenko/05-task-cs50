from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("subscribe/<str:author>", views.subscribe, name="subscribe"),
    path("editpost/<intpost_id>", views.editpost, name="editpost"),
]
