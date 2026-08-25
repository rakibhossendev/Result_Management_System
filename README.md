# Result Management System

A school result management system built with Flask. This application implements three user roles (Admin, Principal, Teacher) and provides administrative workflows for managing principals, teachers, departments, subjects, students, attendance, and marks topics.

## Overview

The project is a Flask-based web application organized with Blueprints and SQLAlchemy models. It is designed to support:

- Admin dashboard to manage principals
- Principal dashboard to manage teachers, departments, subjects, and curriculum
- Teacher dashboard to manage students, attendance, and marks topics
- Session-based login with role-aware navigation

> Note: This project is currently incomplete and requires additional refinement. The README is based on the current code state.

## Technology Stack

- Python 3
- Flask
- Flask SQLAlchemy
- Flask-WTF / WTForms
- SQLite (default)

## Installation

1. Create a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Important: The current `requirements.txt` file does not list all code dependencies. Add the following packages if missing:
>
> - `Flask-WTF`
> - `WTForms`
> - `Flask-SQLAlchemy`
>
> Then run:
>
> ```bash
> pip install Flask-WTF WTForms Flask-SQLAlchemy
> ```

3. Run the app:

```bash
python run.py
```

The app creates the database automatically when started.

## Configuration

Configuration is loaded from `app/config.py`.

- `SECRET_KEY`: used for session security
- `SQLALCHEMY_DATABASE_URI`: database connection string

Default values are:

- `SECRET_KEY = 'your-secret-key'`
- `SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'`

For production, set environment variables:

```bash
export SECRET_KEY='your-secret-key'
export DATABASE_URL='sqlite:///database.db'
```

## Run the Application

Start the server with:

```bash
python run.py
```

Then visit:

- `http://127.0.0.1:5000/` for the home page
- `http://127.0.0.1:5000/login` for login

## Default Login

The app currently uses a hard-coded admin account in `app/routes/auth/login.py`:

- username: `admin`
- password: `admin123`

Principal and teacher users must be created from the admin and principal dashboards.

## User Roles and Flows

### Admin

- Login with the default admin account
- Add new principals
- View principals
- Edit principal profile
- Delete principals

### Principal

- Login after being created by the admin
- Select a shift (Morning or Day)
- Add teachers
- View teachers
- Edit or delete teachers
- Manage departments
- Add subjects
- Assign subjects to departments and semesters
- View departments and subjects

### Teacher

- Login after being created by a principal
- Add students
- View student lists
- Record and save attendance
- Manage marks topics

## Project Structure

Key files and directories:

- `run.py` — application entrypoint
- `app/__init__.py` — Flask app factory and Blueprint registration
- `app/config.py` — configuration settings
- `app/extensions.py` — SQLAlchemy initialization
- `app/models/` — database models for Admin, Principal, Teacher, Student, Departments, Subjects, Curriculum, Attendance, and Marks Topics
- `app/routes/` — blueprint route handlers split by role
- `app/utils/` — form definitions
- `templates/` — HTML templates for each role
- `static/` — CSS and JS assets

## How To Use The AI Features

The app includes an AI assistant that helps teachers query student data through conversation (e.g., "Show me student 322053's details" or "What's the attendance for group B?").

### Setup (One-time)

1. **Get a Mistral API key** (free):
   - Visit [console.mistral.ai](https://console.mistral.ai)
   - Sign up, go to **API Keys**, click **Create API Key**, and copy it

2. **Create `.env` file** in your project root (same folder as `run.py`):
   ```
   MISTRAL_API_KEY=your-key-here
   ```

### Using the Assistant

1. Start the app: `python run.py`
2. Log in as a teacher
3. Visit `http://localhost:5000/ask`
4. Ask questions like:
   - "Tell me about student 322053"
   - "What's the CGPA for student 322056?"

### Troubleshooting

| Error | Fix |
|-------|-----|
| "MISTRAL_API_KEY is not set" | Check your `.env` file exists and has the correct key |
| "401 Unauthorized" | Your API key is wrong; regenerate it at console.mistral.ai |
| "student not found" | Make sure the student exists in your teacher's class. And log in as the teacher. |

## Adding Sample Students For Testing Purpose

- Make a teacher with ID 01 and make sure your principal ID is 2006
- run `sqlite3 instance/database.db < import_students.sql` in your terminal

The shell command will load 45 students in the database. Now you can test AI features with this data or test the software.

## Known Issues and Review Notes

The current code contains some areas to improve before final release:

- Passwords are stored in plain text. Add password hashing with `werkzeug.security.generate_password_hash` and `check_password_hash`. - Problem Solved ✅
- Authentication logic in `app/routes/auth/login.py` is not fully robust and mixes principal and teacher login flows incorrectly.
- `requirements.txt` is incomplete and should include `Flask-WTF`, `WTForms`, and `Flask-SQLAlchemy`.
- Session management uses `session["temp_principal_id"]` and `session["principal_id"]`; verify principal/teacher workflows carefully.
- No unit tests are included.

## Future Improvements

- Add password hashing and stronger authentication - Done ✅
- Add input validation and error handling for all routes
- Create a proper registration flow for principals, teachers, and students
- Add a student-facing view for marks and attendance records
- Add tests for models, forms, and routes
- Add deployment instructions and production configuration

## Contribution

Once the project is complete, update this README with:

- full dependency list
- installation and usage steps for production
- new feature descriptions
- testing commands
- deployment guide

---

This document was created from the current project implementation and is ready to be updated as the app evolves.

## Authors

- Rakib Hossen
- Aronno Rahman Arpa
- Srestho