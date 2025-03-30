from rest_framework import permissions
from role.models import Role
from role_detail.models import RoleDetail
from feature.models import Feature

class DynamicPermission(permissions.BasePermission):
    """
    Kiểm tra quyền của user dựa trên chức năng (Feature).
    """

    def has_permission(self, request, view):
        """
        Kiểm tra xem user có quyền thực hiện hành động (view, create, update, delete) trên chức năng hiện tại không.
        """
        user = request.user

        # Nếu user chưa đăng nhập -> Không có quyền
        if not user.is_authenticated:
            return False

        # Lấy tên của view hiện tại (chính là chức năng cần kiểm tra)
        feature_name = getattr(view, "feature_name", None)
        if not feature_name:
            return False  # Nếu không có tên chức năng -> Không cấp quyền

        # Tìm chức năng trong bảng Feature
        try:
            feature = Feature.objects.get(name=feature_name)
        except Feature.DoesNotExist:
            return False  # Nếu chức năng chưa được định nghĩa -> Không cấp quyền

        # Kiểm tra quyền trong RoleDetail
        role_details = RoleDetail.objects.filter(role=user.role, feature=feature).first()

        if not role_details:
            return False  # Nếu user không có quyền với chức năng này -> Từ chối

        # Kiểm tra quyền dựa trên loại HTTP method (GET, POST, PUT, DELETE)
        if request.method == "GET":
            return role_details.can_view
        elif request.method == "POST":
            return role_details.can_create
        elif request.method in ["PUT", "PATCH"]:
            return role_details.can_update
        elif request.method == "DELETE":
            return role_details.can_delete

        return False  # Mặc định từ chối nếu không phù hợp
