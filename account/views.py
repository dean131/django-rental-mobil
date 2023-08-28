from django.contrib.auth import login
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import (
    LoginView as KnoxLoginView, 
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView,
)

from .serializers import (
    CustomUserModelSerializer,
    RegistrationModelSerializer
)

from rental_mobil.utils import custom_response
from .models import User


# USER LIST 
class UserModelViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserModelSerializer


# AUTH
class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RegistrationModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=1,
                message='Registration successful.',
                data=serializer.data,
                status_code=status.HTTP_201_CREATED,
            )
        else:
            return custom_response(
                success=0,
                message='Registration failed.',
                error=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        response = {}
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            login(request, user)

            res = super(LoginView, self).post(request, format=None)

            return custom_response(
                success=1,
                message='Login successful.',
                data=res.data,
                status_code=status.HTTP_200_OK,
            )
        else:
            print(serializer.errors)
            return custom_response(
                success=0,
                message='Login failed.',
                error='Invalid username or password.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    

class LogoutView(KnoxLogoutView):
    permission_classes = (permissions.AllowAny,)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = (permissions.AllowAny,)
    

