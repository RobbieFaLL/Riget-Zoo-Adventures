from django.contrib import admin
from django.urls import path
from .views import signup, custom_login_view, Booking, check_user_exists, opening_hours, check_user_exists_password, event_list, booking_success
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', custom_login_view, name='login'),
    path('booking/', Booking, name="Booking"),
    path('booking/success/', booking_success, name='booking_success'),
    path('opening-hours/', opening_hours, name='opening_hours'),
    path('events/', event_list, name='event_list'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('check_user_exists/', check_user_exists, name='check_user_exists'),
    path('check_user_exists_password/', check_user_exists_password, name='check_user_exists_password'),
]
