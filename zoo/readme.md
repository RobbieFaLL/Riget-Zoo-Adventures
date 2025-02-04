# README - Riget Zoo Adventures (Zoo Directory)

## Overview
The `zoo` directory is the main Django project folder for Riget Zoo Adventures. It contains project-wide configurations, settings, and static files.

## Directory Structure
```
zoo/
│── __init__.py         # Package marker
│── asgi.py             # ASGI entry point
│── settings.py         # Project settings and configurations
│── urls.py             # Global URL routing
│── wsgi.py             # WSGI entry point
│── db.sqlite3          # SQLite database (for development)
│── manage.py           # Django management commands
│── devstatic/          # Static files (CSS, JS, Images)
│   ├── images/        # Image assets
│   ├── booking.js     # JavaScript for booking functionality
│   ├── cal.js         # JavaScript for calendar functionality
│   ├── login.js       # JavaScript for login functionality
│   ├── styles.css     # Stylesheet for the website
```

## Features
- Global Django settings and URL routing.
- Contains static files for frontend styling and interactivity.
- Manages ASGI and WSGI configurations for deployment.

## Setup
Ensure all dependencies are installed using:
```sh
pip install -r requirements.txt
```
Run the server:
```sh
python manage.py runserver
```

## Contribution
- Modify `settings.py` for project-wide changes.
- Update `urls.py` for global routing.
- Store static assets in `devstatic/`.

## License
This project is licensed under the MIT License.

