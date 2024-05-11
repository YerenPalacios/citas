from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, name, phone, email, password=None):
        if not email:
            raise ValueError('Email must be provided')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, phone=phone)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    role = models.CharField(max_length=15, blank=True, null=True, default="PATIENT")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.pk} {self.email}: {self.name}'


class Appointment(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField(blank=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_apointments")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_apointments")

    def __str__(self):
        return f'{self.pk} {self.date}'