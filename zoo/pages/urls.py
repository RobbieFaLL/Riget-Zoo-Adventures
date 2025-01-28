from django.contrib import admin
from django.urls import path
from .views import Homepage, About, Animals, Events, Conservation, Visit

urlpatterns = [
    path('', Homepage, name='Homepage'),
    path('aboutus', About, name='About'),
    path('animals', Animals, name='Animals'),
    path('events', Events, name='Events'),
    path('conservation', Conservation, name='Conservation'),
    path('visit', Visit, name='Visit')
]
