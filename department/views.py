from rest_framework import viewsets, status  # Import các lớp generics và mã trạng thái HTTP
from rest_framework.response import Response  # Import lớp Response để trả về dữ liệu API
from .models import Department  # Import model Department từ models.py của ứng dụng hiện tại
from .serializers import DepartmentSerializer, DepartmentCreateUpdateSerializer  # Import các serializer cho model Department
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action



class DepartmentPagination(PageNumberPagination):
    page_size = 5  # Số lượng phần tử trên mỗi trang

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet để xử lý CRUD phòng ban.
    """
    queryset = Department.objects.filter(is_deleted=False).order_by('id')
    pagination_class = DepartmentPagination  

    def get_serializer_class(self):
        """
        Xác định serializer được sử dụng dựa trên phương thức request.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentCreateUpdateSerializer
        return DepartmentSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Xử lý yêu cầu xóa phòng ban (DELETE).
        Thay vì xóa khỏi database, cập nhật trường is_deleted thành True.
        """
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_all_departments(self, request):
        """
        API lấy tất cả phòng ban (không phân trang).
        """
        departments = Department.objects.filter(is_deleted=False)
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
