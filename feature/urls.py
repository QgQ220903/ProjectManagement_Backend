from django.urls import path
from .views import FeatureListCreate, FeatureRetrieveUpdateDestroy

urlpatterns = [
    path('', FeatureListCreate.as_view()),
    path('<int:pk>/', FeatureRetrieveUpdateDestroy.as_view()),
]