# task_assignment/urls.py
from django.urls import path
from .views import TaskAssignmentListCreate, TaskAssignmentRetrieveUpdateDestroy

urlpatterns = [
    path('', TaskAssignmentListCreate.as_view()),
    path('<int:pk>/', TaskAssignmentRetrieveUpdateDestroy.as_view()),
]