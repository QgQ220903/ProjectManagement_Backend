from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import ProjectPart
from .serializers import ProjectPartSerializer
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

class ProjectPartPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectPartViewSet(viewsets.ModelViewSet):
    queryset = ProjectPart.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProjectPartSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    pagination_class = ProjectPartPagination

@api_view(['GET'])
def projectpart_list(request):
    queryset = ProjectPart.objects.filter(is_deleted=False).order_by('-created_at')
    serializer = ProjectPartSerializer(queryset, many=True)
    return Response(serializer.data)