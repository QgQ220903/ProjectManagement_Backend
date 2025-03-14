# tasks/views.py
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'priority', 'start_time', 'end_time', 'completion_percentage', 'created_at', 'updated_at']
    pagination_class = TaskPagination