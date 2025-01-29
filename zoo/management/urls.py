from django.contrib import admin
from django.urls import path
from .views import signup, custom_login_view, Booking, check_user_exists
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', custom_login_view, name='login'),
    path('booking', Booking, name="Booking"),
    # Use the built-in LogoutView and specify a custom template for logout
    path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
     path('check_user_exists/', check_user_exists, name='check_user_exists'),
]