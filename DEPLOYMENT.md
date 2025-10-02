# Deployment Guide

This guide provides comprehensive instructions for deploying Riget Zoo Adventures to production environments.

## Table of Contents
- [Deployment Overview](#deployment-overview)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Platform-Specific Deployments](#platform-specific-deployments)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Static Files](#static-files)
- [Security Considerations](#security-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Deployment Overview

Riget Zoo Adventures is a Django web application that can be deployed on various platforms. This guide covers deployment to:

- **Heroku** (Platform as a Service)
- **DigitalOcean** (Virtual Private Server)
- **AWS** (Amazon Web Services)
- **Traditional VPS** (Ubuntu/CentOS)
- **Docker** (Containerized deployment)

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Git
- PostgreSQL (recommended for production)
- Web server (Nginx/Apache)
- Process manager (Gunicorn/uWSGI)

### Dependencies
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib
```

## Environment Setup

### 1. Create Production Settings

Create a production settings file: `zoo/zoo/settings_production.py`

```python
from .settings import *
import os

# Production settings
DEBUG = False

# Update with your domain
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files (if using file uploads)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email configuration (update with your email service)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Environment Variables

Create a `.env` file for environment variables:

```bash
# Database
DB_NAME=riget_zoo_production
DB_USER=riget_zoo_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your_production_secret_key
DJANGO_SETTINGS_MODULE=zoo.settings_production

# Email
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@your-domain.com
EMAIL_HOST_PASSWORD=your_email_password

# Security
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Platform-Specific Deployments

### Heroku Deployment

#### 1. Prepare for Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn zoo.wsgi --log-file -" > Procfile

# Create runtime.txt
echo "python-3.13.0" > runtime.txt

# Update requirements.txt
pip freeze > zoo/requirements.txt
echo "gunicorn==21.2.0" >> zoo/requirements.txt
echo "psycopg2-binary==2.9.7" >> zoo/requirements.txt
echo "whitenoise==6.5.0" >> zoo/requirements.txt
```

#### 2. Configure WhiteNoise (for static files)
Add to `settings_production.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### 3. Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create riget-zoo-adventures

# Set environment variables
heroku config:set SECRET_KEY="your_secret_key"
heroku config:set DJANGO_SETTINGS_MODULE="zoo.settings_production"

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Run migrations
heroku run python zoo/manage.py migrate

# Create superuser
heroku run python zoo/manage.py createsuperuser

# Collect static files
heroku run python zoo/manage.py collectstatic --noinput
```

### DigitalOcean Deployment

#### 1. Create Droplet
```bash
# Create Ubuntu 22.04 droplet
# Connect via SSH
ssh root@your_server_ip
```

#### 2. Server Setup
```bash
# Update system
apt update && apt upgrade -y

# Install dependencies
apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git -y

# Create application user
adduser riget_zoo
usermod -aG sudo riget_zoo

# Switch to application user
su - riget_zoo
```

#### 3. Application Setup
```bash
# Clone repository
git clone https://github.com/RobbieFaLL/Riget-Zoo-Adventures.git
cd Riget-Zoo-Adventures

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r zoo/requirements.txt
pip install gunicorn psycopg2-binary

# Create production settings
cp zoo/zoo/settings.py zoo/zoo/settings_production.py
# Edit settings_production.py as shown above
```

#### 4. Database Setup
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE riget_zoo_production;
CREATE USER riget_zoo_user WITH PASSWORD 'your_secure_password';
ALTER ROLE riget_zoo_user SET client_encoding TO 'utf8';
ALTER ROLE riget_zoo_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE riget_zoo_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE riget_zoo_production TO riget_zoo_user;
\q
```

#### 5. Gunicorn Configuration
Create `/home/riget_zoo/gunicorn_start.sh`:
```bash
#!/bin/bash

NAME="riget_zoo_adventures"
DJANGODIR=/home/riget_zoo/Riget-Zoo-Adventures/zoo
SOCKFILE=/home/riget_zoo/riget_zoo_adventures.sock
USER=riget_zoo
GROUP=riget_zoo
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=zoo.settings_production
DJANGO_WSGI_MODULE=zoo.wsgi

cd $DJANGODIR
source /home/riget_zoo/Riget-Zoo-Adventures/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=-
```

Make it executable:
```bash
chmod +x /home/riget_zoo/gunicorn_start.sh
```

#### 6. Supervisor Configuration
Create `/etc/supervisor/conf.d/riget_zoo.conf`:
```ini
[program:riget_zoo]
command = /home/riget_zoo/gunicorn_start.sh
user = riget_zoo
stdout_logfile = /var/log/riget_zoo/gunicorn_supervisor.log
redirect_stderr = true
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
```

#### 7. Nginx Configuration
Create `/etc/nginx/sites-available/riget_zoo`:
```nginx
upstream riget_zoo_app_server {
    server unix:/home/riget_zoo/riget_zoo_adventures.sock fail_timeout=0;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    client_max_body_size 4G;
    
    access_log /var/log/nginx/riget_zoo.access.log;
    error_log /var/log/nginx/riget_zoo.error.log;
    
    location /static/ {
        alias /home/riget_zoo/Riget-Zoo-Adventures/zoo/staticfiles/;
    }
    
    location /media/ {
        alias /home/riget_zoo/Riget-Zoo-Adventures/zoo/media/;
    }
    
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://riget_zoo_app_server;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/riget_zoo /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### AWS Deployment (EC2 + RDS)

#### 1. EC2 Instance Setup
```bash
# Launch EC2 instance (Ubuntu 22.04)
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# Follow similar setup as DigitalOcean
# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv nginx git supervisor -y
```

#### 2. RDS Database Setup
```bash
# Create RDS PostgreSQL instance through AWS Console
# Note connection details for environment variables
```

#### 3. Application Deployment
```bash
# Similar to DigitalOcean deployment
# Update database settings to use RDS endpoint
```

### Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY zoo/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Copy application code
COPY zoo/ .

# Collect static files
RUN python manage.py collectstatic --noinput --settings=zoo.settings_production

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "zoo.wsgi"]
```

#### 2. Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=zoo.settings_production
      - DB_HOST=db
      - DB_NAME=riget_zoo
      - DB_USER=riget_zoo
      - DB_PASSWORD=password
    depends_on:
      - db
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=riget_zoo
      - POSTGRES_USER=riget_zoo
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/var/www/static
      - media_volume:/var/www/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### 3. Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Configuration

### Environment Variables
Set these environment variables in your production environment:

```bash
# Required
SECRET_KEY=your_production_secret_key
DJANGO_SETTINGS_MODULE=zoo.settings_production
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host

# Optional
EMAIL_HOST=your_email_host
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
SENTRY_DSN=your_sentry_dsn  # For error tracking
```

### SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## Database Setup

### PostgreSQL Production Setup
```sql
-- Create database
CREATE DATABASE riget_zoo_production;

-- Create user
CREATE USER riget_zoo_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE riget_zoo_production TO riget_zoo_user;
ALTER USER riget_zoo_user CREATEDB;

-- Configure PostgreSQL settings for production
-- Edit /etc/postgresql/15/main/postgresql.conf
shared_preload_libraries = 'pg_stat_statements'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
```

### Database Migration
```bash
# Run migrations
python manage.py migrate --settings=zoo.settings_production

# Create superuser
python manage.py createsuperuser --settings=zoo.settings_production

# Load initial data (if any)
python manage.py loaddata initial_data.json --settings=zoo.settings_production
```

## Static Files

### Collect Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput --settings=zoo.settings_production
```

### CDN Setup (Optional)
For better performance, consider using a CDN:
- AWS CloudFront
- Cloudflare
- KeyCDN

## Security Considerations

### Security Checklist
- [ ] DEBUG = False in production
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set secure cookie flags
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Database connection encryption
- [ ] Firewall configuration
- [ ] Regular backups

### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Check status
sudo ufw status
```

### Regular Updates
```bash
# Create update script
#!/bin/bash
cd /home/riget_zoo/Riget-Zoo-Adventures
git pull origin main
source venv/bin/activate
pip install -r zoo/requirements.txt
python zoo/manage.py migrate --settings=zoo.settings_production
python zoo/manage.py collectstatic --noinput --settings=zoo.settings_production
sudo supervisorctl restart riget_zoo
sudo systemctl reload nginx
```

## Monitoring and Maintenance

### Log Management
```bash
# View application logs
tail -f /var/log/riget_zoo/gunicorn_supervisor.log

# View Nginx logs
tail -f /var/log/nginx/riget_zoo.access.log
tail -f /var/log/nginx/riget_zoo.error.log

# Django logs
tail -f /home/riget_zoo/Riget-Zoo-Adventures/zoo/django.log
```

### Backup Strategy
```bash
# Database backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="riget_zoo_production"

pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
```

### Health Checks
```bash
# Create health check endpoint in Django
# Add to urls.py
path('health/', health_check, name='health'),

# Health check view
def health_check(request):
    return JsonResponse({'status': 'healthy', 'timestamp': timezone.now()})
```

### Performance Monitoring
Consider implementing:
- **Sentry** for error tracking
- **New Relic** or **DataDog** for performance monitoring
- **Uptime monitoring** services
- **Database query optimization**

## Troubleshooting

### Common Issues
1. **Static files not loading**: Check STATIC_ROOT and collectstatic
2. **Database connection errors**: Verify credentials and network access
3. **502 Bad Gateway**: Check Gunicorn process and socket file permissions
4. **SSL certificate issues**: Verify domain configuration and renewal

### Debug Commands
```bash
# Check Django configuration
python manage.py check --settings=zoo.settings_production

# Test database connection
python manage.py dbshell --settings=zoo.settings_production

# Check static files
python manage.py findstatic admin/css/base.css --settings=zoo.settings_production
```

## Rollback Procedures

### Quick Rollback
```bash
# Rollback to previous git commit
git reset --hard HEAD~1
sudo supervisorctl restart riget_zoo

# Rollback database migration
python manage.py migrate app_name previous_migration_number --settings=zoo.settings_production
```

## Scaling Considerations

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple application servers
- Database replication
- Redis for session storage
- Static file CDN

### Vertical Scaling
- Increase server resources
- Database optimization
- Connection pooling
- Caching strategies

---

**Last Updated**: October 2025

For deployment support, refer to our [Troubleshooting Guide](TROUBLESHOOTING.md) or contact the development team.