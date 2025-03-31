from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Role
from .serializers import RoleSerializer,RoleCreateUpdateSerializer

class RoleListCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RoleSerializer  # Trả về đầy đủ thông tin
        return RoleCreateUpdateSerializer
    

class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RoleCreateUpdateSerializer  # Không yêu cầu role_details khi cập nhật
        return RoleSerializer