# task_department/views.py
from rest_framework import viewsets
from .models import DepartmentTask
from .serializers import DepartmentTaskSerializer, DepartmentTaskCreateUpdateSerializer
from rest_framework.pagination import PageNumberPagination

class DepartmentTaskPagination(PageNumberPagination):
    page_size = 10  # Số lượng mục trên mỗi trang
    page_size_query_param = 'page_size'
    max_page_size = 100

class DepartmentTaskViewSet(viewsets.ModelViewSet):
    queryset = DepartmentTask.objects.filter(is_deleted=False)
    pagination_class = DepartmentTaskPagination  # Thêm lớp phân trang

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentTaskCreateUpdateSerializer
        return DepartmentTaskSerializer