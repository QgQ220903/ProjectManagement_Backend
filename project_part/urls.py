# project_parts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectPartViewSet

router = DefaultRouter()
router.register(r'project_parts', ProjectPartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]