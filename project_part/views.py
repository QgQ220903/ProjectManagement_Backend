# project_part/views.py
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import ProjectPart
from .serializers import ProjectPartSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

class ProjectPartPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectPartViewSet(viewsets.ModelViewSet):
    queryset = ProjectPart.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProjectPartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    pagination_class = ProjectPartPagination

    def perform_create(self, serializer):
        """
        Phương thức này được gọi khi bạn tạo mới phần dự án.
        Chúng ta sẽ đảm bảo rằng phần dự án mới được phân công phòng ban đúng đắn.
        """
        department = self.request.data.get('department')  # Lấy phòng ban từ dữ liệu yêu cầu (nếu có)
        
        if department:
            try:
                department_instance = Department.objects.get(id=department)  # Kiểm tra phòng ban có tồn tại không
                serializer.save(department=department_instance)  # Lưu phần dự án với phòng ban
            except Department.DoesNotExist:
                raise serializers.ValidationError("Phòng ban không tồn tại.")
        else:
            serializer.save()

    def perform_update(self, serializer):
        """
        Phương thức này được gọi khi bạn cập nhật phần dự án.
        """
        department = self.request.data.get('department')  # Lấy phòng ban từ dữ liệu yêu cầu (nếu có)
        
        if department:
            try:
                department_instance = Department.objects.get(id=department)  # Kiểm tra phòng ban có tồn tại không
                serializer.save(department=department_instance)  # Lưu phần dự án với phòng ban
            except Department.DoesNotExist:
                raise serializers.ValidationError("Phòng ban không tồn tại.")
        else:
            # Nếu không có phòng ban, chỉ update các trường còn lại mà không thay đổi phòng ban
            serializer.save()
