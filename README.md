# Student Management REST API

A production-ready, secure RESTful API built with **Django** and **Django REST Framework (DRF)** for managing student records. The API features **JWT authentication**, **row-level user data isolation**, **advanced filtering and search**, and dual-database support (**PostgreSQL** & **SQLite**).

---

## Table of Contents

- [Features](#features)
- [Security & GitHub Best Practices](#security--github-best-practices)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create and Activate Virtual Environment](#2-create-and-activate-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Generate Secret Key & Configure Environment Variables](#4-generate-secret-key--configure-environment-variables)
  - [5. Run Migrations](#5-run-migrations)
  - [6. Create a Superuser (Optional)](#6-create-a-superuser-optional)
  - [7. Start the Development Server](#7-start-the-development-server)
- [Alternative: Running with SQLite](#alternative-running-with-sqlite)
- [Environment Variables](#environment-variables)
- [Pre-Push Security Checklist](#pre-push-security-checklist)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Student Endpoints](#student-endpoints)
- [Querying, Filtering, and Pagination](#querying-filtering-and-pagination)
- [Permission and Ownership Model](#permission-and-ownership-model)
- [Running Tests](#running-tests)
- [License](#license)

---

## Features

- **JWT Authentication**: Secure user registration, token generation, and token refresh using `djangorestframework-simplejwt`.
- **Data Isolation & Row-Level Permissions**:
  - Regular users can only create, view, update, and delete their own assigned student records.
  - Staff / Admin users (`is_staff=True`) have global administrative access to all records.
- **Robust Field Validation**:
  - Validates student name (non-empty, whitespace stripped).
  - Enforces unique email addresses across students and users.
  - Restricts student age between 1 and 120 with dual model and serializer validators.
  - Enforces Django's built-in password complexity validators during registration.
- **Search, Filter & Sorting**:
  - Case-insensitive search on `name` and `email`.
  - Filter by age: exact, greater than or equal to (`gte`), and less than or equal to (`lte`).
  - Sort results by `name`, `age`, or `created_at` (default: newest first `-id`).
- **Pagination**: Built-in `PageNumberPagination` (10 items per page).
- **Dual Database Flexibility**: Configured for PostgreSQL by default with an included standalone SQLite configuration for effortless local development and testing.

---

## Security & GitHub Best Practices

> [!IMPORTANT]
> **No Secrets or Credentials in Version Control**
> - **Never commit `.env` or any production secrets to GitHub.**
> - This repository includes `.env.example` as a template with placeholder values.
> - The `.gitignore` file is configured to exclude `.env`, local database files (`db.sqlite3`, `sqlite_data.json`), and virtual environments.
> - Generate a unique `DJANGO_SECRET_KEY` on each deployment or local machine.

---

## Tech Stack

- **Backend Framework**: [Django 6.x](https://www.djangoproject.com/)
- **API Toolkit**: [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- **Authentication**: [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- **Filtering**: [django-filter](https://django-filter.readthedocs.io/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) (via `psycopg 3`) / [SQLite](https://www.sqlite.org/)
- **Environment Management**: [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## Project Architecture

```
student_api_project/
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── asgi.py              # ASGI configuration for deployment
│   ├── settings.py          # Main settings (PostgreSQL, JWT, DRF config)
│   ├── settings_sqlite.py   # Alternative SQLite settings for local dev
│   ├── urls.py              # Root routing (/admin/ and /api/)
│   └── wsgi.py              # WSGI configuration for deployment
├── students/                # Main application package
│   ├── migrations/          # Database migrations
│   ├── admin.py             # Admin panel registrations
│   ├── apps.py              # App configuration
│   ├── models.py            # Student model definition
│   ├── serializers.py       # Student ModelSerializer & field validators
│   ├── users_serializers.py # User registration serializer & validations
│   ├── urls.py              # API routes (Auth & Student ViewSet)
│   ├── views.py             # RegisterView & StudentViewSet logic
│   └── tests.py             # Unit and integration tests
├── .env.example             # Safe template for environment variables (committed)
├── .gitignore               # Excludes secrets, cache, and virtual environment
├── manage.py                # Django CLI utility
├── README.md                # Project documentation
└── requirements.txt         # Project dependencies
```

---

## Prerequisites

- **Python**: Version `3.10` or higher
- **PostgreSQL**: Installed and running (or use SQLite mode)
- **Git**: Installed for version control

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/student_api_project.git
cd student_api_project
```

### 2. Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Secret Key & Configure Environment Variables

1. Copy `.env.example` to create your local `.env` file:

   ```bash
   # Windows
   copy .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```

2. Generate a secure, unique Django secret key using Python:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. Open `.env` and paste your generated secret key along with your local PostgreSQL credentials:

   ```env
   # Your generated secret key (keep this private!)
   DJANGO_SECRET_KEY=paste_generated_key_here

   # PostgreSQL Database Configuration
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

> [!NOTE]
> Make sure the PostgreSQL database (e.g. `your_database_name`) is created in your database server before applying migrations.

### 5. Run Migrations

Apply the database schema migrations:

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To access the Django Admin interface at `/admin/`:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter a username, email, and password.

### 7. Start the Development Server

```bash
python manage.py runserver
```

The API will now be running at `http://127.0.0.1:8000/`.

---

## Alternative: Running with SQLite

If you want a zero-setup local run without installing or starting PostgreSQL:

```bash
# 1. Run migrations on SQLite
python manage.py migrate --settings=config.settings_sqlite

# 2. Start server with SQLite
python manage.py runserver --settings=config.settings_sqlite
```

---

## Environment Variables

All sensitive values are loaded from environment variables using `python-dotenv`:

| Variable | Required | Description | Example / Default |
| :--- | :---: | :--- | :--- |
| `DJANGO_SECRET_KEY` | Yes | Unique cryptographic key for Django session/signing. | *(Generated locally)* |
| `DB_NAME` | Yes | Name of the PostgreSQL database. | `student_api_db` |
| `DB_USER` | Yes | PostgreSQL user account. | `postgres` |
| `DB_PASSWORD` | Yes | PostgreSQL user password. | *(Your local password)* |
| `DB_HOST` | No | PostgreSQL host address. | `localhost` |
| `DB_PORT` | No | PostgreSQL port. | `5432` |

---

## Pre-Push Security Checklist

Before pushing this repository to GitHub, verify that no confidential files are staged:

```bash
# Check git status
git status
```

Confirm that:
- [x] `.env` is **NOT** listed in staged or untracked files (it must be ignored by `.gitignore`).
- [x] `db.sqlite3` is **NOT** listed in staged or untracked files.
- [x] Only safe template files like `.env.example` and `README.md` are being tracked.

---

## API Endpoints

Base URL: `http://127.0.0.1:8000/api/`

### Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `POST` | `/api/auth/register/` | No | Register a new user account. |
| `POST` | `/api/auth/token/` | No | Obtain JWT pair (`access` and `refresh` tokens). |
| `POST` | `/api/auth/token/refresh/` | No | Refresh an expired access token using the refresh token. |

#### 1. Register a New User
- **URL**: `POST /api/auth/register/`
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "password": "StrongPassword123!"
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com"
  }
  ```

#### 2. Obtain JWT Token (Login)
- **URL**: `POST /api/auth/token/`
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "password": "StrongPassword123!"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "refresh": "<refresh_token_string>",
    "access": "<access_token_string>"
  }
  ```

#### 3. Refresh Access Token
- **URL**: `POST /api/auth/token/refresh/`
- **Request Body**:
  ```json
  {
    "refresh": "<refresh_token_string>"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "access": "<new_access_token_string>"
  }
  ```

---

### Student Endpoints

All student endpoints require authentication. Include the access token in the `Authorization` header:

```http
Authorization: Bearer <your_access_token>
```

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :---: | :--- |
| `GET` | `/api/students/` | Bearer Token | List all students belonging to the user (paginated). |
| `POST` | `/api/students/` | Bearer Token | Create a new student (automatically assigned to caller). |
| `GET` | `/api/students/{id}/` | Bearer Token | Retrieve student details by ID. |
| `PUT` | `/api/students/{id}/` | Bearer Token | Update all fields of a student. |
| `PATCH` | `/api/students/{id}/` | Bearer Token | Partially update student fields. |
| `DELETE` | `/api/students/{id}/` | Bearer Token | Delete a student. |

#### 1. Create a Student
- **URL**: `POST /api/students/`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "name": "Alice Smith",
    "email": "alice.smith@university.edu",
    "age": 21
  }
  ```
- **Response** (`201 Created`):
  ```json
  {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice.smith@university.edu",
    "age": 21,
    "owner": 1,
    "created_at": "2026-11-04T12:00:00Z",
    "updated_at": "2026-11-04T12:00:00Z"
  }
  ```

#### 2. List Students
- **URL**: `GET /api/students/`
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response** (`200 OK`):
  ```json
  {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Alice Smith",
        "email": "alice.smith@university.edu",
        "age": 21,
        "owner": 1,
        "created_at": "2026-11-04T12:00:00Z",
        "updated_at": "2026-11-04T12:00:00Z"
      }
    ]
  }
  ```

#### 3. Update a Student
- **URL**: `PATCH /api/students/1/`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "age": 22
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice.smith@university.edu",
    "age": 22,
    "owner": 1,
    "created_at": "2026-11-04T12:00:00Z",
    "updated_at": "2026-11-04T12:05:00Z"
  }
  ```

#### 4. Delete a Student
- **URL**: `DELETE /api/students/1/`
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**: `204 No Content`

---

## Querying, Filtering, and Pagination

The `GET /api/students/` endpoint supports query parameters for searching, filtering, and ordering:

### 1. Search
Search by `name` or `email` (case-insensitive substring match):
```http
GET /api/students/?search=alice
GET /api/students/?search=university.edu
```

### 2. Age Filtering
Filter records by student age using exact match or numeric boundaries:
- **Exact match**: `GET /api/students/?age=20`
- **Greater than or equal (`gte`)**: `GET /api/students/?age__gte=18`
- **Less than or equal (`lte`)**: `GET /api/students/?age__lte=25`
- **Range (Combined)**: `GET /api/students/?age__gte=18&age__lte=25`

### 3. Ordering
Sort results by `name`, `age`, or `created_at`. Prepend with `-` for descending order:
- **Sort by age (ascending)**: `GET /api/students/?ordering=age`
- **Sort by age (descending)**: `GET /api/students/?ordering=-age`
- **Sort by creation date**: `GET /api/students/?ordering=-created_at`

### 4. Pagination
Navigate pages with the `page` query parameter (default page size is 10):
```http
GET /api/students/?page=2
```

---

## Permission and Ownership Model

| User Role | Permissions |
| :--- | :--- |
| **Anonymous User** | Access only to `/api/auth/register/`, `/api/auth/token/`, and `/api/auth/token/refresh/`. |
| **Standard Authenticated User** | Can create students (automatically set as `owner`). Can view, update, and delete **only their own** students. |
| **Staff / Admin User (`is_staff=True`)** | Has administrative visibility over **all** students in the database regardless of owner. |

---

## Running Tests

Execute the test suite using Django's test runner:

```bash
# Standard test run
python manage.py test

# Run tests using SQLite settings
python manage.py test --settings=config.settings_sqlite
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).
