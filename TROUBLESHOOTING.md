# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with Riget Zoo Adventures.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Development Environment](#development-environment)
- [Database Issues](#database-issues)
- [Authentication Problems](#authentication-problems)
- [Booking System Issues](#booking-system-issues)
- [Static Files and Media](#static-files-and-media)
- [Performance Issues](#performance-issues)
- [Production Deployment](#production-deployment)
- [Error Messages](#error-messages)
- [Getting Help](#getting-help)

## Installation Issues

### Virtual Environment Problems

#### Issue: `python -m venv env` fails
**Symptoms:**
```
Error: No module named venv
```

**Solutions:**
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# macOS (using Homebrew)
brew install python

# Windows
# Use python.exe -m venv env
```

#### Issue: Virtual environment activation fails
**Symptoms:**
```
bash: env/bin/activate: No such file or directory
```

**Solutions:**
```bash
# Check if virtual environment was created properly
ls -la env/

# Recreate virtual environment
rm -rf env
python3 -m venv env

# Windows activation
env\Scripts\activate
```

### Dependency Installation Issues

#### Issue: `pip install -r requirements.txt` fails
**Common Errors and Solutions:**

**Error:** `error: Microsoft Visual C++ 14.0 is required`
```bash
# Windows solution
# Install Microsoft Build Tools for Visual Studio
# Or use pre-compiled wheels:
pip install --only-binary=all -r zoo/requirements.txt
```

**Error:** `Failed building wheel for psycopg2`
```bash
# Use binary version instead
pip install psycopg2-binary
```

**Error:** `Permission denied`
```bash
# Use user installation
pip install --user -r zoo/requirements.txt

# Or ensure virtual environment is activated
source env/bin/activate  # Linux/macOS
env\Scripts\activate      # Windows
```

## Development Environment

### Django Server Issues

#### Issue: `python manage.py runserver` fails
**Common Errors:**

**Error:** `ModuleNotFoundError: No module named 'django'`
```bash
# Ensure virtual environment is activated
source env/bin/activate

# Install Django
pip install django

# Or install all requirements
pip install -r requirements.txt
```

**Error:** `Port already in use`
```bash
# Use different port
python manage.py runserver 8001

# Or kill process using port 8000
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

#### Issue: Browser shows "Server Error (500)"
**Debugging Steps:**
```bash
# Check Django settings
python manage.py check

# View detailed error in terminal
# Set DEBUG=True temporarily in settings.py

# Check Django logs
tail -f django.log
```

### Database Migration Issues

#### Issue: Migration conflicts
**Error:** `django.db.migrations.exceptions.InconsistentMigrationHistory`

**Solution:**
```bash
# Reset migrations (development only!)
rm management/migrations/0*.py
rm pages/migrations/0*.py

# Create new initial migration
python manage.py makemigrations management
python manage.py makemigrations pages

# Apply migrations
python manage.py migrate
```

#### Issue: Database locked error
**Error:** `sqlite3.OperationalError: database is locked`

**Solutions:**
```bash
# Stop all Django processes
pkill -f runserver

# Remove database lock (if exists)
rm db.sqlite3-journal

# Restart development server
python manage.py runserver
```

## Database Issues

### SQLite Issues

#### Issue: Database corruption
**Symptoms:**
- Random errors when accessing database
- `sqlite3.DatabaseError: database disk image is malformed`

**Solutions:**
```bash
# Backup current database
cp db.sqlite3 db.sqlite3.backup

# Try to repair
sqlite3 db.sqlite3 ".recover" | sqlite3 db_recovered.sqlite3

# If repair fails, restore from backup or recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### PostgreSQL Issues (Production)

#### Issue: Connection refused
**Error:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
```bash
# Check PostgreSQL service status
sudo systemctl status postgresql

# Start PostgreSQL service
sudo systemctl start postgresql

# Check connection parameters
python manage.py dbshell
```

#### Issue: Authentication failed
**Error:** `psycopg2.OperationalError: FATAL: authentication failed`

**Solutions:**
```bash
# Reset PostgreSQL user password
sudo -u postgres psql
ALTER USER riget_zoo_user PASSWORD 'new_password';

# Update environment variables
export DB_PASSWORD=new_password
```

## Authentication Problems

### User Registration Issues

#### Issue: User registration fails silently
**Debugging Steps:**
```python
# Check form validation in Django shell
python manage.py shell

from management.forms import YourRegistrationForm
form = YourRegistrationForm(data={
    'username': 'testuser',
    'email': 'test@example.com',
    'password1': 'testpass123',
    'password2': 'testpass123'
})
print(form.is_valid())
print(form.errors)
```

#### Issue: Phone number validation fails
**Error:** Phone number validation errors

**Solutions:**
```python
# Check phone number format in models.py
# Ensure phone number has at least 11 digits
phone_number = "12345678901"  # Correct format

# Debug validation
from management.models import CustomUser
user = CustomUser(phone_number="123")  # Too short
user.clean()  # Should raise ValidationError
```

### Login Issues

#### Issue: "Invalid credentials" for valid users
**Debugging Steps:**
```bash
# Check if user exists
python manage.py shell
from management.models import CustomUser
user = CustomUser.objects.get(username='your_username')
print(user.check_password('your_password'))

# Test authentication backend
from django.contrib.auth import authenticate
user = authenticate(username='test@example.com', password='password')
print(user)
```

#### Issue: Session issues
**Symptoms:**
- User gets logged out immediately
- Session data not persisting

**Solutions:**
```python
# Check session configuration in settings.py
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Clear sessions
python manage.py clearsessions
```

## Booking System Issues

### Calendar Display Problems

#### Issue: Calendar not showing opening hours
**Debugging Steps:**
```bash
# Check if opening hours data exists
python manage.py shell
from management.models import OpeningHours
print(OpeningHours.objects.all())

# Create test data
from datetime import date
oh = OpeningHours.objects.create(
    date=date.today(),
    opening_time='09:00',
    closing_time='18:00'
)
```

#### Issue: Calendar colors not displaying
**Check the color mapping in models.py:**
```python
# Verify COLOR_MAP in OpeningHours model
def get_color(self):
    time_key = (self.opening_time, self.closing_time)
    return self.COLOR_MAP.get(time_key, "red")
```

### Booking Form Issues

#### Issue: Booking form validation fails
**Common Issues:**
```python
# Check date format
booking_date = "2025-10-15"  # Correct format (YYYY-MM-DD)

# Check time format
booking_time = "10:00"  # Correct format (HH:MM)

# Validate phone number
phone = "12345678901"  # Must be at least 11 digits
```

#### Issue: Booking success page not loading
**Check URL configuration:**
```python
# In management/urls.py
path('booking/success/', booking_success, name='booking_success'),

# Ensure view function exists
def booking_success(request):
    return render(request, 'Booking_Success.html')
```

## Static Files and Media

### CSS/JavaScript Not Loading

#### Issue: Static files return 404
**Solutions:**
```python
# Check settings.py
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'zoo/devstatic')
]

# Collect static files
python manage.py collectstatic

# Check file paths
python manage.py findstatic css/your-file.css
```

#### Issue: Static files not updating
**Solutions:**
```bash
# Clear browser cache
# Hard refresh (Ctrl+F5 or Cmd+Shift+R)

# Restart development server
python manage.py runserver

# Check file timestamps
ls -la zoo/devstatic/css/
```

### Template Issues

#### Issue: Template not found
**Error:** `TemplateDoesNotExist`

**Solutions:**
```python
# Check TEMPLATES setting in settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Check this path
        'APP_DIRS': True,
        # ...
    },
]

# Verify template file exists
ls -la templates/your_template.html
```

## Performance Issues

### Slow Page Loading

#### Issue: Database queries taking too long
**Debugging:**
```python
# Enable query logging in settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Use Django Debug Toolbar
pip install django-debug-toolbar
```

#### Issue: High memory usage
**Solutions:**
```python
# Optimize database queries
# Use select_related() for foreign keys
bookings = BookingModel.objects.select_related('user').all()

# Use prefetch_related() for many-to-many
events = Event.objects.prefetch_related('attendees').all()

# Paginate large datasets
from django.core.paginator import Paginator
```

## Production Deployment

### Gunicorn Issues

#### Issue: Gunicorn won't start
**Check logs:**
```bash
# View Gunicorn logs
tail -f /var/log/riget_zoo/gunicorn_supervisor.log

# Test Gunicorn manually
cd /path/to/your/app
source venv/bin/activate
gunicorn zoo.wsgi:application --bind 127.0.0.1:8000
```

#### Issue: 502 Bad Gateway
**Common Causes:**
```bash
# Check if Gunicorn is running
ps aux | grep gunicorn

# Check socket file permissions
ls -la /path/to/your/app/*.sock

# Restart services
sudo supervisorctl restart riget_zoo
sudo systemctl reload nginx
```

### Nginx Issues

#### Issue: Static files not served
**Check Nginx configuration:**
```nginx
location /static/ {
    alias /path/to/your/staticfiles/;
    expires 30d;
}

# Test Nginx config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### SSL Certificate Issues

#### Issue: SSL certificate errors
**Solutions:**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

## Error Messages

### Common Django Errors

#### `ImproperlyConfigured: The SECRET_KEY setting must not be empty`
**Solution:**
```python
# Set SECRET_KEY in settings.py
SECRET_KEY = 'your-secret-key-here'

# Or use environment variable
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
```

#### `OperationalError: no such table`
**Solution:**
```bash
# Run migrations
python manage.py migrate

# If migrations exist but table doesn't
python manage.py migrate --run-syncdb
```

#### `AttributeError: 'NoneType' object has no attribute`
**Debugging:**
```python
# Add debug prints
print(f"Variable value: {your_variable}")
print(f"Variable type: {type(your_variable)}")

# Check for None values
if your_variable is not None:
    # Use the variable
    pass
```

### HTTP Error Codes

#### 400 Bad Request
- Check form validation
- Verify CSRF token
- Check request data format

#### 403 Forbidden
- Check user permissions
- Verify CSRF token
- Check `ALLOWED_HOSTS` setting

#### 404 Not Found
- Check URL patterns
- Verify file paths
- Check template names

#### 500 Internal Server Error
- Check Django logs
- Verify database connection
- Check for Python exceptions

## Getting Help

### Before Asking for Help

1. **Check the logs** - Most issues show up in error logs
2. **Search existing issues** - Check GitHub issues for similar problems
3. **Test in isolation** - Try to reproduce the issue with minimal code
4. **Check documentation** - Review Django and project documentation

### What to Include When Reporting Issues

```markdown
## Issue Description
Brief description of the problem

## Environment
- Operating System: [e.g., Ubuntu 22.04]
- Python Version: [e.g., 3.13.0]
- Django Version: [e.g., 5.1.3]
- Browser: [e.g., Chrome 118.0]

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Error Messages
```
Include full error messages and stack traces
```

## Screenshots
If applicable, add screenshots

## Additional Context
Any other relevant information
```

### Where to Get Help

1. **GitHub Issues**: [Project Issues](https://github.com/RobbieFaLL/Riget-Zoo-Adventures/issues)
2. **Django Documentation**: [Django Docs](https://docs.djangoproject.com/)
3. **Stack Overflow**: Tag questions with `django` and `riget-zoo-adventures`
4. **Django Community**: [Django Forum](https://forum.djangoproject.com/)

### Debug Mode Checklist

```python
# Enable debug mode temporarily (development only!)
DEBUG = True

# Add detailed logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Install debug toolbar
pip install django-debug-toolbar
```

### Emergency Recovery

#### If the site is completely broken:
```bash
# Revert to last known good commit
git reset --hard HEAD~1

# Restore database from backup
cp db.sqlite3.backup db.sqlite3

# Restart all services
sudo supervisorctl restart riget_zoo
sudo systemctl reload nginx
```

#### Quick health check:
```bash
# Test basic functionality
python manage.py check
python manage.py migrate --check
curl -I http://your-domain.com/
```

---

**Last Updated**: October 2025

Remember: When in doubt, check the logs first! Most issues can be diagnosed by examining error messages and stack traces.

For additional support, please refer to our [Contributing Guidelines](CONTRIBUTING.md) or open an issue on GitHub.