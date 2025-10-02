# Contributing to Riget Zoo Adventures

Thank you for your interest in contributing to Riget Zoo Adventures! We welcome contributions from the community and appreciate your help in making this project better.

## Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Contribution Process](#contribution-process)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Django framework
- SQLite (included with Python)

### Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Riget-Zoo-Adventures.git
   cd Riget-Zoo-Adventures
   ```

2. **Set Up Virtual Environment**
   ```bash
   cd zoo
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep line length under 88 characters (Black formatter standard)
- Use type hints where appropriate

### Django Specific Guidelines
- Follow Django's coding style conventions
- Use Django's built-in validators when possible
- Keep models simple and focused
- Use proper URL naming conventions
- Follow Django's template conventions

### HTML/CSS Guidelines
- Use semantic HTML elements
- Follow consistent indentation (2 spaces)
- Use descriptive class names
- Ensure accessibility standards are met

### Example Code Format
```python
from django.db import models
from django.core.exceptions import ValidationError


class ExampleModel(models.Model):
    """
    Example model demonstrating proper code style.
    """
    name = models.CharField(max_length=100, help_text="Enter the name")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        """Validate model data."""
        super().clean()
        if not self.name.strip():
            raise ValidationError({"name": "Name cannot be empty"})

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Examples"
```

## Contribution Process

### 1. Choose an Issue
- Look for issues labeled `good first issue` for beginners
- Check if the issue is already assigned
- Comment on the issue to express your interest

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Your Changes
- Write clean, well-documented code
- Follow the coding standards above
- Test your changes thoroughly
- Update documentation if necessary

### 4. Commit Your Changes
```bash
git add .
git commit -m "Add feature: brief description of changes"
```

**Commit Message Guidelines:**
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally

### 5. Push and Create Pull Request
```bash
git push origin your-branch-name
```

Create a pull request with:
- Clear title and description
- Reference to related issues
- Screenshots if UI changes are involved
- List of changes made

## Testing

### Running Tests
```bash
python manage.py test
```

### Writing Tests
- Write unit tests for new models and views
- Include edge cases in your tests
- Aim for good test coverage
- Test both success and failure scenarios

### Test Example
```python
from django.test import TestCase
from django.urls import reverse
from management.models import CustomUser


class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test that a user is created successfully."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
```

## Documentation

### Updating Documentation
- Update README.md if installation steps change
- Add docstrings to new functions and classes
- Update API documentation for new endpoints
- Include examples in your documentation

### Code Comments
- Explain complex business logic
- Document non-obvious code decisions
- Avoid obvious comments
- Keep comments up to date with code changes

## Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Be Helpful
- Help newcomers get started
- Share knowledge and resources
- Provide constructive feedback
- Be patient with questions

### Quality Standards
- Ensure your code works before submitting
- Test edge cases
- Follow the project's coding standards
- Write meaningful commit messages

## Questions and Support

If you have questions or need help:
- Check existing issues and documentation first
- Open a new issue for bugs or feature requests
- Use clear, descriptive titles
- Provide as much context as possible

## Recognition

Contributors will be recognized in our README.md file and release notes. We appreciate all contributions, whether they're code, documentation, bug reports, or suggestions!

Thank you for contributing to Riget Zoo Adventures! 🦁🐘🦒