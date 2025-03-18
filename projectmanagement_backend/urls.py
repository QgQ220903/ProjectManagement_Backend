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
from django.urls import path, include
from project import views
from role import views as role_views
from feature import views as feature_views
from roleDetail import views as roleDetail_views
from account import views as account_views
urlpatterns = [
   path('api/projects/', include('project.urls')), # Thêm URL của app projects
   path('api/project-parts/', include('project_part.urls')), # Thêm URL của app project_parts
   path('api/tasks/', include('task.urls')),
   path('roles/', role_views.RoleListCreate.as_view(), name='role-list-create'),
   path('roles/<int:pk>/', role_views.RoleRetrieveUpdateDestroy.as_view(), name='role-retrieve-update-destroy'),
   path('features/', feature_views.FeatureListCreate.as_view(), name='feature-list-create'),
   path('features/<int:pk>/', feature_views.FeatureRetrieveUpdateDestroy.as_view(), name='feature-retrieve-update-destroy'),
   path('role-detail/', roleDetail_views.RoleDetailListCreate.as_view(), name='role-detail-list-create'),
   path('role-detail/<int:pk>/', roleDetail_views.RoleDetailRetrieveUpdateDestroy.as_view(), name='role-detail-retrieve-update-destroy'),
   path('role-detail/by-role/<int:roleId>/', roleDetail_views.RoleDetailByRoleIdList.as_view(), name='role-detail-by-role'),
   path('api/', include('account.urls')),
   path('api/', include('department.urls')),
   path('api/', include('employee.urls'))
]
