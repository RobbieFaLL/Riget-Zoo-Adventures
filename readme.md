# Riget Zoo Adventures

## Overview
Riget Zoo Adventures is a Django-based web application that provides information about the zoo, allows users to book visits, and view events. The project includes authentication, a calendar for opening times, and various informational pages.

## Features
- **User Authentication:** Signup, login, and logout functionalities.
- **Booking System:** Allows users to book visits online.
- **Events Calendar:** Displays zoo events and opening times.
- **Informational Pages:** About, animals, conservation, and visiting details.
- **Interactive UI:** Built with Django templates, Bootstrap, and JavaScript.

## Installation
### Prerequisites
Ensure you have Python and Django installed.
```bash
pip install -r requirements.txt
```

### Running the Project
```bash
python manage.py runserver
```
Access the site at `http://127.0.0.1:8000/`

## Project Structure

| Directory / File            | Description |
|----------------------------|-------------|
| `zoo/`                     | Project root directory |
| ├── `env/`                 | Virtual environment (not included in repo) |
| ├── `management/`          | Django management commands (if any) |
| ├── `pages/`               | Main Django app containing views and models |
| │   ├── `migrations/`       | Django migrations for database changes |
| │   ├── `__init__.py`      | Marks the directory as a package |
| │   ├── `admin.py`         | Django admin configuration |
| │   ├── `apps.py`          | App configuration |
| │   ├── `models.py`        | Database models |
| │   ├── `tests.py`         | Unit tests |
| │   ├── `urls.py`          | URL routing |
| │   ├── `views.py`         | Application logic and views |
| ├── `templates/`           | HTML templates for the site |
| │   ├── `about.html`       | About page |
| │   ├── `animals.html`     | Animal information page |
| │   ├── `base.html`        | Base template for page structure |
| │   ├── `Booking_Success.html` | Booking confirmation page |
| │   ├── `booking.html`     | Booking form page |
| │   ├── `calendar.html`    | Calendar view for opening times |
| │   ├── `conservation.html`| Conservation efforts page |
| │   ├── `events.html`      | Zoo events page |
| │   ├── `index.html`       | Homepage |
| │   ├── `login.html`       | User login page |
| │   ├── `logout.html`      | User logout confirmation |
| │   ├── `signup.html`      | Signup page |
| │   ├── `visit.html`       | Visiting information |
| ├── `devstatic/`           | Static files directory |
| │   ├── `images/`          | Contains images for the site |
| │   ├── `booking.js`       | JavaScript for booking functionality |
| │   ├── `cal.js`           | JavaScript for calendar functionality |
| │   ├── `login.js`         | JavaScript for login interactions |
| │   ├── `styles.css`       | Main stylesheet for the site |
| ├── `zoo/`                 | Django project settings directory |
| │   ├── `__init__.py`      | Marks directory as a package |
| │   ├── `asgi.py`          | ASGI application config |
| │   ├── `settings.py`      | Django settings |
| │   ├── `urls.py`          | Project URL routing |
| │   ├── `wsgi.py`          | WSGI application config |
| ├── `db.sqlite3`           | SQLite database file |
| ├── `manage.py`            | Django management script |
| ├── `requirements.txt`     | List of dependencies |
| ├── `.gitignore`           | Files and directories to ignore in Git |

## Usage
- Navigate to the homepage and explore the available pages.
- Sign up or log in to make a booking.
- View the events calendar to see upcoming zoo events and opening hours.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

---
For any inquiries, contact [Your Email or Project Contact Info].

