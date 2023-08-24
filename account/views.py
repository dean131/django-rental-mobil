from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken

from .serializers import RegistrationSerializer


@api_view(['POST'])
def register_user(resquest):
    serializer = RegistrationSerializer(data=resquest.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        serializer.is_valid(raise_exception=True)
        _, token = AuthToken.objects.create(user=user)
        data['succes'] = 'Berhasil melakukan Registrasi'
        data['first_name'] = user.first_name
        data['email'] = user.email
        data['token'] = str(token)
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    _, token = AuthToken.objects.create(user=user)
    return Response({
        'user': user.username,
        'token': token
    })
