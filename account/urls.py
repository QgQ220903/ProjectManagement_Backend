from django.urls import path
from .views import login_view, logout_view, get_csrf_token,register_view,change_password_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='logout'),
    path('change-password/', change_password_view, name='change_password'),
    path('csrf/', get_csrf_token, name='csrf_token'),
]
