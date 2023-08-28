from django.contrib.auth import login
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import (
    LoginView as KnoxLoginView, 
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView,
)

from .serializers import (
    CustomUserSerializer,
    RegistrationSerializer
)

from .models import User


# USER LIST 
class UserModelViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


# AUTH
class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        response = {}
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            login(request, user)

            res = super(LoginView, self).post(request, format=None)

            response['status'] = 1
            response.update(res.data)
        else:
            response['status'] = 0
            response.update(serializer.errors)
        return Response(response)
    

class LogoutView(KnoxLogoutView):
    permission_classes = (permissions.AllowAny,)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = (permissions.AllowAny,)
    

