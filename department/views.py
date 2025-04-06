from rest_framework import viewsets, status  # Import các lớp generics và mã trạng thái HTTP
from rest_framework.response import Response  # Import lớp Response để trả về dữ liệu API
from .models import Department  # Import model Department từ models.py của ứng dụng hiện tại
from .serializers import DepartmentSerializer, DepartmentCreateUpdateSerializer  # Import các serializer cho model Department
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
def send_department_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "department_updates",
        {"type": "send_update", "message": data}
    )

class DepartmentPagination(PageNumberPagination):
    page_size = 10  # Số lượng phần tử trên mỗi trang

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_deleted=False).order_by('id')
    pagination_class = DepartmentPagination  

    
    def get_serializer_class(self):

        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentCreateUpdateSerializer
        return DepartmentSerializer
    def perform_create(self, serializer):
        department = serializer.save()
        send_department_update({"action": "create", "department": DepartmentSerializer(department).data})

    def perform_update(self, serializer):
        department = serializer.save()
        send_department_update({"action": "update", "department": DepartmentSerializer(department).data})

    def perform_destroy(self, instance):
        instance.delete()
        send_department_update({"action": "delete", "department_id": instance.id})

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        send_department_update({"action": "delete", "department_id": instance.id})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_all_departments(self, request):

        departments = Department.objects.filter(is_deleted=False)
        serializer = DepartmentSerializer(departments, many=True)
        return Response({
            "count": departments.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)
