from django.shortcuts import render
from django.http import JsonResponse
from project.serializers import ProjectSerializer
from project.models import Project

def project_list(request):
  projects = Project.objects.all()
  serializer = ProjectSerializer(projects, many = True)
  return JsonResponse({
    'data' : serializer.data
  })

# Create your views here.
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer

class ProjectListCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
