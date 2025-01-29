from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CustomUserManager
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username or email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Remove 'request' from kwargs
        super().__init__(*args, **kwargs)  # Call the base class constructor

    def clean_username(self):
        username_or_email = self.cleaned_data['username']
        CustomUser = get_user_model()  # Use the custom user model

        if '@' in username_or_email:  # It's an email address
            try:
                # Attempt to find the user by email
                user = CustomUser.objects.get(email=username_or_email)
                return user.username  # Return the username for authentication
            except CustomUser.DoesNotExist:
                raise ValidationError('No account found with this email address.')
        else:
            # Assume it's a username
            return username_or_email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError("Password cannot be empty")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Check if the username/email and password match
        if username_or_email and password:
            CustomUser = get_user_model()  # Use the custom user model
            try:
                if '@' in username_or_email:
                    user = CustomUser.objects.get(email=username_or_email)
                else:
                    user = CustomUser.objects.get(username=username_or_email)
                if not user.check_password(password):
                    raise ValidationError("Incorrect password.")
            except CustomUser.DoesNotExist:
                raise ValidationError("Invalid username or email.")
        return cleaned_data

    
class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[MinLengthValidator(11)],
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    surname = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'name', 'surname', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Create a password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        if commit:
            user.save()
        return user
