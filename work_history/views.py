# work_history/views.py
from rest_framework import viewsets
from .models import WorkHistory
from .serializers import WorkHistorySerializer, WorkHistoryCreateSerializer

class WorkHistoryViewSet(viewsets.ModelViewSet):
    queryset = WorkHistory.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WorkHistoryCreateSerializer
        return WorkHistorySerializer