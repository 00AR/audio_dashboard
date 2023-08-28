from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user_home", views.user_home, name="user_home")
]