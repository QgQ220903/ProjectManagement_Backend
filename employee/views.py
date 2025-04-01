from django.shortcuts import render

# Create your views here.
from rest_framework import status,viewsets
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination
from account.permissions import DynamicPermission
from rest_framework.decorators import action
class EmployeePagination(PageNumberPagination):
    page_size = 5  # Số lượng phần tử trên mỗi trang

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer
    pagination_class = EmployeePagination  # Thêm dòng này
    # permission_classes = [DynamicPermission]  # Áp dụng kiểm tra quyền
    # feature_name = "Quản lý nhân viên"
    @action(detail=False, methods=['get'])
    def get_all_employees(self, request):
        """Lấy tất cả nhân viên mà không phân trang"""
        employees = Employee.objects.all()
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get_by_department/(?P<department_id>[^/.]+)')
    def get_by_department(self, request, department_id=None):
        """Lấy danh sách nhân viên theo ID phòng ban từ đường dẫn"""
        employees = Employee.objects.filter(department_id=department_id)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer