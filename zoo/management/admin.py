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

from datetime import date, timedelta
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import BulkOpeningHoursForm
from .models import OpeningHours
from django.urls import path
from django.contrib import admin
from datetime import datetime

@admin.register(OpeningHours)

class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('date', 'opening_time', 'closing_time')
    change_list_template = "admin/opening_hours_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-set-hours/', self.admin_site.admin_view(self.bulk_set_hours_view), name='bulk_set_hours'),
        ]
        return custom_urls + urls

    def bulk_set_hours_view(self, request):
        """Handles bulk setting of opening hours inside Django Admin"""
        today = date.today()  # Define today here
        available_dates = [today + timedelta(days=i) for i in range(365)]  # Next 30 days

        if request.method == 'POST':
            form = BulkOpeningHoursForm(request.POST)
            if form.is_valid():
                selected_dates = []
                
                # Check for which checkboxes are selected
                for available_date in available_dates:
                    field_name = f"date_{available_date}"
                    if field_name in form.cleaned_data and form.cleaned_data[field_name]:
                        selected_dates.append(available_date)

                # Get the opening_time and closing_time from the form (selected via tickboxes)
                opening_time = form.cleaned_data['opening_time']
                closing_time = form.cleaned_data['closing_time']

                # Use bulk_create_or_update to save the dates
                OpeningHours.bulk_create_or_update(selected_dates, opening_time, closing_time)

                self.message_user(request, "Opening hours updated successfully.")
                return HttpResponseRedirect("../")  # Redirect back to admin

        else:
            form = BulkOpeningHoursForm()

        context = {
            'form': form,
            'opts': self.model._meta,  # Needed for admin templates
        }
        return render(request, 'admin/bulk_opening_hours.html', context)

    
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
