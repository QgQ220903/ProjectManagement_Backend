# project/views.py
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectDetailSerializer

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response(serializer.data)