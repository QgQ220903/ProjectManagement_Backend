from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Department
from .serializers import EmployeeSerializer

@api_view(['GET'])
def get_employee(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_employee(request):
    department_id = request.data.get("departmentID")  # Sử dụng departmentID

    if not department_id:
        return Response({"error": "DepartmentID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Kiểm tra xem departmentID có tồn tại không
    if not Department.objects.filter(pk=department_id).exists():
        return Response({"error": f"Department with ID {department_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        department_id = request.data.get("departmentID")  # Đổi thành departmentID

        if not department_id:
            return Response({"error": "DepartmentID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra departmentID có tồn tại không
        if not Department.objects.filter(pk=department_id).exists():
            return Response({"error": f"Department with ID {department_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
