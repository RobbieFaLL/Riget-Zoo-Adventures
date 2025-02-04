from django.contrib import admin
from django.urls import path
from .views import (
    signup, custom_login_view, Booking, check_user_exists, 
    check_user_exists_password, booking_success, 
    opening_times_calendar, generate_calendar, get_day_details
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication Routes
    path('signup/', signup, name='signup'),
    path('login/', custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    # Booking Routes
    path('booking/', Booking, name="booking"),
    path('booking/success/', booking_success, name='booking_success'),

    # User Validation Routes
    path('check_user_exists/', check_user_exists, name='check_user_exists'),
    path('check_user_exists_password/', check_user_exists_password, name='check_user_exists_password'),

    # Calendar Routes
    path('calendar/', opening_times_calendar, name='calendar'),
    path('calendar/<int:year>/<int:month>/', opening_times_calendar, name='calendar_month'),
    path('calendar-data/', generate_calendar, name='calendar_json'),  # JSON API for calendar
    path('get-day-details/', get_day_details, name='get_day_details'),

]
