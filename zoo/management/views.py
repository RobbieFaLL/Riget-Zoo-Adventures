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

@login_required
def Booking(request):
    return render(request, 'booking.html')


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
