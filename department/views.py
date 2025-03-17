from rest_framework import generics
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
