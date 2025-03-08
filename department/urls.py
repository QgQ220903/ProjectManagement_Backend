from django.urls import path
from .views import get_department,create_department, department_detail

urlpatterns = [
    path('departments/',get_department,name='get_department'),
    path('departments/create/',create_department,name='create_department'),
    path('departments/<int:pk>',department_detail,name='department_detail')
]