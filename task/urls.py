# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet, TaskAssignmentViewSet  # Chỉ import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')  # Chỉ register TaskViewSet
router.register(r'task-assignments', TaskAssignmentViewSet, basename='task-assignment')
urlpatterns = [
    path('', include(router.urls)),
]