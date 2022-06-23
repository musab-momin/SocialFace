from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from . import views



app_name = 'chatapp'
urlpatterns = [
    path('', views.chat_home, name='ChatHome'),
]