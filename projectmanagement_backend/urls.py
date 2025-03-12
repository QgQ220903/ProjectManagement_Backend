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
from django.urls import path
from project import views
from role import views as role_views
from feature import views as feature_views
from roleDetail import views as roleDetail_views

urlpatterns = [
   path('projects/', views.ProjectListCreate.as_view(), name='project-list-create'),
   path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroy.as_view(), name='project-retrieve-update-destroy'),
   path('roles/', role_views.RoleListCreate.as_view(), name='role-list-create'),
   path('roles/<int:pk>/', role_views.RoleRetrieveUpdateDestroy.as_view(), name='role-retrieve-update-destroy'),
   path('features/', feature_views.FeatureListCreate.as_view(), name='feature-list-create'),
   path('features/<int:pk>/', feature_views.FeatureRetrieveUpdateDestroy.as_view(), name='feature-retrieve-update-destroy'),
   path('role-detail/', roleDetail_views.RoleDetailListCreate.as_view(), name='role-detail-list-create'),
   path('role-detail/<int:pk>/', roleDetail_views.RoleDetailRetrieveUpdateDestroy.as_view(), name='role-detail-retrieve-update-destroy'),
   path('role-detail/by-role/<int:roleId>/', roleDetail_views.RoleDetailByRoleIdList.as_view(), name='role-detail-by-role'),
]
