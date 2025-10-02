# Changelog

All notable changes to Riget Zoo Adventures will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Comprehensive documentation suite (CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md)
- Project structure documentation
- Development environment setup guides

### Changed
- Updated README.md with better installation instructions

### Security
- Added security policy and vulnerability reporting guidelines

## [1.0.0] - 2025-10-02
### Added
- Initial release of Riget Zoo Adventures
- Django-based web application for zoo management
- User authentication system with custom user model
- Booking system for zoo visits and activities
- Event management functionality
- Opening hours management with dynamic scheduling
- Closed days management
- Animal exhibits information
- Conservation efforts page
- Responsive web design with Bootstrap integration
- Admin panel for content management
- SQLite database for development
- Virtual environment support
- Requirements.txt for dependency management

#### Features
- **User Management**
  - Custom user model with phone number field
  - Email or username authentication
  - User registration and login system
  - Phone number validation (minimum 11 digits)

- **Booking System**
  - Online booking form for zoo visits
  - Date and time selection
  - Customer information collection
  - Booking confirmation system

- **Schedule Management**
  - Dynamic opening hours with predefined time slots
  - Visual color coding for different schedules:
    - Green: 10:00 AM - 6:00 PM
    - Orange: 10:00 AM - 5:00 PM
    - Blue: 9:00 AM - 5:00 PM
    - Purple: 9:00 AM - 6:00 PM
    - Crimson: 9:00 AM - 9:00 PM
  - Closed days management with reasons
  - Bulk schedule updates

- **Event Management**
  - Event creation and management
  - Start and end time tracking
  - Event descriptions and locations
  - Chronological event ordering

- **Web Pages**
  - Home page with zoo overview
  - Animals page showcasing exhibits
  - Events page with upcoming activities
  - Conservation page highlighting efforts
  - Visit page with practical information
  - About page with zoo information
  - Booking page for online reservations

#### Technical Stack
- **Backend**: Django 5.1.3
- **Database**: SQLite (development)
- **Authentication**: Django Allauth 65.3.1
- **Frontend**: HTML5, CSS3, Bootstrap
- **Additional Libraries**:
  - Django REST Framework 3.15.2
  - Django CORS Headers 4.6.0
  - Django CKEditor 6.7.1
  - Pillow 11.0.0 for image handling
  - Pandas 2.2.3 for data processing

#### Project Structure
```
zoo/
├── management/          # User management and booking app
├── pages/              # Static pages app
├── templates/          # HTML templates
├── zoo/               # Main project configuration
├── db.sqlite3         # Database file
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

### Security
- CSRF protection enabled
- Secure password validation
- Debug mode configured for development
- Secret key management
- User input validation

### Development
- Virtual environment setup
- Development server configuration
- Static files handling
- Django admin interface
- Database migrations
- Custom authentication backends

## Types of Changes
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

## Release Notes

### Version 1.0.0 - "Initial Launch"
This is the first stable release of Riget Zoo Adventures, providing a complete web-based zoo management system. The application offers visitors essential information about the zoo, including animal exhibits, upcoming events, and conservation efforts, along with a convenient online booking system.

#### Key Highlights
- Full-featured Django web application
- User-friendly booking system
- Dynamic schedule management
- Responsive design for all devices
- Comprehensive admin interface
- Secure user authentication
- Event and content management

#### Next Steps
- Enhanced mobile experience
- Payment integration for bookings
- Email notification system
- Advanced reporting features
- Multi-language support
- API development for mobile apps

---

## Contributing to the Changelog

When contributing to the project, please update this changelog following these guidelines:

1. **Add entries to the [Unreleased] section** for new changes
2. **Use the correct category**: Added, Changed, Deprecated, Removed, Fixed, Security
3. **Write clear, concise descriptions** of changes
4. **Include relevant links** to issues or pull requests
5. **Move entries to a new version section** when releasing

### Example Entry Format
```markdown
### Added
- New feature description [#123](https://github.com/user/repo/pull/123)
- Another feature with more details about implementation

### Fixed
- Bug fix description [#456](https://github.com/user/repo/issues/456)
- Another bug fix with context
```

---

**Last Updated**: October 2, 2025

For more information about releases, visit our [GitHub Releases](https://github.com/RobbieFaLL/Riget-Zoo-Adventures/releases) page.