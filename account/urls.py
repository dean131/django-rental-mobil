from django.urls import path

from .views import (
    register_user,
    LoginView,
    LogoutView,
    LogoutAllView,
    UserListView,
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', LogoutAllView.as_view(), name='knox_logout_all'),

    path('userlist/', UserListView.as_view(), name='user_list'),
]