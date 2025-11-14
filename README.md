# Django Banking Application

A Django web application for managing banks and branches with user authentication and profile management.

## Features

- **User Authentication**: Register, login, and logout functionality
- **Profile Management**: View and edit user profiles with password change support
- **Bank Management**: Create and view banks with details
- **Branch Management**: Create, view, and edit bank branches
- **JSON API**: RESTful JSON endpoints for branch information
- **Access Control**: Proper authentication and authorization for protected endpoints

## Requirements

- Python 3.9 or later
- Django 4.2

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install Django==4.2
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Project Structure

```
Website-Sample/
├── accounts/              # User authentication and profile app
│   ├── views/
│   │   ├── auth_views.py      # Register, login, logout views
│   │   └── profile_views.py   # Profile view and edit views
│   ├── templates/
│   │   └── accounts/          # HTML templates for accounts
│   └── urls.py
├── banks/                 # Banks and branches app
│   ├── models.py              # Bank and Branch models
│   ├── forms/                 # Form classes
│   │   ├── bank_form.py
│   │   └── branch_form.py
│   ├── views/
│   │   ├── bank_views.py      # Bank and branch creation views
│   │   └── generic_views.py   # ListView, DetailView, UpdateView
│   ├── templates/
│   │   └── banks/              # HTML templates for banks
│   └── urls.py
├── website/               # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3             # SQLite database (created after migrations)
└── Makefile               # Cleanup script
```

## Available Endpoints

### Authentication Endpoints

- **GET/POST** `/accounts/register/` - User registration
  - Fields: `username`, `password1`, `password2`, `email`, `first_name`, `last_name`
  - Success: Redirects to `/accounts/login/`

- **GET/POST** `/accounts/login/` - User login
  - Fields: `username`, `password`
  - Success: Redirects to `/accounts/profile/view/`

- **GET** `/accounts/logout/` - User logout
  - Redirects to `/accounts/login/`

### Profile Endpoints

- **GET** `/accounts/profile/view/` - View user profile (JSON)
  - Returns: `id`, `username`, `email`, `first_name`, `last_name`
  - Requires: Authentication (401 if not authenticated)

- **GET/POST** `/accounts/profile/edit/` - Edit user profile
  - Fields: `first_name`, `last_name`, `email`, `password1`, `password2`
  - Success: Redirects to `/accounts/profile/view/`
  - Requires: Authentication (401 if not authenticated)

### Bank Endpoints

- **GET** `/banks/all/` - List all banks (HTML)
  - Shows bank ID and name in a list

- **GET** `/banks/<bank_id>/details/` - Bank details (HTML)
  - Shows: name, SWIFT code, institution number, description

- **GET/POST** `/banks/add/` - Create a new bank
  - Fields: `name`, `description`, `inst_num`, `swift_code`
  - Success: Redirects to `/banks/<bank_id>/details/`
  - Requires: Authentication (401 if not authenticated)

### Branch Endpoints

- **GET** `/banks/branch/<branch_id>/details/` - Branch details (JSON)
  - Returns: `id`, `name`, `transit_num`, `address`, `email`, `capacity`, `last_modified`

- **GET** `/banks/<bank_id>/branches/all/` - All branches for a bank (JSON)
  - Returns: Array of branch objects

- **GET/POST** `/banks/<bank_id>/branches/add/` - Create a new branch
  - Fields: `name`, `transit_num`, `address`, `email`, `capacity`
  - Success: Redirects to `/banks/branch/<branch_id>/details/`
  - Requires: Authentication (401 if not authenticated)
  - Requires: User must own the bank (403 if not owner, 404 if bank doesn't exist)

- **GET/POST** `/banks/branch/<branch_id>/edit/` - Edit a branch
  - Fields: `name`, `transit_num`, `address`, `email`, `capacity`
  - Success: Redirects to `/banks/branch/<branch_id>/details/`
  - Requires: Authentication (401 if not authenticated)
  - Requires: User must own the branch's bank (403 if not owner, 404 if branch doesn't exist)

## Models

### Bank
- `name` (CharField, max_length=200)
- `swift_code` (CharField, max_length=200)
- `institution_number` (CharField, max_length=200)
- `description` (CharField, max_length=200)
- `owner` (ForeignKey to User)

### Branch
- `name` (CharField, max_length=200)
- `transit_number` (CharField, max_length=200)
- `address` (CharField, max_length=200)
- `email` (EmailField, default='admin@utoronto.ca')
- `capacity` (PositiveIntegerField, optional)
- `last_modified` (DateTimeField, auto-updated)
- `bank` (ForeignKey to Bank)

## Validation Rules

### Registration
- Username, password, and repeat password are required
- Password must be at least 8 characters
- Passwords must match
- Email must be valid (if provided)
- Username must be unique

### Profile Edit
- Email must be valid (if provided)
- If password is provided, it must be at least 8 characters
- Passwords must match (if both provided)

### Bank Creation
- All fields are required and cannot be blank

### Branch Creation/Edit
- All fields except `capacity` are required
- Email must be valid
- Capacity must be non-negative (if provided)

## Error Handling

The application handles errors with appropriate HTTP status codes:

- **200 OK**: Successful request
- **302 FOUND**: Redirect response
- **401 UNAUTHORIZED**: Authentication required
- **403 FORBIDDEN**: User doesn't have permission
- **404 NOT FOUND**: Resource doesn't exist
- **405 METHOD NOT ALLOWED**: HTTP method not allowed

## Cleanup

To clean the database and Python cache files:

```bash
make clean
```

This removes:
- `db.sqlite3`
- All `__pycache__` directories
- All `.pyc` files

## Testing

After setting up, you can test the application by:

1. Registering a new user at `/accounts/register/`
2. Logging in at `/accounts/login/`
3. Creating a bank at `/banks/add/`
4. Adding branches to your bank at `/banks/<bank_id>/branches/add/`
5. Viewing all banks at `/banks/all/`
6. Accessing JSON endpoints for branch information

## Notes

- The application uses Django's default User model for authentication
- All forms preserve user input on validation errors
- Missing form fields are treated as blank values
- Extra form fields are ignored
- The server never returns 500 INTERNAL SERVER ERROR for invalid requests
