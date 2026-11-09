# Result Management System

A role-based academic management system built with **Python, Flask, and SQLAlchemy**, designed to improve how Polytechnic institutions in Bangladesh manage academic information and how students access their results.

**Live Application:** [Result Management System](https://result-management-system-theta.vercel.app/)

**Test Student Roll:** `322112`

---

## About The Project

When I joined Polytechnic, I noticed a practical problem: Polytechnic students in Bangladesh have very limited options for accessing detailed academic results.

Usually, students receive their semester results as PDF files containing only their CGPA, without a convenient way to explore subject-wise marks, attendance, or other academic information.

Since I had been learning programming since Class 9, I started thinking about how this problem could be solved with software.

That idea became the foundation of this Result Management System.

Initially, I started building the application using the technologies I knew at that time: HTML, CSS, JavaScript, Bootstrap, Flask, SQLAlchemy, and SQL.

As the application grew, I encountered real-world challenges involving application architecture, authentication, authorization, database design, data security, and team collaboration.

This project gradually evolved into a role-based academic management system with four user roles:

**Admin → Principal → Teacher → Student**

Each role has specific responsibilities and access permissions, keeping academic operations organized and controlled.

---

## Key Features

- Four-level role-based access control (RBAC).
- Hierarchical account creation and management.
- Department, subject, and semester management.
- Teacher assignment and academic access restrictions.
- Student management.
- Attendance management.
- Topic-based marks management.
- CGPA updates through PDF uploads.
<!-- - AI-powered student information assistant. -->
- Session-based authentication.
- Password hashing for improved account security.
- Role-specific dashboards and navigation.

---

# User Roles & Features

## 1. Student Features

Students are the primary beneficiaries of this system. The application aims to make academic information more accessible and organized.

- **CGPA Information:** Access the latest CGPA information processed from uploaded result PDFs.
- **Roll-Based Identification:** Student records are associated with their unique roll numbers.
- **Academic Information:** Student academic records are maintained within the system.
- **Result Accessibility:** Reduces dependence on manually searching through PDF result files.

*Note: The availability of individual student dashboard features depends on the current implementation.*

## 2. Teacher Features

Teachers are responsible for managing student records and academic activities within their assigned academic scope.

### Student Management
- Add new students.
- View student lists.
- Manage student information.
- Organize students according to assigned academic groups.

### Attendance Management
- Record student attendance.
- Save attendance records.
- Manage attendance for assigned students.

### Marks Management
- Create and manage assessment topics.
- Organize marks according to individual assessment categories.
- Maintain structured academic assessment information.

For example, a Python Programming subject may contain:

| Assessment Topic | Marks |
|---|---:|
| Mid Term | 20 |
| Lab Report | 10 |
| Other Assessments | As configured |

<!-- ### AI Assistant
- Ask questions about student information using natural language.
- Retrieve student details using roll numbers.
- Query available academic information.
- Ask questions such as:
  - "Tell me about student 322053."
  - "What's the CGPA for student 322056?"
  - "What's the attendance for group B?"

The AI assistant uses the Mistral API to process natural-language questions. -->

### Academic Access Control
- Teachers are assigned to specific departments, subjects, and semesters.
- Access to student and academic data is restricted according to their assignments.

## 3. Principal Features

Principals manage the academic structure and teaching staff of their respective institutions.

### Teacher Management
- Create teacher accounts.
- View registered teachers.
- Edit teacher profiles.
- Delete teacher accounts.
- Manage teacher information.

### Department Management
- Create departments.
- View department information.
- Manage academic departments.

### Subject Management
- Add new subjects.
- View available subjects.
- Assign subjects to departments.
- Associate subjects with specific semesters.

### Academic Structure
- Select an institutional shift (Morning or Day).
- Organize departments, subjects, and semesters.
- Manage the academic structure required for teacher assignments.

### Controlled Account Management
- Create teacher accounts under the principal's authority.
- Maintain control over teacher account creation.
- Keep teacher management within the institutional hierarchy.

## 4. Admin Features

The Admin has the highest level of administrative control over the application.

### Principal Management
- Create new principal accounts.
- View all principals.
- Edit principal profiles.
- Delete principal accounts.

### CGPA Management
- Upload official Polytechnic result PDF files.
- Process student result information from uploaded PDFs.
- Match result records using student roll numbers.
- Update students' CGPA information.

This feature was introduced to solve a practical problem: students often receive their results in PDF format, so manually entering every student's CGPA would be unnecessarily time-consuming.

Instead, the Admin can upload the result PDF, and the application processes the available information.

---

# How The System Works

The application follows a controlled hierarchical workflow.

```text
                 ADMIN
                   |
          Creates Principals
                   |
                   v
                PRINCIPAL
                   |
       +-----------+-----------+
       |           |           |
   Departments  Subjects   Teachers
                   |
                   v
                TEACHER
                   |
          +--------+--------+
          |        |        |
       Students Attendance Marks Topics
          |
          v
        STUDENT
          |
    Academic Information
       & CGPA
```

### Step 1: Admin Creates Principals

The Admin logs into the administrative dashboard and creates Principal accounts.

This prevents unrestricted public registration of institutional administrators.

### Step 2: Principal Organizes Academic Structure

After logging in, the Principal selects an institutional shift and manages:

- Departments
- Subjects
- Semesters
- Teachers

Subjects are associated with their respective departments and semesters.

### Step 3: Teachers Manage Students

Teachers receive accounts from their respective Principals.

They can then add students and manage academic activities within their assigned departments, subjects, and semesters.

### Step 4: Teachers Manage Academic Records

Teachers maintain attendance records and organize assessment topics.

For example, instead of treating all marks as a single value, the system can organize assessments into individual topics such as Mid Term and Lab Report.

### Step 5: Admin Updates CGPA

The Admin uploads official result PDFs.

The application processes the result information and updates student CGPA records using roll numbers.

### Step 6: Students Access Academic Information

Students are identified through their roll numbers, and their academic information is maintained in the system.

---

# Authentication & Authorization

One of the biggest architectural challenges was designing a secure account creation process.

Initially, I considered allowing users to register themselves. However, unrestricted registration could result in fake or unauthorized institutional accounts.

To address this problem, I implemented a controlled account hierarchy:

- Admin creates Principal accounts.
- Principal creates Teacher accounts.
- Teachers create and manage Student records.

This approach keeps account creation under institutional control.

### Role-Based Access Control

Authentication alone is not enough to protect an academic management system.

A Teacher should not be able to access or modify another department's academic information.

To address this, teachers are associated with specific:

- Departments
- Subjects
- Semesters

The application uses these assignments to restrict access to relevant student records and academic information.

This was one of the most important lessons I learned while developing this project: **Authorization and data-level access control are just as important as authentication.**

### Password Security

Initially, passwords were stored in plain text. Later, I improved the authentication system by implementing password hashing using Werkzeug security utilities.

---

# AI-Powered Academic Assistant

The project includes an AI assistant that allows teachers to interact with available student information through natural-language questions.

**Technology:** Mistral API

Example queries:

- Tell me about student 322053.
- What's the CGPA for student 322056?
- What's the attendance for group B?

The goal is to make academic information easier to retrieve without requiring teachers to manually navigate multiple pages.

<!-- ### AI Assistant Setup

1. Create an API key from [Mistral Console](https://console.mistral.ai/).
2. Create a `.env` file in the project root.
3. Add your API key:

```env
MISTRAL_API_KEY=your-mistral-api-key
```

4. Restart the application.

The AI assistant can be accessed by an authenticated teacher through:

```text
http://localhost:5000/ask
```

--- -->

# Technology Stack

| Category | Technologies |
|---|---|
| Language | Python, JavaScript |
| Backend | Flask |
| Database ORM | SQLAlchemy, Flask-SQLAlchemy |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap |
| Forms & Validation | Flask-WTF, WTForms |
| Authentication | Flask Sessions, Werkzeug Security |
| AI Integration | Mistral API |
| Version Control | Git, GitHub |

---

# Project Structure

```text
Result_Management_System/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── admin.py
│   │   ├── principal.py
│   │   ├── teacher.py
│   │   ├── student.py
│   │   ├── department.py
│   │   ├── subject.py
│   │   └── ...
│   │
│   ├── routes/
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── principal/
│   │   ├── teacher/
│   │   └── ...
│   │
│   └── utils/
│
├── templates/
│
├── static/
│   ├── css/
│   └── js/
│
├── instance/
│
├── requirements.txt
├── run.py
├── import_students.sql
└── README.md
```

---

# Installation & Local Setup

Follow these steps to run the project on your local machine.

### Prerequisites

Make sure you have installed:

- Python 3
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/rakibhossendev/Result_Management_System.git
```

Navigate into the project directory:

```bash
cd Result_Management_System
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If any required dependencies are missing from `requirements.txt`, install them manually:

```bash
pip install Flask Flask-SQLAlchemy Flask-WTF WTForms python-dotenv
```

<!-- ### 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database.db
MISTRAL_API_KEY=your-mistral-api-key
``` -->

The Mistral API key is required only if you want to use the AI assistant.

Make sure the configuration in `app/config.py` reads the environment variables correctly.

### 5. Run the Application

```bash
python run.py
```

The application initializes the database automatically when started, according to its configured database setup.

### 6. Open the Application

Visit:

- Home: http://127.0.0.1:5000/
- Login: http://127.0.0.1:5000/login

## Run with Docker

Build the image from the project directory:

```bash
docker build -t result-management-system:dev .
```

Start a temporary container:

```bash
docker run --rm -p 5000:5000 result-management-system:dev
```

Open http://127.0.0.1:5000/ to use the application. This first run keeps the
SQLite database and uploaded PDFs inside the container, so `--rm` deletes them
when the container stops. Add persistent storage before using it with data.

---

# Testing The Application

You can explore the deployed application using the following student test roll:

**Test Student Roll:** `322112`

**Live Application:** [Open Result Management System](https://result-management-system-theta.vercel.app/)

*Note: A student roll number is not a login password. Use the credentials and login flow configured by the application.*

---

# Import Sample Students (Optional)

For local testing, you can import sample student records using the provided SQL file.

Before importing, make sure:

- A Teacher with ID `01` exists.
- The Principal ID is `2006`.
- The SQLite database has been initialized.

Run:

```bash
sqlite3 instance/database.db < import_students.sql
```

This imports 45 sample student records into the database.

---

# Challenges & Lessons Learned

Building this application was one of my biggest learning experiences.

I started the project without a complete understanding of application architecture, security, scalability, or modern web development practices.

During development, I learned about:

- Application Architecture and Flask Blueprints
- Authentication and Authorization
- Role-Based Access Control (RBAC)
- Database Design and Relationships
- Data-Level Access Restrictions
- Session Management
- Password Hashing
- Academic Data Management
- Requirements Analysis
- PDF-Based Data Processing
- AI API Integration
- Team Collaboration
- Real-World Problem Solving

I also learned that building a large application is not just about writing code. Understanding the problem, designing the architecture, managing responsibilities, and making the right technical decisions are equally important.

---

# Team Collaboration

This project was developed collaboratively.

- **Rakib Hossen** — Project Initiation, Backend Development, and Application Architecture.
- **Aronno Rahman Arpa** — Frontend Development and UI Implementation.
- **Srestho** — AI Agent Feature Development.

Working with other developers helped me understand the importance of communication, task distribution, collaboration, and maintaining a consistent application structure.

---

# Future Improvements

The project is still evolving. Some areas I would like to improve include:

- Complete student-facing academic dashboards.
- More comprehensive marks and attendance views.
- Stronger authentication and session management.
- Improved input validation and error handling.
- Automated testing for models, forms, and routes.
- More robust database management.
- Better production configuration and deployment.
- Improved documentation and code organization.

---

# What I Would Do Differently Today

When I started this project, I did not have much experience with modern web technologies or large application architecture.

Today, after learning Next.js, React.js, TypeScript, and Tailwind CSS, I have a much better understanding of how I would approach the same application.

I would pay more attention to:

- Separation of business logic and UI components.
- Scalable backend architecture.
- Database design and optimization.
- Secure authentication and authorization.
- API design and maintainability.
- Reusable components and clean code.

This project started as an idea to solve a problem I personally noticed as a Polytechnic student.

Eventually, it became much more than a programming project. It taught me how real-world software problems are identified, analyzed, designed, solved, and continuously improved.

---

# Authors

- [Rakib Hossen](https://github.com/rakibhossendev)
- [Aronno Rahman Arpa](https://github.com/AronnoRahmanArpa)
- Srestho

**GitHub Repository:** [Result Management System](https://github.com/rakibhossendev/Result_Management_System)

**Live Application:** [https://result-management-system-theta.vercel.app/](https://result-management-system-theta.vercel.app/)
