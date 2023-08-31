import random

from django.contrib.auth import login

from rest_framework import permissions, status
from rest_framework.views import APIView
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

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from rental_mobil.my_libraries import CustomResponse
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
        return CustomResponse.success(
            message='User list retrive successful.',
            data=serializer.data,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message='User retrive successful.',
            data=serializer.data,
        )

    def partial_update(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message='User update successful.',
                data=serializer.data,
            )
        else:
            return CustomResponse.error(
                message='User update failed.',
                error=serializer.errors,
            )


# AUTH
class RegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = RegistrationModelSerializer(data=request.data)
        if serializer.is_valid():

            name = serializer.data.get('full_name').split()[0]
            email = serializer.data.get('email')
            otp_code = random.randrange(100000,999999)
            template = render_to_string('otp.html', {'name': name, 'otp_code': otp_code})

            email = EmailMessage(
                'Email Verification',
                template,
                settings.EMAIL_HOST_USER,
                [email,],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)


            user = serializer.save()
            user_serializer = UserModelSerializer(user)
            return CustomResponse.success(
                message='Registration successful.',
                data=user_serializer.data,
            )
        else:
            return CustomResponse.error(
                message='Registration failed.',
                error=serializer.errors,
            )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            login(request, user)

            res = super(LoginView, self).post(request, format=None)

            return CustomResponse.success(
                message='Login successful.',
                data=res.data,
            )
        else:
            print(serializer.errors)
            return CustomResponse.error(
                message='Login failed.',
                error=serializer.errors,
            )
    

class LogoutView(KnoxLogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = (permissions.IsAuthenticated,)
    

