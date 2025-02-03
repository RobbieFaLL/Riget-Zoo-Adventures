
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define what fields to display in the admin panel
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')

    # Use the fieldsets from the base UserAdmin for consistency
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),  # Add custom fields here
    )

    # Use the add_fieldsets for the 'Add User' form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),  # Add custom fields here
    )

from .models import opening_hours_list, ClosedDays

@admin.register(opening_hours_list)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'open_time', 'close_time')
    search_fields = ('day_of_week',)
    
@admin.register(ClosedDays)
class ClosedDaysAdmin(admin.ModelAdmin):
    list_display = ('date', 'reason')
    search_fields = ('date', 'reason')
    
from django.contrib import admin
from .models import Bookingmodel

@admin.register(Bookingmodel)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'booking_date', 'booking_time', 'message')
    search_fields = ('name', 'email', 'booking_date', 'booking_time')
    list_filter = ('booking_date',)

from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'description', 'location', 'created_at', 'updated_at')
    list_filter = ('start_time', 'end_time')  # Filter events by date
    search_fields = ('title', 'description')  # Enable searching by title and description
