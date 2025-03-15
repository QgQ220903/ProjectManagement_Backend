from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import LoginSerializer, UserSerializer

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

@api_view(['GET'])
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})
