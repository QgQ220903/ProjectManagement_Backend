# task_assignment/views.py
from rest_framework import generics
from .models import TaskAssignment
from .serializers import TaskAssignmentSerializer  # Chỉ import TaskAssignmentSerializer

class TaskAssignmentListCreate(generics.ListCreateAPIView):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer

class TaskAssignmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskAssignment.objects.all()
    serializer_class = TaskAssignmentSerializer