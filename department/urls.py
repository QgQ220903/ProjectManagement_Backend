from django.urls import path
from .views import DepartmentListCreate, DepartmentRetrieveUpdateDestroy

urlpatterns = [
    path('', DepartmentListCreate.as_view()),
    path('<int:pk>/', DepartmentRetrieveUpdateDestroy.as_view()),
]