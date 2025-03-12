from django.shortcuts import render
from django.http import JsonResponse
from feature.serializers import FeatureSerializer
from feature.models import Feature

def feature_list(request):
  features = Feature.objects.all()
  serializer = FeatureSerializer(features, many = True)
  return JsonResponse({
    'data' : serializer.data
  })

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
# Create your views here.
