from django.urls import path
from .views import get_employee,create_employee, employee_detail

urlpatterns = [
    path('employees/',get_employee,name='get_employee'),
    path('employees/create/',create_employee,name='create_employee'),
    path('employees/<int:pk>',employee_detail,name='employee_detail')
]