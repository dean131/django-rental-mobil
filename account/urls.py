from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    # path('login-user/', views.login_user, name='login-user'),
    path('login/', views.LoginView.as_view(), name='knox_login'),
    path('logout/', views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', views.LogoutAllView.as_view(), name='knox_logout_all'),
]