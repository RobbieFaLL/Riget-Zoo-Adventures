from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.phone_number and len(self.phone_number) < 11:
            raise ValidationError({"phone_number": "Phone number must be at least 11 digits long."})


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

class opening_hours_list(models.Model):
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    is_open = models.BooleanField(default=True)  # True for open, False for closed
    open_time = models.TimeField(null=True, blank=True)  # Store opening time
    close_time = models.TimeField(null=True, blank=True)  # Store closing time

    def __str__(self):
        return f"{self.day_of_week} - {'Open' if self.is_open else 'Closed'}"

class ClosedDays(models.Model):
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Closed on {self.date} - {self.reason or 'No specific reason'}"

class Bookingmodel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Booking by {self.name} for {self.booking_date} at {self.booking_time}"
    
    
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)  # Event title
    start_time = models.DateTimeField()  # Event start time
    end_time = models.DateTimeField()  # Event end time
    description = models.TextField(blank=True, null=True)  # Optional description
    location = models.CharField(max_length=255, blank=True, null=True)  # Optional location
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the event was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of when the event was last updated

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_time']  # Optional: sort events by start time
