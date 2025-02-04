from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
import calendar
from .models import CustomUser, BookingModel, ClosedDays, OpeningHours, Event
from .forms import CustomLoginForm, CustomSignupForm

# Signup View
def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

# Custom Login View
def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            CustomUser = get_user_model()

            try:
                user = CustomUser.objects.get(email=username_or_email) if '@' in username_or_email else CustomUser.objects.get(username=username_or_email)
            except CustomUser.DoesNotExist:
                form.add_error('username', 'User not found.')
                return render(request, 'login.html', {'form': form})

            if user.check_password(password):
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('booking')
            else:
                form.add_error(None, 'Invalid password.')

    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return render(request, 'logout.html')

# Booking View
@login_required
def Booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        message = request.POST.get('message', '')

        if not all([name, email, phone, booking_date, booking_time]):
            messages.error(request, "All fields are required.")
            return redirect('booking')

        try:
            booking_date_obj = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('booking')

        if ClosedDays.objects.filter(date=booking_date_obj).exists():
            messages.error(request, f"Sorry, we are closed on {booking_date_obj}.")
            return redirect('booking')

        booking_instance = BookingModel.objects.create(
            name=name, email=email, phone=phone, booking_date=booking_date_obj,
            booking_time=booking_time, message=message
        )

        request.session['booking_id'] = booking_instance.id
        messages.success(request, "Your booking has been confirmed!")
        return redirect('booking_success')

    return render(request, 'booking.html')

# Booking Success View
def booking_success(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('booking')
    
    booking_instance = BookingModel.objects.get(id=booking_id)
    return render(request, 'booking_success.html', {'booking': booking_instance})

# Check if User Exists (AJAX)
def check_user_exists(request):
    username_or_email = request.GET.get('username_or_email')
    exists = CustomUser.objects.filter(email=username_or_email).exists() if '@' in username_or_email else CustomUser.objects.filter(username=username_or_email).exists()
    return JsonResponse({'exists': exists})

# Check if User Exists with Password (AJAX)
def check_user_exists_password(request):
    username_or_email = request.GET.get('username_or_email')
    password = request.GET.get('password')

    if not username_or_email or not password:
        return JsonResponse({"valid": False, "error_type": "missing_fields"})

    CustomUser = get_user_model()

    try:
        user = CustomUser.objects.get(email=username_or_email) if '@' in username_or_email else CustomUser.objects.get(username=username_or_email)
    except CustomUser.DoesNotExist:
        return JsonResponse({"valid": False, "error_type": "user_not_found"})

    user = authenticate(request, username=user.username, password=password)

    return JsonResponse({"valid": True} if user else {"valid": False, "error_type": "invalid_password"})

# Generate Calendar Data

def generate_calendar(year, month):
    """Generate a structured calendar list for the given month."""
    cal = calendar.Calendar()
    first_day, num_days = calendar.monthrange(year, month)
    days = list(cal.itermonthdates(year, month))

    structured_calendar = []
    week = []

    for day in days:
        if day.month != month:
            week.append({'date': day, 'opening_time': None, 'closing_time': None, 'color': 'grey'})
        else:
            opening_entry = OpeningHours.objects.filter(date=day).first()
            color = opening_entry.get_color() if opening_entry else 'red'
            week.append({
                'date': day,
                'opening_time': opening_entry.opening_time.strftime('%H:%M') if opening_entry else None,
                'closing_time': opening_entry.closing_time.strftime('%H:%M') if opening_entry else None,
                'color': color,
            })

        if len(week) == 7:
            structured_calendar.append(week)
            week = []

    if week:
        structured_calendar.append(week)

    return structured_calendar

from datetime import datetime, timedelta

# Opening Times Calendar View

def opening_times_calendar(request, year=None, month=None):
    today = datetime.today().date()  # Ensure correct usage

    # Convert year and month to integers, or use the current year/month
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    # Generate calendar data
    calendar_data = generate_calendar(year, month)

    # Calculate previous and next months
    prev_month, prev_year = (month - 1, year) if month > 1 else (12, year - 1)
    next_month, next_year = (month + 1, year) if month < 12 else (1, year + 1)

    return render(request, 'calendar.html', {
        'calendar_data': calendar_data,
        'month': month,
        'year': year,
        'month_name': calendar.month_name[month],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year
    })
    
# Event List (AJAX for Calendar)
def event_list(request):
    events = Event.objects.all()
    event_data = [
        {
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'description': event.description,
            'color': '#378006',
        }
        for event in events
    ]
    return JsonResponse(event_data, safe=False)

# Opening Hours API (AJAX for Calendar)
def opening_hours(request):
    opening_hours = OpeningHours.objects.all()
    business_hours = [
               {
            'daysOfWeek': [day.date.weekday()],  # Convert date to day index (0 = Monday, 6 = Sunday)
            'startTime': day.opening_time.strftime('%H:%M') if day.opening_time else None,
            'endTime': day.closing_time.strftime('%H:%M') if day.closing_time else None,
            'color': day.get_color(),  # Get the predefined color for the opening hours
        }
        for day in opening_hours
    ]

    return JsonResponse(business_hours, safe=False)

from django.http import JsonResponse
from .models import OpeningHours, ClosedDays

def get_day_details(request):
    """ Returns JSON data with opening hours or closure reason when a date is clicked """
    date_str = request.GET.get('date')
    
    try:
        opening_entry = OpeningHours.objects.get(date=date_str)
        response = {
            "date": date_str,
            "status": "open",
            "opening_time": opening_entry.opening_time.strftime('%H:%M'),
            "closing_time": opening_entry.closing_time.strftime('%H:%M')
        }
    except OpeningHours.DoesNotExist:
        try:
            closed_entry = ClosedDays.objects.get(date=date_str)
            response = {
                "date": date_str,
                "status": "closed",
                "reason": closed_entry.reason or "No specific reason provided"
            }
        except ClosedDays.DoesNotExist:
            response = {
                "date": date_str,
                "status": "unknown",
                "message": "No data available for this day."
            }
    
    return JsonResponse(response)
