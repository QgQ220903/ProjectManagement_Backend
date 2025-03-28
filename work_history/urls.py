# work_history/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkHistoryViewSet

router = DefaultRouter()
router.register(r'', WorkHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]