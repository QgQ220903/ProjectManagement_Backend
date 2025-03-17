from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import LoginSerializer, UserSerializer,RegisterSerializer,ChangePasswordSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)  # Dùng session-based login
        response = Response({"message": "Đăng nhập thành công", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)
        response["X-CSRFToken"] = get_token(request)  # Trả về CSRF Token
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])  # Cho phép truy cập không cần đăng nhập
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])  # Hash mật khẩu
        user.save()

        return Response({
            "message": "Đăng ký thành công",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Chỉ cho phép user đã đăng nhập
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
    
    if serializer.is_valid():
        serializer.update_password()
        return Response({"message": "Mật khẩu đã được thay đổi thành công."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)