from django.urls import path

from .views import (
    RegisterAPIView,
    LoginView,
    LogoutView,
    LogoutAllView,
    UserModelViewSet,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='knox_logout_all'),

    path('userdetail/<str:pk>/', UserModelViewSet.as_view({'get': 'retrieve'}), name='userdetail'),
    path('userlist/', UserModelViewSet.as_view({'get': 'list'}), name='userlist'),
    path('userupdate/<str:pk>/', UserModelViewSet.as_view({'patch': 'partial_update'}), name='userupdate'),
]