from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from project.serializers import ProjectSerializer, ProjectPartSerializer
from project.models import Project, ProjectPart
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def project_list(request):
  projects = Project.objects.all()
  serializer = ProjectSerializer(projects, many = True)
  return Response(serializer.data)

@api_view(['GET'])
def project_detail(request, pk):
  project = get_object_or_404(Project, pk = pk)
  serializer = ProjectSerializer(project)
  return Response(serializer.data)


@api_view(['POST'])
def project_create(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    serializer = ProjectSerializer(project, data=request.data, partial=True if request.method == 'PATCH' else False) #partial allows for patch requests
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def project_part_list(request):
    project_parts = ProjectPart.objects.all()
    serializer = ProjectPartSerializer(project_parts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def project_part_detail(request, pk):
    project_part = get_object_or_404(ProjectPart, pk=pk)
    serializer = ProjectPartSerializer(project_part)
    return Response(serializer.data)

@api_view(['POST'])
def project_part_create(request):
    serializer = ProjectPartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def project_part_update(request, pk):
    project_part = get_object_or_404(ProjectPart, pk=pk)
    serializer = ProjectPartSerializer(project_part, data=request.data, partial=True if request.method == 'PATCH' else False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def project_part_delete(request, pk):
    project_part = get_object_or_404(ProjectPart, pk=pk)
    project_part.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
