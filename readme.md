# 🧺 Riget Zoo Adventures

## 🌍 Overview
**Riget Zoo Adventures** is a Django-based web application designed to enhance the visitor experience at a zoo. It provides key features including:

- 🐾 Animal exhibits
- 🗕️ Upcoming events
- 🌱 Conservation efforts
- 🧾 Online booking system for visits and activities

---

## 📁 Directory Structure
```plaintext
riget-zoo-adventures/
│
├── zoo/                              # Main Django application
├── .gitignore                        # Git ignore rules
├── readme.md                         # Project overview and documentation
├── Task1_Test_Strategy_Template.doc  # Test strategy template
├── Task2_Test_Log_Template.doc       # Test log template
└── W76777-T-Level-Documents/         # Additional project documentation
```

### 🔑 Key Components
- **`zoo/`** – Django app logic and configuration.
- **`.gitignore`** – Files and folders to be excluded from version control.
- **`readme.md`** – Main documentation file.
- **Test Docs** – Templates for test strategy and logs to support project testing.

---

## ⚙️ Installation Guide

Follow these steps to set up and run the project locally:

1. **Clone the repository**  
   ```bash
   git clone https://github.com/RobbieFall/riget-zoo-adventures.git
   ```

2. **Navigate into the project folder**  
   ```bash
   cd riget-zoo-adventures
   ```

3. **Create and activate a virtual environment**  
   ```bash
   python -m venv env
   source env/bin/activate        # On Windows: env\Scripts\activate
   ```

4. **Install dependencies**  
   ```bash
   pip install -r zoo/requirements.txt
   ```

5. **Apply database migrations**  
   ```bash
   python zoo/manage.py migrate
   ```

6. **Run the development server**  
   ```bash
   python zoo/manage.py runserver
   ```

---

## 🚀 Usage

Once the server is running, open your browser and visit:

👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📚 Note

This project was created for **educational purposes only**, as part of my personal development ahead of my exams.

---

