from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Project
from .serializers import ProjectDetailSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def broadcast_project_update():
    """Gửi sự kiện WebSocket khi có thay đổi dữ liệu"""
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "projects",
        {"type": "project_update"}
    )
class ProjectPagination(PageNumberPagination):
    page_size = 10  # Số lượng item mỗi trang
    page_size_query_param = 'page_size'  # Cho phép client tuỳ chỉnh số lượng item/trang
    max_page_size = 100  # Giới hạn tối đa item/trang

class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProjectDetailSerializer
    pagination_class = ProjectPagination  # Thêm phân trang vào ViewSet

    def perform_create(self, serializer):
        instance = serializer.save()
        broadcast_project_update()

    def perform_update(self, serializer):
        instance = serializer.save()
        broadcast_project_update()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        broadcast_project_update()
        
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response(serializer.data)