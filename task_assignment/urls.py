from django.urls import path  # Import hàm path để định nghĩa URL pattern
from .views import TaskAssignmentListCreate, TaskAssignmentRetrieveUpdateDestroy  # Import các view đã tạo

urlpatterns = [
    path('', TaskAssignmentListCreate.as_view()),  # Định nghĩa URL cho danh sách và tạo mới TaskAssignment
    path('<int:pk>/', TaskAssignmentRetrieveUpdateDestroy.as_view()),  # Định nghĩa URL cho chi tiết, cập nhật và xóa TaskAssignment
]