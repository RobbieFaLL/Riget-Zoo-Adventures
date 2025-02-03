from django.shortcuts import render, redirect
from .forms import CustomLoginForm, CustomSignupForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CustomUser, CustomUserManager
from django.contrib.auth.backends import ModelBackend

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)  # Log in the user after signup
            return redirect('home')  # Redirect to your desired page
        else:
            # Add custom messages for form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})
        

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Get the custom user model dynamically
            CustomUser = get_user_model()

            # Check if it's an email or username
            if '@' in username_or_email:  # It's an email
                try:
                    user = CustomUser.objects.get(email=username_or_email)
                except CustomUser.DoesNotExist:
                    form.add_error('username', 'This email address is not registered.')
                    return render(request, 'login.html', {'form': form})
            else:
                # It's a username
                try:
                    user = CustomUser.objects.get(username=username_or_email)
                except CustomUser.DoesNotExist:
                    form.add_error('username', 'This username is not registered.')
                    return render(request, 'login.html', {'form': form})

            # Check if the password is correct
            if user and user.check_password(password):
                # Set the backend to the default ModelBackend (or your custom backend)
                user.backend = 'django.contrib.auth.backends.ModelBackend'

                # Log the user in
                login(request, user)
                return redirect('Booking')  # Redirect to the booking page
            else:
                form.add_error(None, 'Invalid password. Please try again.')

        else:
            # Handle specific form errors
            for field, errors in form.errors.items():
                for error in errors:
                    form.add_error(field, error)
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)  # Logs the user out
    messages.success(request, "You have been logged out.")  # Optional success message
    return render(request, 'logout.html')  # Render the logout page instead of redirecting

from django.shortcuts import render, redirect
from .models import Bookingmodel, ClosedDays
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def Booking(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        message = request.POST.get('message', '')

        # Basic Validation: Ensure all required fields are provided
        if not name or not email or not phone or not booking_date or not booking_time:
            messages.error(request, "All fields are required. Please complete the form.")
            return redirect('booking')  # Redirect back to the booking form

        # Validate the booking date
        try:
            booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please select a valid date.")
            return redirect('booking')

        # Check if the zoo is closed on the selected date
        if ClosedDays.objects.filter(date=booking_date_obj).exists():
            messages.error(request, f"Sorry, the zoo is closed on {booking_date_obj}. Please choose another day.")
            return redirect('Booking')

        # Create the new booking instance using the Booking model
        booking_instance = Bookingmodel.objects.create(
            name=name,
            email=email,
            phone=phone,
            booking_date=booking_date_obj,
            booking_time=booking_time,
            message=message,
        )

        # Save the booking id in the session for later use (if needed)
        request.session['booking_id'] = booking_instance.id

        # Display a success message and redirect to the booking success page
        messages.success(request, "Your booking has been successfully confirmed!")
        return redirect('booking_success')

    return render(request, 'booking.html')
    
def booking_success(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('booking')
    booking_instance = Bookingmodel.objects.get(id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking_instance})


from django.http import JsonResponse
from .models import CustomUser

def check_user_exists(request):
    username_or_email = request.GET.get('username_or_email')

    # Check if it's an email or username
    if '@' in username_or_email:
        exists = CustomUser.objects.filter(email=username_or_email).exists()
    else:
        exists = CustomUser.objects.filter(username=username_or_email).exists()

    return JsonResponse({'exists': exists})

from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model

def check_user_exists_password(request):
    username_or_email = request.GET.get('username_or_email')
    password = request.GET.get('password')

    if not username_or_email or not password:
        return JsonResponse({"valid": False, "error_type": "missing_fields"})

    CustomUser = get_user_model()

    # Try to fetch the user by email first
    try:
        user = CustomUser.objects.get(email=username_or_email)
        username = user.username  # Convert email to username
    except CustomUser.DoesNotExist:
        # If not found by email, try username
        try:
            user = CustomUser.objects.get(username=username_or_email)
            username = user.username
        except CustomUser.DoesNotExist:
            return JsonResponse({"valid": False, "error_type": "user_not_found"})

    # Authenticate using the obtained username
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        return JsonResponse({"valid": True})
    else:
        return JsonResponse({"valid": False, "error_type": "invalid_password"})
    
from django.http import JsonResponse
from .models import Event

def event_list(request):
    # Assuming you have Event model to retrieve events from
    events = Event.objects.all()
    event_data = []
    
    for event in events:
        event_data.append({
            'title': event.title,
            'start': event.start_time,
            'end': event.end_time,
        })
    
    return JsonResponse(event_data, safe=False)


from django.shortcuts import render
from .models import Bookingmodel

def booking_success(request):
    # Retrieve the latest booking from the session or other context if necessary
    booking_id = request.session.get('booking_id')
    
    if not booking_id:
        # Handle cases where there is no booking found (e.g., session expired, or no booking made)
        return redirect('booking')  # Redirect to the booking page or show a different error
    
    booking = Bookingmodel.objects.get(id=booking_id)
    
    # Render the success page with the booking details
    return render(request, 'booking_success.html', {'booking': booking})

# views.py
from django.http import JsonResponse
from .models import opening_hours_list

DAY_MAP = {
    'Sunday': 0,
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}

from django.http import JsonResponse
from .models import Event, opening_hours_list

# Fetch and return the event data for FullCalendar
def event_list(request):
    events = Event.objects.all()  # Fetch events from your Event model
    event_data = []

    for event in events:
        event_data.append({
            'title': event.title,  # Event title
            'start': event.start_time.isoformat(),  # Event start time (ISO format)
            'end': event.end_time.isoformat(),  # Event end time (ISO format)
            'description': event.description,  # Optional: Add more fields as needed
            'color': '#378006',  # Optional: color for the event (green)
        })

    return JsonResponse(event_data, safe=False)

# Fetch and return the business hours (opening hours) for FullCalendar
def opening_hours(request):
    opening_hours = opening_hours_list.objects.all()  # Fetch opening hours from your model
    business_hours = []
    
    for day in opening_hours:
        if day.is_open:
            business_hours.append({
                'daysOfWeek': [get_day_of_week(day.day_of_week)],  # Convert string to FullCalendar day index
                'startTime': day.open_time.strftime('%H:%M'),
                'endTime': day.close_time.strftime('%H:%M'),
                'color': '#378006',  # Green color for open hours
            })
        else:
            # Mark as closed days with a red background color
            business_hours.append({
                'daysOfWeek': [get_day_of_week(day.day_of_week)],  # Days that are closed
                'rendering': 'background',
                'color': '#FF0000'  # Red color for closed days
            })
    
    return JsonResponse(business_hours, safe=False)

# Helper function to map day name to FullCalendar's dayOfWeek values
def get_day_of_week(day_name):
    days = {
        'Sunday': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
    }
    return days.get(day_name, None)


