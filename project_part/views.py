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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
def send_project_part_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(  # Sử dụng async_to_sync để gọi trong môi trường không đồng bộ
        "project_part_updates",
        {
            "type": "send_update",
            "message": data
        }
    )
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

    def perform_create(self, serializer):
        department = self.request.data.get('department')  # Lấy phòng ban từ dữ liệu yêu cầu (nếu có)
        
        if department:
            try:
                department_instance = Department.objects.get(id=department)
                serializer.save(department=department_instance)  # Lưu phần dự án với phòng ban
            except Department.DoesNotExist:
                raise serializers.ValidationError("Phòng ban không tồn tại.")
        else:
            serializer.save()
        
        # Gửi cập nhật WebSocket
        send_project_part_update({"action": "create", "project_part": ProjectPartSerializer(serializer.instance).data})

    def perform_update(self, serializer):
        department = self.request.data.get('department')
        
        if department:
            try:
                department_instance = Department.objects.get(id=department)
                serializer.save(department=department_instance)
            except Department.DoesNotExist:
                raise serializers.ValidationError("Phòng ban không tồn tại.")
        else:
            serializer.save()
        
        # Gửi cập nhật WebSocket
        send_project_part_update({"action": "update", "project_part": ProjectPartSerializer(serializer.instance).data})

    def perform_destroy(self, instance):
        instance.delete()
        
        # Gửi cập nhật WebSocket
        send_project_part_update({"action": "delete", "project_part_id": instance.id})

    
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


    @action(detail=False, methods=['get'], url_path='with-archived-tasks/(?P<department_id>\d+)')
    def with_archived_tasks(self, request, department_id=None):
        """
        Lấy danh sách các phần dự án theo ID phòng ban (is_deleted=False)
        nhưng chỉ lấy các task đã xóa (is_deleted=True) bên trong
        URL: /api/project-parts/with-archived-tasks/<department_id>/
        """
        try:
            # Kiểm tra department có tồn tại không
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response(
                {"error": "Department không tồn tại"},
                status=status.HTTP_404_NOT_FOUND
            )

        project_parts = self.queryset.filter(
            department_id=department_id
        ).prefetch_related('tasks')
        
        # Phân trang
        page = self.paginate_queryset(project_parts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Chỉ lấy archived_tasks, không lấy tasks thông thường
            data = [{
                **item,
                'tasks': item['archived_tasks'],  # Thay tasks bằng archived_tasks
                'archived_tasks': None  # Ẩn trường archived_tasks
            } for item in serializer.data]
            return self.get_paginated_response(data)
        
        serializer = self.get_serializer(project_parts, many=True)
        # Chỉ lấy archived_tasks, không lấy tasks thông thường
        data = [{
            **item,
            'tasks': item['archived_tasks'],  # Thay tasks bằng archived_tasks
            'archived_tasks': None  # Ẩn trường archived_tasks
        } for item in serializer.data]
        return Response(data, status=status.HTTP_200_OK)


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context