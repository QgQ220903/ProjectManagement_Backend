from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SendEmailViewSet

router = DefaultRouter()
router.register(r'', SendEmailViewSet, basename='email')

urlpatterns = [
    path('', include(router.urls)),
]
