from django.urls import path

from . import views
app_name = "code_converter"
urlpatterns = [
    path("", views.index, name="index"),
    path("convert_code", views.convert_code, name="convert_code"),
    path("auto-test", views.auto_test, name="auto_test"),
    path("auto-project", views.auto_project, name="auto_project"),
]