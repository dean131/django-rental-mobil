from django.conf import settings
from django.db import models
from django.utils import timezone


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('A', 'Automatic'),
        ('M', 'Manual'),
    ]
    
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    color = models.CharField(max_length=50)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    license_plate = models.CharField(max_length=15, unique=True)
    passenger_capacity = models.PositiveIntegerField()
    fuel_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(blank=True, null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Rental(models.Model):
    STATUS_CHOICES = [
        ('A', 'Aktif'),
        ('P', 'Menunggu'),
        ('C', 'Selesai'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Rental {self.id}: {self.car} by {self.customer} ({self.get_status_display()})"

    @property
    def total_cost(self):
        duration = (self.end_date - self.start_date).days
        total = self.car.price * duration
        return total

    @property
    def total_days(self):
        duration = (self.end_date - self.start_date).days
        return duration
    
