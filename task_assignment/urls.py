# task_assignment/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task_assignment.views import TaskAssignmentViewSet  # Import từ app riêng

router = DefaultRouter()
router.register(r'', TaskAssignmentViewSet, basename='task-assignment')

urlpatterns = [
    path('', include(router.urls)),
]