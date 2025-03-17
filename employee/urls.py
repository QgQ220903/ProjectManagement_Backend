from django.urls import path
from .views import EmployeeListCreate, EmployeeRetrieveUpdateDestroy

urlpatterns = [
    path('employees/', EmployeeListCreate.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroy.as_view(), name='employee-detail'),
]
