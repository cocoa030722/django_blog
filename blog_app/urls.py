from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
app_name = "blog_app"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),

    path("read_post/<int:id>", views.post_detail, name="read_post"),
    path("create_post", views.create_post, name="create_post"),
    path("update_post/<slug:slug>", views.edit_post, name="update_post"),
    path("delete_post/<int:id>", views.delete_post, name="delete_post"),
]