from django.urls import path
from . import views

app_name = "game"
urlpatterns = [
    path('', views.index, name='index'),
    path('create-game', views.create_game, name='create_game'),
    path('sub/<int:main_pk>', views.sub_user_choice, name='sub_user_choice'),
    path('socket-test', views.socket_test, name='socket_test'),
    path('ajax/send-choice', views.send_choice, name='send_choice'),
    path('api/get-main', views.get_main, name='get_main'),
]