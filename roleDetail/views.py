from django.shortcuts import render
from django.http import JsonResponse
from roleDetail.serializers import RoleDetailSerializer
from roleDetail.models import RoleDetail

def roleDetail_list(request):
  roleDetails = RoleDetail.objects.all()
  serializer = RoleDetailSerializer(roleDetails, many = True)
  return JsonResponse({
    'data' : serializer.data
  })

# Create your views here.
from rest_framework import generics
from .models import RoleDetail
from .serializers import RoleDetailSerializer

class RoleDetailListCreate(generics.ListCreateAPIView):
    queryset = RoleDetail.objects.all()
    serializer_class = RoleDetailSerializer

class RoleDetailRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoleDetail.objects.all()
    serializer_class = RoleDetailSerializer

class RoleDetailByRoleIdList(generics.ListAPIView):
    serializer_class = RoleDetailSerializer

    def get_queryset(self):
        role_id = self.kwargs.get('roleId')  # Lấy roleId từ URL
        return RoleDetail.objects.filter(roleId=role_id)
