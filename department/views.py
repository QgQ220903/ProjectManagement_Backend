from rest_framework import generics, status  # Import các lớp generics và mã trạng thái HTTP
from rest_framework.response import Response  # Import lớp Response để trả về dữ liệu API
from .models import Department  # Import model Department từ models.py của ứng dụng hiện tại
from .serializers import DepartmentSerializer, DepartmentCreateUpdateSerializer  # Import các serializer cho model Department

class DepartmentListCreate(generics.ListCreateAPIView):
    """
    View để xử lý danh sách phòng ban (GET) và tạo phòng ban mới (POST).
    """
    queryset = Department.objects.filter(is_deleted=False)  # Chỉ lấy các Department có is_deleted là False
    def get_serializer_class(self):
        """
        Xác định serializer được sử dụng dựa trên phương thức request.
        Sử dụng DepartmentCreateUpdateSerializer cho POST (tạo mới) và DepartmentSerializer cho GET (lấy danh sách).
        """
        if self.request.method == 'POST':
            return DepartmentCreateUpdateSerializer
        return DepartmentSerializer

class DepartmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    View để xử lý chi tiết phòng ban (GET), cập nhật phòng ban (PUT, PATCH) và xóa phòng ban (DELETE).
    """
    queryset = Department.objects.filter(is_deleted=False)  # Chỉ lấy các Department có is_deleted là False
    def get_serializer_class(self):
        """
        Xác định serializer được sử dụng dựa trên phương thức request.
        Sử dụng DepartmentCreateUpdateSerializer cho PUT/PATCH (cập nhật) và DepartmentSerializer cho GET (lấy chi tiết).
        """
        if self.request.method in ['PUT', 'PATCH']:
            return DepartmentCreateUpdateSerializer
        return DepartmentSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Xử lý yêu cầu xóa phòng ban (DELETE).
        Thay vì xóa phòng ban khỏi database, cập nhật trường is_deleted thành True.
        """
        instance = self.get_object()  # Lấy đối tượng Department cần xóa
        instance.is_deleted = True  # Đặt is_deleted thành True
        instance.save()  # Lưu lại đối tượng với is_deleted đã cập nhật
        return Response(status=status.HTTP_204_NO_CONTENT)  # Trả về response 204 No Content (xóa thành công)