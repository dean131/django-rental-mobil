from django.conf import settings
from django.db import models

from decimal import Decimal


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    
    name = models.CharField(max_length=255)
    car_type = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    color = models.CharField(max_length=50)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    license_plate = models.CharField(max_length=15, unique=True)
    passenger_capacity = models.IntegerField()
    fuel_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Rental(models.Model):
    STATUS_CHOICES = [
        ('aktif', 'Aktif'),
        ('pending', 'Pending'),
        ('selesai', 'Selesai'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Rental {self.id}: {self.car} by {self.customer} ({self.get_status_display()})"

    @property
    def total_cost(self):
        days = (self.end_date - self.start_date).days
        total_price = self.car.price * days
        return int(total_price)

    @property
    def total_days(self):
        duration = (self.end_date - self.start_date).days
        return duration
    
    @property
    def late_fee(self):
        fee = 0
        if self.check_out_date:
            if self.check_out_date > self.end_date:
                days = (self.check_out_date - self.end_date).days
                fee = days * (Decimal(0.02) * self.total_cost)
        return int(fee)
    
