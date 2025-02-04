# Riget Zoo Adventures

## Overview
**Riget Zoo Adventures** is a Django-based web application that provides visitors with essential zoo information, including:
- Animal exhibits
- Upcoming events
- Conservation efforts
- Online booking system for visits and activities

## Directory Structure
```
Riget Zoo Adventures/
│── zoo/                     # Main Django application directory
│── .gitignore               # Git ignore file
│── readme.md                # Project documentation
│── Task1_Test_Strategy_Template.doc  # Test strategy document
│── Task2_Test_Log_Template.doc       # Test log document
│── W76777-T-Level-Documents/         # Additional documentation files
```

### Key Components
- **`zoo/`** - Contains Django applications and configurations.
- **`.gitignore`** - Specifies files and directories to be ignored by Git.
- **`readme.md`** - Project documentation.
- **Testing Documents** - Includes testing strategy and logging templates.

## Installation
Follow these steps to set up the project:

1. **Clone the repository**  
   ```sh
   git clone https://github.com/yourusername/riget-zoo-adventures.git
   ```
2. **Navigate into the project directory**  
   ```sh
   cd riget-zoo-adventures
   ```
3. **Create and activate a virtual environment**  
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
4. **Install dependencies**  
   ```sh
   pip install -r zoo/requirements.txt
   ```
5. **Apply database migrations**  
   ```sh
   python zoo/manage.py migrate
   ```
6. **Start the development server**  
   ```sh
   python zoo/manage.py runserver
   ```

## Usage
- Open **[`http://127.0.0.1:8000/`](http://127.

