"""
URL configuration for projectmanagement_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path('api/projects/', include('project.urls')), # Thêm URL của app projects
    path('api/project-parts/', include('project_part.urls')), # Thêm URL của app project_parts
    path('api/tasks/', include('task.urls')),
    path('api/departments/', include('department.urls')),
    path('api/employees/', include('employee.urls')),
    path('api/task-assignments/', include('task_assignment.urls')),  # Include các URL của ứng dụng task_assignment]
]