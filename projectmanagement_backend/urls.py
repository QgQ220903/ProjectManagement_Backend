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

urlpatterns = [
  path('api/projects/', views.project_list),
  path('api/projects/<int:pk>', views.project_detail),
  path('api/projects/create', views.project_create),
  path('api/projects/update/<int:pk>/', views.project_update),
  path('api/projects/delete/<int:pk>/', views.project_delete),
  path('api/project-parts/', views.project_part_list, name='project-part-list'),
  path('api/project-parts/<int:pk>/', views.project_part_detail, name='project-part-detail'),
  path('api/project-parts/create/', views.project_part_create, name='project-part-create'),
  path('api/project-parts/update/<int:pk>/', views.project_part_update, name='project-part-update'),
  path('api/project-parts/delete/<int:pk>/', views.project_part_delete, name='project-part-delete'),
]
