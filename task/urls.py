# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('', views.task_list),
]