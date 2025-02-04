# README - devstatic Directory

## Overview
The `devstatic` directory contains static assets such as JavaScript, CSS, and images used in the Riget Zoo Adventures project. These files are essential for styling, interactivity, and visual content within the application.

## Directory Structure
```
devstatic/
│── images/        # Directory for storing image assets
│── booking.js     # JavaScript for booking functionality
│── cal.js         # JavaScript for the calendar system
│── login.js       # JavaScript for login interactions
│── styles.css     # Main CSS file for site-wide styling
```

## Features
- **CSS (`styles.css`)**: Defines the overall appearance of the website, including layout, colors, and responsive design.
- **JavaScript (`booking.js`, `cal.js`, `login.js`)**: Provides interactivity for various features like booking, calendar display, and login handling.
- **Images (`images/`)**: Contains graphical assets for use in the templates.

## Usage
- CSS files are linked in the HTML templates using `{% static %}`:
  ```html
  <link rel="stylesheet" href="{% static 'styles.css' %}">
  ```
- JavaScript files are included in templates where needed:
  ```html
  <script src="{% static 'cal.js' %}"></script>
  ```
- Images can be used in templates like this:
  ```html
  <img src="{% static 'images/example.jpg' %}" alt="Example Image">
  ```

## Contribution Guidelines
- Keep styles organized and modular.
- Minify JavaScript and CSS files where possible for better performance.
- Store only essential images to optimize loading times.

## License
This project is licensed under the MIT License.