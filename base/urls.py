from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout_user'),

    path('', views.home, name='home'),
    path('rentals-page', views.rentals_page, name='rentals_page'),
    path('add-rental/', views.add_rental, name='add_rental'),
    path('edit-rental/<str:pk>/', views.edit_rental, name='edit_rental'),
    path('checkout-rental/<str:pk>/', views.checkout_rental, name='checkout_rental'),
    
    path('cars-page/', views.cars_page, name='cars_page'),

    path('users-page/', views.users_page, name='users_page'),
]