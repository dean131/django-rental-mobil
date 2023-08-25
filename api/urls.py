from django.urls import path
from .views import car_list, rental_list, HomePageView

urlpatterns = [
    path('cars/', car_list, name='car-list'),
    path('rentals/', rental_list, name='rental-list'),

    path('home/', HomePageView.as_view(), name='home'),
]
