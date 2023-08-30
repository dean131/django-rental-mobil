from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import (
    LoginView as KnoxLoginView, 
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView,
)

from .serializers import (
    UserModelSerializer,
    RegistrationModelSerializer
)

from rental_mobil.my_libraries import custom_response
from ..models import User


# USER LIST 
class UserModelViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ## Default built in
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return custom_response(
            success=1,
            message='User list retrive successful.',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return custom_response(
            success=1,
            message='User retrive successful.',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=1,
                message='User update successful.',
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        else:
            return custom_response(
                success=0,
                message='User update failed.',
                error=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


# AUTH
class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RegistrationModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserModelSerializer(user)
            return custom_response(
                success=1,
                message='Registration successful.',
                data=user_serializer.data,
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
                error=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    

class LogoutView(KnoxLogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = (permissions.IsAuthenticated,)
    

