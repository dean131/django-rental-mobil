from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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


# AUTH
@api_view(['POST'])
def register_user(resquest):
    serializer = RegistrationSerializer(data=resquest.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        serializer.is_valid(raise_exception=True)
        data['id'] = user.id
        data['full_name'] = user.full_name
        data['email'] = user.email
    else:
        data = serializer.errors
    return Response(data)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
    

class LogoutView(KnoxLogoutView):
    permission_classes = (permissions.AllowAny,)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = (permissions.AllowAny,)
    

# USER LIST 
class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer