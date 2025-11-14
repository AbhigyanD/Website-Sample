# Technologies Used & Application Flow

## Technologies and Concepts

### Core Technologies

1. **Python 3.9+**
   - Programming language used for the entire backend
   - Object-oriented programming concepts

2. **Django 4.2**
   - High-level Python web framework
   - Handles URL routing, views, models, templates, forms
   - Built-in admin interface and authentication system

3. **SQLite**
   - Lightweight database (stored in `db.sqlite3`)
   - Used for storing Bank, Branch, and User data
   - No separate database server needed

4. **HTML**
   - Markup language for creating web pages
   - Used in templates to structure content

5. **HTTP/HTTPS**
   - Protocol for communication between browser and server
   - Methods: GET (retrieve data), POST (submit data)

### Django Components Used

1. **Models** (`models.py`)
   - Define database structure (Bank, Branch)
   - Use Django ORM (Object-Relational Mapping)
   - Fields: CharField, EmailField, ForeignKey, DateTimeField

2. **Views**
   - Function-based views: `register_view()`, `login_view()`, etc.
   - Class-based views: `FormView`, `ListView`, `DetailView`, `UpdateView`
   - Handle business logic and return responses

3. **URLs** (`urls.py`)
   - URL routing configuration
   - Maps URLs to view functions/classes
   - URL patterns with parameters (e.g., `<int:bank_id>`)

4. **Templates** (HTML files)
   - Django template language
   - Template tags: `{% csrf_token %}`, `{% for %}`, `{% if %}`
   - Template filters: `|default:''`, `|default_if_none:''`

5. **Forms**
   - Django form classes (`forms.Form`)
   - Form validation and error handling
   - CSRF protection

6. **Middleware**
   - Authentication middleware (checks if user is logged in)
   - CSRF middleware (security)
   - Session middleware (maintains user sessions)

7. **Migrations**
   - Database schema version control
   - `makemigrations`: Create migration files
   - `migrate`: Apply migrations to database

### Security Features

1. **CSRF Protection**
   - Cross-Site Request Forgery protection
   - `{% csrf_token %}` in forms

2. **Authentication**
   - Django's built-in User model
   - Session-based authentication
   - `LoginRequiredMixin` for protected views

3. **Authorization**
   - Permission checks (user owns bank/branch)
   - HTTP status codes: 401, 403, 404

### Development Tools

1. **Virtual Environment** (`venv`)
   - Isolates project dependencies
   - Prevents conflicts between projects

2. **pip**
   - Python package manager
   - Installs Django and dependencies

3. **Makefile**
   - Automation tool for common tasks
   - `make clean` removes database and cache

