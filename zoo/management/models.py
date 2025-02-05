from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

# Custom User Model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def clean(self):
        super().clean()
        if self.phone_number and len(self.phone_number) < 11:
            raise ValidationError({"phone_number": "Phone number must be at least 11 digits long."})

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class OpeningHours(models.Model):
    date = models.DateField(unique=True)
    
    # Predefined opening times (e.g., 9 AM, 10 AM)
    OPENING_TIME_CHOICES = [
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
    ]
    
    # Predefined closing times (e.g., 5 PM, 6 PM, 9 PM)
    CLOSING_TIME_CHOICES = [
        ('17:00', '5:00 PM'),
        ('18:00', '6:00 PM'),
        ('21:00', '9:00 PM'),
    ]
    
    # Using CharField with choices instead of TimeField
    opening_time = models.CharField(max_length=5, choices=OPENING_TIME_CHOICES, null=True, blank=True)
    closing_time = models.CharField(max_length=5, choices=CLOSING_TIME_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.date}: {self.opening_time} - {self.closing_time}"

    # Define color mapping based on opening and closing times
    COLOR_MAP = {
        ("10:00", "18:00"): "green",
        ("10:00", "17:00"): "orange",
        ("09:00", "17:00"): "blue",
        ("09:00", "18:00"): "purple",
        ("09:00", "21:00"): "crimson",
    }

    def get_color(self):
        # Directly compare the opening_time and closing_time as strings (no need for strftime)
        time_key = (self.opening_time, self.closing_time)
        return self.COLOR_MAP.get(time_key, "red" if not self.opening_time else "grey")

    @classmethod
    def bulk_create_or_update(cls, dates, opening_time, closing_time):
        existing_hours = {oh.date: oh for oh in cls.objects.filter(date__in=dates)}
        new_entries = []

        for date in dates:
            if date in existing_hours:
                existing_hours[date].opening_time = opening_time
                existing_hours[date].closing_time = closing_time
                existing_hours[date].save()
            else:
                new_entries.append(cls(date=date, opening_time=opening_time, closing_time=closing_time))

        if new_entries:
            cls.objects.bulk_create(new_entries)

# Closed Days Model
class ClosedDays(models.Model):
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Closed on {self.date} - {self.reason or 'No specific reason'}"

# Booking Model
class BookingModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Booking by {self.name} for {self.booking_date} at {self.booking_time}"

# Event Model
class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_time']
