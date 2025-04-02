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
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/projects/', include('project.urls')), # Thêm URL của app projects
    path('api/project-parts/', include('project_part.urls')), # Thêm URL của app project_parts
    path('api/tasks/', include('task.urls')),
    path('api/departments/', include('department.urls')),
    path('api/employees/', include('employee.urls')),
    path('api/task-assignments/', include('task_assignment.urls')),  # Include các URL của ứng dụng task_assignment]
    path('api/department-tasks/', include('task_department.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account/', include('account.urls')),
    path('api/roles/', include('role.urls')),
    path('api/features/', include('feature.urls')),
    path('api/role-details/', include('role_detail.urls')),
    path('api/work-histories/', include('work_history.urls')),
    path('api/files/', include('file.urls')),
    path('api/file-details/', include('file_detail.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)