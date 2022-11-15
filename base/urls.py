from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('questions/', questions, name="questions"),
    path('answer/<str:pk>/', answer, name='answer'),
    path('ask/', ask, name='ask'),
    path('post/', post, name='post'),
    path('notifications/', notifications, name='notifications'),
    path('profile/<str:pk>/', profile, name='profile'),
    path('follow/<str:pk>/', follow, name='follow'),
    path('unfollow/<str:pk>/', unfollow, name='unfollow'),
    path('following/', followPosts, name='following'),
    path('edit/', editProfile, name='edit'),

    path('login/', loginPage, name="login"),
    path('logout/', logoutPage, name='logout'),
    path('register/', registerPage, name="register"),
]
