from rest_framework import generics, status  # Import các lớp generics và mã trạng thái HTTP
from rest_framework.response import Response  # Import lớp Response để trả về dữ liệu API
from .models import TaskAssignment  # Import model TaskAssignment từ models.py của ứng dụng hiện tại
from .serializers import TaskAssignmentSerializer, TaskAssignmentCreateUpdateSerializer  # Import các serializer cho model TaskAssignment

class TaskAssignmentListCreate(generics.ListCreateAPIView):
    """
    View để xử lý danh sách TaskAssignment (GET) và tạo TaskAssignment mới (POST).
    """
    queryset = TaskAssignment.objects.filter(is_deleted=False)  # Lấy tất cả các đối tượng TaskAssignment có is_deleted là False từ database

    def get_serializer_class(self):
        """
        Xác định serializer được sử dụng dựa trên phương thức request.
        Sử dụng TaskAssignmentCreateUpdateSerializer cho POST (tạo mới) và TaskAssignmentSerializer cho GET (lấy danh sách).
        """
        if self.request.method == 'POST':
            return TaskAssignmentCreateUpdateSerializer
        return TaskAssignmentSerializer

class TaskAssignmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    View để xử lý chi tiết TaskAssignment (GET), cập nhật TaskAssignment (PUT, PATCH) và xóa TaskAssignment (DELETE).
    """
    queryset = TaskAssignment.objects.filter(is_deleted=False)  # Lấy tất cả các đối tượng TaskAssignment có is_deleted là False từ database

    def get_serializer_class(self):
        """
        Xác định serializer được sử dụng dựa trên phương thức request.
        Sử dụng TaskAssignmentCreateUpdateSerializer cho PUT/PATCH (cập nhật) và TaskAssignmentSerializer cho GET (lấy chi tiết).
        """
        if self.request.method in ['PUT', 'PATCH']:
            return TaskAssignmentCreateUpdateSerializer
        return TaskAssignmentSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Xử lý yêu cầu xóa TaskAssignment (DELETE).
        Thay vì xóa TaskAssignment khỏi database, cập nhật trường is_deleted thành True.
        """
        instance = self.get_object()  # Lấy đối tượng TaskAssignment cần xóa
        instance.is_deleted = True  # Đặt is_deleted thành True
        instance.save()  # Lưu lại đối tượng với is_deleted đã cập nhật
        return Response(status=status.HTTP_204_NO_CONTENT)  # Trả về response 204 No Content (xóa thành công)