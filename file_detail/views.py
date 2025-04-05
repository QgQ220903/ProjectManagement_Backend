from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import FileDetail
from .serializers import FileDetailSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_file_detail_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "file_detail_updates",
        {
            "type": "send_update",
            "message": data
        }
    )
class FileDetailViewSet(viewsets.ModelViewSet):
    queryset = FileDetail.objects.all()
    serializer_class = FileDetailSerializer

    def perform_create(self, serializer):
        file_detail = serializer.save()
        send_file_detail_update({
            "action": "create",
            "file_detail": FileDetailSerializer(file_detail).data
        })

    def perform_update(self, serializer):
        file_detail = serializer.save()
        send_file_detail_update({
            "action": "update",
            "file_detail": FileDetailSerializer(file_detail).data
        })

    def perform_destroy(self, instance):
        file_detail_id = instance.id
        instance.delete()
        send_file_detail_update({
            "action": "delete",
            "file_detail_id": file_detail_id
        })

