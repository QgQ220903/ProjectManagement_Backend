from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import RoleDetail
from .serializers import RoleDetailSerializer

class RoleDetailViewSet(viewsets.ModelViewSet):
    queryset = RoleDetail.objects.all()
    serializer_class = RoleDetailSerializer