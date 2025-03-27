# project_part/serializers.py
from rest_framework import serializers

from .models import RoleDetail
from feature.serializers import FeatureSerializer
class RoleDetailSerializer(serializers.ModelSerializer):
    feature = FeatureSerializer()
    class Meta:
        model = RoleDetail
        fields = '__all__'