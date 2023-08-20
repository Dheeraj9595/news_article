"""__________________________Project urls.py__________________________________"""
from django.contrib import admin
from django.urls import path,include
from newsapp import views  # Import the views from newsapp
import app1.views as app1_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.headlines, name='headlines'),
    path('fetch-news/', views.fetch_news, name='fetch-news'),
    path('sources/', views.sources, name='sources'),
    path('signup/', app1_views.SignupPage, name='signup'),
    path('login/', app1_views.LoginPage, name='login'),
    path('logout/', app1_views.LogoutPage, name='logout'),
    path('home2/', views.home2, name='home2'),
]
