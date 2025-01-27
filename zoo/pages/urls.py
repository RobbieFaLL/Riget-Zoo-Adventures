from django.contrib import admin
from django.urls import path
from .views import Homepage, About

urlpatterns = [
    path('', Homepage, name='Homepage'),
    path('aboutus', About, name='About')
]
