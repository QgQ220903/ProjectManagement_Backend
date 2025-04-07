from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
from .serializers import AccountSerializer,LoginSerializer,LogoutSerializer,UpdateSerializer

from rest_framework.pagination import PageNumberPagination

class AccountPagination(PageNumberPagination):
    page_size = 5
class AccountViewSet(viewsets.ModelViewSet):
    
    queryset = Account.objects.all().order_by('id')
    serializer_class = AccountSerializer
    pagination_class = AccountPagination

    @action(detail=False, methods=['get'])
    def get_all_acount(self, request):
        accounts = self.get_queryset()
        serializer = self.get_serializer(accounts, many=True)
        return Response({
            'count': accounts.count(),
            'results': serializer.data
        })
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """API Đăng ký người dùng với quyền"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": AccountSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], serializer_class=LoginSerializer)
    def login(self, request):
        """API Đăng nhập bằng email và trả về JWT"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Kiểm tra tài khoản theo email
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"error": "Email không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra mật khẩu
        if not user.check_password(password):
            return Response({"error": "Mật khẩu không đúng"}, status=status.HTTP_400_BAD_REQUEST)

        # Xác thực thành công
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": AccountSerializer(user).data
        }, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], serializer_class=LogoutSerializer)
    def logout(self, request):
        """API Logout bằng cách đưa Refresh Token vào blacklist"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data['refresh']  # Lấy refresh token từ serializer
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['put'], permission_classes=[AllowAny],serializer_class=UpdateSerializer)
    def update_account(self, request, pk=None):
        """Cập nhật password hoặc role"""
        account = self.get_object()
        serializer = UpdateSerializer(account, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật thành công", "user": AccountSerializer(account).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """API Lấy thông tin user hiện tại"""
        return Response(AccountSerializer(request.user).data)

