from django.shortcuts import render

# Create your views here.
from rest_framework import status,viewsets
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination
from account.permissions import DynamicPermission
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_employee_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "employee_updates",
        {
            "type": "send_update",
            "message": data
        }
    )
class EmployeePagination(PageNumberPagination):
    page_size = 5 # Số lượng item mỗi trang
    page_size_query_param = 'page_size'  # Cho phép client tuỳ chỉnh số lượng item/trang
    max_page_size = 100  # Giới hạn tối đa item/tran

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().filter(is_deleted=False).order_by('id')
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination  # Thêm dòng này
    # permission_classes = [DynamicPermission]  # Áp dụng kiểm tra quyền
    # feature_name = "Quản lý nhân viên"

    def perform_create(self, serializer):
        employee = serializer.save()
        send_employee_update({"action": "create", "employee": EmployeeSerializer(employee).data})

    def perform_update(self, serializer):
        employee = serializer.save()
        send_employee_update({"action": "update", "employee": EmployeeSerializer(employee).data})

    def perform_destroy(self, instance):
        instance.delete()
        send_employee_update({"action": "delete", "employee_id": instance.id})
        
    @action(detail=False, methods=['get'])
    def get_all_employees(self, request):
        """Lấy tất cả nhân viên mà không phân trang"""
        employees = Employee.objects.all().filter(is_deleted=False).order_by('id')
        serializer = self.get_serializer(employees, many=True)
        return Response({
            "count": employees.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get_by_department/(?P<department_id>[^/.]+)')
    def get_by_department(self, request, department_id=None):
        """Lấy danh sách nhân viên theo ID phòng ban từ đường dẫn"""
        employees = Employee.objects.filter(department_id=department_id, is_deleted=False)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer