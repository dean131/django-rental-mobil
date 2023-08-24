from django.contrib import admin

from .models import Car, Customer, Rental 

# Register your models here.

admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Rental)
