from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import FileDetail
from .serializers import FileDetailSerializer
# Create your views here.
class FileDetailViewSet(viewsets.ModelViewSet):
    queryset = FileDetail.objects.all()
    serializer_class = FileDetailSerializer
