# README - Pages App

## Overview
The `pages` app in the Riget Zoo Adventures project handles the core functionality of the website, including views, models, and URL routing for various pages.

## Directory Structure
```
pages/
│── migrations/          # Django migrations
│── __init__.py         # Package marker
│── admin.py            # Admin panel configurations
│── apps.py             # Django app configuration
│── models.py           # Database models
│── tests.py            # Unit tests
│── urls.py             # URL routing for the app
│── views.py            # View functions and class-based views
```

## Features
- Handles user navigation across various pages.
- Manages bookings, events, and other interactive features.
- Implements authentication and user-related functionality.

## Setup
Ensure the app is installed in `INSTALLED_APPS` inside `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'pages',
    ...
]
```

## Usage
This app controls the routing and rendering of various views defined in `views.py`. Modify `urls.py` to add new routes or update existing ones.

## Contribution
- Add new views in `views.py`.
- Register new models in `models.py` and run migrations.
- Modify `urls.py` to update routing.

## License
This project is licensed under the MIT License.

