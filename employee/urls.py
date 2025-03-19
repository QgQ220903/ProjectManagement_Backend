from django.urls import path
from .views import EmployeeListCreate, EmployeeRetrieveUpdateDestroy

urlpatterns = [
    path('', EmployeeListCreate.as_view()),
    path('<int:pk>/', EmployeeRetrieveUpdateDestroy.as_view()),
]