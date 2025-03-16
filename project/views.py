# projects/views.py
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination # Import phân trang
from .models import Project
from .serializers import ProjectSerializer
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

class ProjectPagination(PageNumberPagination):
    page_size = 10  # Số lượng item trên mỗi trang (có thể ghi đè giá trị trong settings)
    page_size_query_param = 'page_size'  # Cho phép client tùy chỉnh số lượng item trên mỗi trang
    max_page_size = 100 # Giới hạn số lượng item tối đa trên mỗi trang

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False).order_by('-created_at') # Lọc các project chưa bị xóa và sắp xếp theo ngày tạo mới nhất
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] # Thêm bộ lọc tìm kiếm và sắp xếp
    search_fields = ['name'] # Cho phép tìm kiếm theo tên
    ordering_fields = ['name', 'created_at', 'updated_at'] # Cho phép sắp xếp theo các trường này

@api_view(['GET'])
def project_list(request):
    queryset = Project.objects.filter(is_deleted=False).order_by('-created_at')
    serializer = ProjectSerializer(queryset, many=True)
    return Response(serializer.data)