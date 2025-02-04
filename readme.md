Here's your `README.md` in proper Markdown format:  

```md
# Riget Zoo Adventures

## Overview
Riget Zoo Adventures is a Django-based web application designed to provide visitors with information about the zoo, including events, animals, conservation efforts, and an online booking system.

## Directory Structure
```
Riget Zoo Adventures/
│── zoo/                   # Main Django application directory
│── .gitignore             # Git ignore file
│── readme.md              # Project documentation
│── Task1_Test_Strategy_Template.doc  # Test strategy document
│── Task2_Test_Log_Template.doc       # Test log document
│── W76777-T-Level-Documents/         # Additional documentation files
```

### Key Components
- **`zoo/`** - The main Django project directory containing all applications and configurations.
- **`.gitignore`** - Specifies files and directories to be ignored by Git.
- **`readme.md`** - Project documentation file.
- **Testing Documents** - Includes strategy and logging templates for software testing.

## Installation
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
5. **Run database migrations**  
   ```sh
   python zoo/manage.py migrate
   ```
6. **Start the development server**  
   ```sh
   python zoo/manage.py runserver
   ```

## Usage
- Visit **[`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)** in a web browser to explore the site.
- Access the Django admin panel at **`/admin/`** (requires superuser credentials).
- Use the booking system to reserve tickets online.

## Contribution
- Fork the repository and create a new branch for changes.
- Submit pull requests for review.
- Ensure all contributions follow Django best practices.

## License
This project is licensed under the **MIT License**.
```

Would you like to add any additional sections? 🚀