from django.urls import path
from .views import car_list, customer_list, rental_list

urlpatterns = [
    path('cars/', car_list, name='car-list'),
    path('customers/', customer_list, name='customer-list'),
    path('rentals/', rental_list, name='rental-list'),
]
