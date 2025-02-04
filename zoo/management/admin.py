from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClosedDays, Event, OpeningHours, BookingModel


# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)  # Ensure consistent ordering

    # Extend the default UserAdmin fieldsets to include custom fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),  
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),  
    )

# Opening Hours Admin
@admin.register(OpeningHours)
class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('date', 'opening_time', 'closing_time', 'get_color_display')
    search_fields = ('date',)
    ordering = ('date',)
    list_filter = ('opening_time', 'closing_time')

    def get_color_display(self, obj):
        """Display the color associated with the opening hours"""
        return obj.get_color()
    get_color_display.short_description = "Opening Hours Color"

# Closed Days Admin
@admin.register(ClosedDays)
class ClosedDaysAdmin(admin.ModelAdmin):
    list_display = ('date', 'reason')
    search_fields = ('date', 'reason')
    ordering = ('date',)
    list_filter = ('date',)

# Booking System Admin
@admin.register(BookingModel)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'booking_date', 'booking_time', 'message')
    search_fields = ('name', 'email', 'booking_date', 'booking_time')
    list_filter = ('booking_date',)
    ordering = ('-booking_date', '-booking_time')

# Events Admin
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'description', 'location', 'created_at', 'updated_at')
    list_filter = ('start_time', 'end_time')  
    search_fields = ('title', 'description')
    ordering = ('-start_time',)
    date_hierarchy = 'start_time'  # Enables quick navigation by date
