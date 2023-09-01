from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, 
    AbstractBaseUser,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email,password=None, full_name=None,  *args, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), full_name=full_name, *args, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(email=email, password=password, full_name=full_name,)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True,)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True) 
    nik = models.CharField(max_length=16, unique=True, blank=True, null=True)  
    license_card_image = models.ImageField(blank=True, null=True)
    id_card_image = models.ImageField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)

    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True,)
    last_login = models.DateField(verbose_name='last login', auto_now=True,)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OTPCode(models.Model):
    code = models.IntegerField(null=True, blank=True)
    expire = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.expire = timezone.now() + timedelta(minutes=5)
        super(OTPCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.full_name