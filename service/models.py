from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Service(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    owner_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Ensures unique email
    phone = models.CharField(max_length=10)
    vehicle_no = models.CharField(max_length=20, unique=True)
    trip = models.PositiveIntegerField()  # Ensures non-negative trip values
    address = models.TextField()
    last_service = models.DateField()
    booking_date = models.DateField()
    problems = models.TextField(blank=True, null=True)  # Optional field

    def __str__(self):
        return f"{self.owner_name} - {self.vehicle_no}"
    


import random
import string
from django.utils import timezone

def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + timezone.timedelta(minutes=5)  # OTP expires in 5 minutes
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP for {self.user.username}"

    def is_valid(self):
        return timezone.now() < self.expires_at