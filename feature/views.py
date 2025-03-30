from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Feature
from .serializers import FeatureSerializer

class FeatureListCreate(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer