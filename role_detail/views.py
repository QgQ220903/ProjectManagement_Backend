from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import RoleDetail
from .serializers import RoleDetailSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def send_role_detail_update(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "role_detail_updates",
        {
            "type": "send_role_detail_update",
            "message": message
        }
    )
class RoleDetailViewSet(viewsets.ModelViewSet):
    queryset = RoleDetail.objects.all()
    serializer_class = RoleDetailSerializer
    
    def perform_create(self, serializer):
        role_detail = serializer.save()
        send_role_detail_update({
            "action": "create",
            "role_detail": RoleDetailSerializer(role_detail).data
        })

    def perform_update(self, serializer):
        role_detail = serializer.save()
        send_role_detail_update({
            "action": "update",
            "role_detail": RoleDetailSerializer(role_detail).data
        })

    def perform_destroy(self, instance):
        instance.delete()
        send_role_detail_update({
            "action": "delete",
            "role_detail_id": instance.id
        })