from django.shortcuts import render
from django.http import JsonResponse
from role.serializers import RoleSerializer
from role.models import Role

def role_list(request):
  roles = Role.objects.all()
  serializer = RoleSerializer(roles, many = True)
  return JsonResponse({
    'data' : serializer.data
  })

# Create your views here.
from rest_framework import generics
from .models import Role
from .serializers import RoleSerializer

class RoleListCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
# Create your views here.
