from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20) 
    nik = models.CharField(max_length=16, unique=True)  
    # foto profil
    
    def __str__(self):
        return self.full_name
    

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('Auto', 'Automatic'),
        ('Manual', 'Manual'),
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

    def __str__(self):
        return self.name
    

class Rental(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Aktif'),
        ('Pending', 'Menunggu'),
        ('Completed', 'Selesai'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

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
    
