# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet  # Chỉ import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')  # Chỉ register TaskViewSet

urlpatterns = [
    path('', include(router.urls)),
]