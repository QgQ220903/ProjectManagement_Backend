# tasks/views.py
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.filter(is_deleted=False).order_by('-created_at')
#     serializer_class = TaskSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name', 'description']
#     ordering_fields = ['name', 'priority', 'start_time', 'end_time', 'completion_percentage', 'created_at', 'updated_at']
#     pagination_class = TaskPagination

# tasks/views.py
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

@api_view(['GET'])
def task_list(request):
    queryset = Task.objects.filter(parent_task__isnull=True, is_deleted=False).order_by('-created_at')
    serializer = TaskSerializer(queryset, many=True)
    return Response(serializer.data)