## Application Flow - Request/Response Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                                │
│  User types URL or submits form                                  │
│  Example: http://127.0.0.1:8000/accounts/register/              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Request (GET or POST)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DJANGO SERVER                                 │
│                    (manage.py runserver)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              MIDDLEWARE LAYER                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Security Middleware (CSRF protection)                  │  │
│  │ 2. Session Middleware (maintains user sessions)           │  │
│  │ 3. Authentication Middleware (checks if user logged in)    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    URL ROUTING                                   │
│                    (website/urls.py)                             │
│                                                                   │
│  URL Pattern Matching:                                           │
│  /accounts/register/ → accounts.urls                             │
│  /banks/all/ → banks.urls                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              APP-LEVEL URL ROUTING                               │
│              (accounts/urls.py or banks/urls.py)                 │
│                                                                   │
│  Matches specific pattern and calls view:                        │
│  /accounts/register/ → register_view()                           │
│  /banks/<bank_id>/details/ → BankDetailView.as_view()           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VIEW LAYER                                    │
│                    (views.py files)                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Function-Based View:                                      │  │
│  │  1. Check request method (GET or POST)                    │  │
│  │  2. If GET: Render form template                          │  │
│  │  3. If POST:                                              │  │
│  │     a. Validate form data                                  │  │
│  │     b. If valid: Process data, save to database            │  │
│  │     c. If invalid: Re-render form with errors             │  │
│  │  4. Return HTTP response                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Class-Based View (FormView, ListView, etc.):              │  │
│  │  1. dispatch() - Entry point, checks permissions          │  │
│  │  2. get() - Handles GET requests                          │  │
│  │  3. post() - Handles POST requests                        │  │
│  │  4. form_valid() - Called when form is valid              │  │
│  │  5. get_context_data() - Prepares data for template       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ (If database access needed)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MODEL LAYER                                   │
│                    (models.py)                                   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Django ORM (Object-Relational Mapping)                    │  │
│  │                                                           │  │
│  │ Bank.objects.create(...)  → Creates new bank record      │  │
│  │ Bank.objects.get(pk=1)    → Retrieves bank by ID        │  │
│  │ Bank.objects.all()        → Gets all banks               │  │
│  │ branch.bank.owner         → Follows foreign key          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│                    SQLite Database                               │
│                    (db.sqlite3)                                  │
│                    Stores: Users, Banks, Branches               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ (Data returned)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TEMPLATE LAYER                                │
│                    (templates/*.html)                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Django Template Engine:                                   │  │
│  │  1. Receives context data from view                      │  │
│  │  2. Renders HTML with dynamic content                    │  │
│  │  3. Template tags: {% csrf_token %}, {% for %}            │  │
│  │  4. Template filters: {{ form.name.value|default:'' }}    │  │
│  │  5. Generates final HTML                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTML Response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                                │
│  Displays rendered HTML page                                     │
│  User sees form, data, or error messages                         │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Flow Examples

### Example 1: User Registration Flow

```
1. User visits: /accounts/register/
   └─> URL Router → accounts.urls → register_view()

2. GET Request:
   └─> register_view() creates empty RegisterForm
   └─> Renders register.html template
   └─> Returns HTML form to browser

3. User fills form and clicks "Register"
   └─> Browser sends POST request with form data

4. POST Request:
   └─> register_view() receives POST data
   └─> Creates RegisterForm with POST data
   └─> Form validation:
       ├─> Checks required fields
       ├─> Validates password length (min 8 chars)
       ├─> Checks if passwords match
       ├─> Validates email format (if provided)
       └─> Checks if username exists

5. If Valid:
   └─> Creates User object in database
   └─> Redirects to /accounts/login/ (302 status)

6. If Invalid:
   └─> Re-renders form with error messages
   └─> Preserves user input
   └─> Returns HTML with errors (200 status)
```

### Example 2: Creating a Bank Flow

```
1. User (logged in) visits: /banks/add/
   └─> URL Router → banks.urls → BankAddView.as_view()

2. Authentication Check:
   └─> LoginRequiredMixin checks if user authenticated
   └─> If not: Returns 401 Unauthorized
   └─> If yes: Continues

3. GET Request:
   └─> BankAddView.get() called
   └─> Creates empty BankForm
   └─> Renders bank_add.html template
   └─> Returns HTML form

4. User submits form:
   └─> POST request with: name, description, inst_num, swift_code

5. POST Request:
   └─> BankAddView.post() called
   └─> Creates BankForm with POST data
   └─> Form validation:
       └─> All fields required (checked by form)

6. If Valid:
   └─> form_valid() method called
   └─> Creates Bank object:
       ├─> Sets name, description, etc.
       └─> Sets owner = request.user (current logged-in user)
   └─> Saves to database (SQLite)
   └─> Redirects to /banks/<bank_id>/details/

7. Bank Details View:
   └─> BankDetailView retrieves bank from database
   └─> Renders bank_details.html
   └─> Shows bank information
```

### Example 3: JSON API Endpoint Flow

```
1. Request: GET /banks/branch/1/details/
   └─> URL Router → banks.urls → BranchDetailsView()

2. View Function:
   └─> Tries to get Branch with id=1 from database
   └─> If not found: Returns 404 Not Found
   └─> If found: Creates dictionary with branch data

3. Response:
   └─> JsonResponse() converts dictionary to JSON
   └─> Returns JSON string:
       {
         "id": 1,
         "name": "Main Branch",
         "transit_num": "12345",
         "address": "123 Main St",
         "email": "admin@utoronto.ca",
         "capacity": 100,
         "last_modified": "2025-11-14T16:55:00Z"
       }
   └─> Content-Type: application/json
```

## Key Principles

### 1. **Separation of Concerns**
   - **Models**: Data structure and database operations
   - **Views**: Business logic and request handling
   - **Templates**: Presentation and user interface
   - **URLs**: Routing and navigation

### 2. **DRY (Don't Repeat Yourself)**
   - Reusable form classes
   - Template inheritance (can be extended)
   - Class-based views for common patterns

### 3. **MVC Pattern (Model-View-Controller)**
   - **Model**: Database models (Bank, Branch)
   - **View**: Views and templates (what user sees)
   - **Controller**: URL routing and view logic

### 4. **Security First**
   - CSRF protection on all forms
   - Authentication checks before sensitive operations
   - Authorization checks (user owns resource)
   - Input validation and sanitization

### 5. **Stateless HTTP with State Management**
   - HTTP is stateless (each request is independent)
   - Django sessions maintain user state
   - Cookies store session ID

## Request/Response Types

### HTML Responses
- Used for: Forms, lists, detail pages
- Content-Type: `text/html`
- Rendered by: Django templates

### JSON Responses
- Used for: API endpoints, profile data
- Content-Type: `application/json`
- Created by: `JsonResponse()`

### Redirect Responses
- Used for: After successful form submission
- Status Code: `302 Found`
- Created by: `redirect()` function

## Error Handling Flow

```
Request → View → Error Occurs?
                    │
        ┌───────────┴───────────┐
        │                        │
    Try/Except              Validation Error
        │                        │
        ▼                        ▼
  404 Not Found          Form with Errors
  (Resource missing)     (Re-render template)
        │                        │
        └───────────┬────────────┘
                    │
                    ▼
            HTTP Response
            (Status Code + Message)
```

## Database Interaction Flow

```
View needs data
    │
    ▼
Model.objects.method()
    │
    ├─> .create() → INSERT INTO database
    ├─> .get() → SELECT WHERE (single object)
    ├─> .all() → SELECT * (all objects)
    ├─> .filter() → SELECT WHERE (multiple objects)
    └─> .save() → UPDATE database
    │
    ▼
Django ORM converts to SQL
    │
    ▼
SQLite executes SQL query
    │
    ▼
Returns Python objects
    │
    ▼
View uses objects
    │
    ▼
Template renders data
```

This architecture ensures:
- **Maintainability**: Clear separation of code
- **Scalability**: Can handle more users/data
- **Security**: Built-in protections
- **Testability**: Each component can be tested separately

