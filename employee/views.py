from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination

# class EmployeePagination(PageNumberPagination):
#     page_size = 5  # Số lượng phần tử trên mỗi trang

class EmployeeListCreate(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # pagination_class = EmployeePagination  # Thêm dòng này

class EmployeeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer