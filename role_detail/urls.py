from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleDetailViewSet

router = DefaultRouter()
router.register(r'', RoleDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
