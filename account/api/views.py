import random

from django.contrib.auth import login
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
    UserModelSerializer,
    RegistrationModelSerializer
)

from rental_mobil.my_libraries import CustomResponse
from ..models import User, OTPCode
from rental_mobil.my_libraries import EmailSender


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
        otp_code = random.randint(100000,999999)
        email = request.data.get('email')
        name = request.data.get('full_name')
        if name:
            name = name.split()[0]

        try:
            user = User.objects.get(email=email, is_active=False)
            serializer = UserModelSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

            otp_obj = get_object_or_404(OTPCode, user=user)
            otp_obj.code = otp_code
            otp_obj.save()
            EmailSender.otp_email(email=email, otp_code=otp_code, name=name)
            return CustomResponse.success(message=f'OTP code has been sent to {email}. Please check your email.')
        except:
            print(f'request.data = {request.data}')
            serializer = RegistrationModelSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                OTPCode.objects.create(user=user, code=otp_code)
                EmailSender.otp_email(email=email, otp_code=otp_code, name=name)
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


class OTPConfirmAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        otp_code = request.data.get('otp_code')
        email = request.data.get('email')

        otp_obj = get_object_or_404(OTPCode, code=otp_code, user__email=email)

        if otp_obj.expire > timezone.now():
            user = otp_obj.user 
            user.is_active = True
            user.save()
            return CustomResponse.success(message='OTP code is still Valid')
            
        return CustomResponse.error(message='OTP Code has expired')
    

