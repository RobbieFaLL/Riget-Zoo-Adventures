# README - Management Directory

## Overview
The `management` directory in the Riget Zoo Adventures project is responsible for handling administrative and background processes.

## Directory Structure
```
management/
│── __init__.py         # Package marker
```

## Features
- Can be used to define custom Django management commands.
- Supports automated scripts for database maintenance, user management, etc.

## Setup
Ensure `management` is recognized by Django by placing it inside an installed app:
```python
INSTALLED_APPS = [
    ...
    'pages',
    'zoo',
    ...
]
```

## Contribution
- Add custom management commands under `management/commands/`.
- Ensure new commands are tested and documented properly.

## License
This project is licensed under the MIT License.

