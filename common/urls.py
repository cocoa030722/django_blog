from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from blog_app import views as blog_app_views
    
app_name = "common"
urlpatterns = [
    path("", blog_app_views.PostListView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),

    path("logout/", views.logout_view, name="logout"), 
    path("signup/", views.signup, name="signup"), 
    path("monitor/", views.resource_monitor, name="resource_monitor"), 
    
]