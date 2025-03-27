from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer
from account.permissions import DynamicPermission

class EmployeeListCreate(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [DynamicPermission]  # Áp dụng kiểm tra quyền
    # feature_name = "Quản lý nhân viên"

class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer