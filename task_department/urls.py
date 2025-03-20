# department_task/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentTaskViewSet

router = DefaultRouter()
router.register(r'', DepartmentTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]