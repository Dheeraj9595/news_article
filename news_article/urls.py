"""__________________________Project urls.py__________________________________"""
from django.contrib import admin
from django.urls import path,include
from newsapp import views  # Import the views from newsapp
import app1.views as app1_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.headlines, name='headlines'),
    path('fetch-news/', views.fetch_news, name='fetch-news'),
    path('sources/', views.sources, name='sources'),
    path('signup/', app1_views.SignupPage, name='signup'),
    path('login/', app1_views.LoginPage, name='login'),
    path('logout/', app1_views.LogoutPage, name='logout'),
    path('home2/', views.home2, name='home2'),
    path('profile/', app1_views.user_profile, name='profile'),
    path('profile/edit/', app1_views.edit_user_profile, name='edit_user_profile'),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)