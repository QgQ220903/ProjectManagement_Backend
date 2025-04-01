# project_part/views.py
from rest_framework.decorators import action
from rest_framework import viewsets, filters,status
from rest_framework.pagination import PageNumberPagination
from .models import ProjectPart
from department.models import Department
from rest_framework import serializers
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
    search_fields = ['name', 'department__manager__id']
    ordering_fields = ['name', 'created_at', 'updated_at']
    pagination_class = ProjectPartPagination

    @action(detail=False, methods=['get'])
    def by_manager(self, request):
        """
        API endpoint để tìm kiếm các phần dự án theo ID của manager trong department
        """
        manager_id = request.query_params.get('manager_id')
        
        if not manager_id:
            return Response(
                {"error": "Vui lòng cung cấp manager_id"}, 
                status=400
            )
            
        try:
            # Lọc các phần dự án theo manager_id trong department
            project_parts = self.queryset.filter(
                department__manager_id=manager_id,
                department__isnull=False  # Chỉ lấy các phần dự án có department
            )
            
            # Phân trang kết quả
            page = self.paginate_queryset(project_parts)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                
            serializer = self.get_serializer(project_parts, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": f"Lỗi khi tìm kiếm: {str(e)}"}, 
                status=500
            )

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
    
    @action(detail=False, methods=['get'], url_path='by_department/(?P<department_id>\d+)')
    def by_department(self, request, department_id=None):
        """
        Lấy danh sách các phần dự án theo ID phòng ban.
        """
        project_parts = self.queryset.filter(department_id=department_id)
        # page = self.paginate_queryset(project_parts)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(project_parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
