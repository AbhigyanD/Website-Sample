# Application Flow - Simple Visual Guide

## Main Request Flow

```
┌─────────────┐
│   Browser   │ User types URL or submits form
└──────┬──────┘
       │ HTTP Request
       │ (GET or POST)
       ▼
┌─────────────────────────────────────┐
│      Django Server                  │
│  (manage.py runserver)              │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   Middleware                        │
│   • Security checks                 │
│   • Session management              │
│   • Authentication check            │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   URL Router                        │
│   (website/urls.py)                  │
│   Which app handles this?            │
└──────┬──────────────────────────────┘
       │
       ├─── /accounts/* ────→ accounts app
       │
       └─── /banks/* ────────→ banks app
              │
              ▼
┌─────────────────────────────────────┐
│   App URL Router                    │
│   (accounts/urls.py or banks/urls.py)│
│   Which view handles this?          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│   VIEW                              │
│   (views.py)                        │
│                                     │
│   What happens?                     │
│   • Check if user logged in?        │
│   • GET: Show form/page             │
│   • POST: Process form data         │
└──────┬──────────────────────────────┘
       │
       ├─── Need data? ────┐
       │                    │
       ▼                    ▼
┌──────────────┐    ┌──────────────┐
│   DATABASE   │    │   TEMPLATE   │
│   (SQLite)   │    │   (HTML)     │
│              │    │              │
│  Get/Store   │    │  Render HTML │
│  data        │    │  with data   │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └─────────┬──────────┘
                 │
                 ▼
         ┌──────────────┐
         │   Response   │
         │  (HTML/JSON) │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │   Browser    │
         │  Shows page  │
         └──────────────┘
```

## Registration Flow (Step by Step)

```
STEP 1: User visits /accounts/register/
        │
        ▼
STEP 2: URL Router finds register_view()
        │
        ▼
STEP 3: View checks: Is this GET or POST?
        │
        ├─── GET ────→ Show empty form
        │              (Go to STEP 4)
        │
        └─── POST ───→ Process form data
                       (Go to STEP 5)

STEP 4: Render register.html template
        │
        ▼
STEP 5: User sees form, fills it out, clicks "Register"
        │
        ▼
STEP 6: Browser sends POST request with form data
        │
        ▼
STEP 7: View receives POST data
        │
        ▼
STEP 8: Create RegisterForm with POST data
        │
        ▼
STEP 9: Form Validation
        │
        ├─── Valid? ────→ Create User in database
        │                 Redirect to /accounts/login/
        │
        └─── Invalid? ──→ Show form again with errors
                          (Go back to STEP 4)
```

## Creating a Bank Flow

```
User (logged in) → /banks/add/
        │
        ▼
┌──────────────────────────┐
│  Authentication Check    │
│  Is user logged in?      │
└──────┬───────────────────┘
       │
       ├─── No ────→ Return 401 Unauthorized
       │
       └─── Yes ────→ Continue
              │
              ▼
       ┌──────────────┐
       │  GET Request │
       │  Show form   │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │  POST Request│
       │  User submits│
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │  Validate    │
       │  Form Data   │
       └──────┬───────┘
              │
              ├─── Invalid ────→ Show errors
              │
              └─── Valid ──────→ Create Bank
                                  Save to database
                                  Redirect to details page
```

## Data Flow: View → Database → Template

```
┌──────────────┐
│    VIEW      │
│              │
│  Needs data  │
└──────┬───────┘
       │
       │ Bank.objects.get(pk=1)
       ▼
┌──────────────┐
│    MODEL     │
│              │
│  Bank model  │
└──────┬───────┘
       │
       │ Django ORM converts to SQL
       ▼
┌──────────────┐
│   DATABASE   │
│   (SQLite)   │
│              │
│  SELECT *    │
│  FROM banks  │
│  WHERE id=1  │
└──────┬───────┘
       │
       │ Returns Bank object
       ▼
┌──────────────┐
│    VIEW      │
│              │
│  Gets data   │
└──────┬───────┘
       │
       │ Pass to template as context
       ▼
┌──────────────┐
│   TEMPLATE   │
│              │
│  Renders     │
│  {{ bank.name }}│
└──────┬───────┘
       │
       │ Final HTML
       ▼
┌──────────────┐
│   BROWSER    │
│              │
│  Shows page  │
└──────────────┘
```

## Error Handling Flow

```
Request comes in
       │
       ▼
┌──────────────┐
│  Try to      │
│  process     │
└──────┬───────┘
       │
       ├─── Success ────→ Return 200 OK
       │
       ├─── Not logged in ────→ Return 401 Unauthorized
       │
       ├─── Not found ────→ Return 404 Not Found
       │
       ├─── No permission ────→ Return 403 Forbidden
       │
       └─── Form errors ────→ Return 200 OK with error messages
```

## Technologies Stack (Visual)

```
┌─────────────────────────────────────┐
│         USER INTERFACE              │
│  • HTML Templates                   │
│  • Forms                            │
│  • Browser                          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         DJANGO FRAMEWORK             │
│  ┌──────────────────────────────┐   │
│  │  URL Routing                │   │
│  │  Views (Logic)              │   │
│  │  Forms (Validation)         │   │
│  │  Templates (Presentation)   │   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         DATABASE LAYER               │
│  • Django ORM (Object-Relational     │
│    Mapping)                          │
│  • SQLite Database                   │
│  • Models (Bank, Branch, User)       │
└─────────────────────────────────────┘
```

## Key Concepts Explained Simply

### 1. **URL Routing**
   - Like a receptionist directing visitors
   - "/accounts/register/" → "Go to register view"
   - "/banks/all/" → "Go to bank list view"

### 2. **Views**
   - The "brain" of the application
   - Decides what to do with each request
   - Gets data, processes forms, returns responses

### 3. **Models**
   - Define what data looks like
   - Bank has: name, swift_code, owner, etc.
   - Like a blueprint for database tables

### 4. **Templates**
   - HTML pages with placeholders
   - `{{ bank.name }}` gets filled with actual data
   - Like a form letter with blanks to fill in

### 5. **Forms**
   - Collect user input
   - Validate data (check if valid)
   - Show errors if something's wrong

### 6. **Database**
   - Stores all the data
   - Like a filing cabinet
   - Django ORM is like a translator (Python ↔ SQL)

## Simple Example: Viewing All Banks

```
1. User clicks link: "View All Banks"
   URL: /banks/all/

2. Browser sends: GET /banks/all/

3. Django receives request
   → Checks middleware (security, sessions)
   → Routes to banks app
   → Finds BankListView

4. BankListView runs:
   → Gets all banks from database
   → Bank.objects.all()
   → Returns list of Bank objects

5. Template renders:
   → Loops through banks
   → Shows each bank's ID and name
   → Generates HTML

6. Browser receives HTML
   → Displays list of banks to user
```

## Form Submission Example

```
1. User fills out form
   Name: "First Bank"
   Description: "A great bank"
   [Submit button clicked]

2. Browser sends POST request
   POST /banks/add/
   Data: name=First Bank&description=A great bank...

3. Django processes:
   → Creates BankForm with POST data
   → Validates: Are all fields filled?
   → If valid: Create Bank object
   → Save to database
   → Redirect to success page

4. If invalid:
   → Show form again
   → Display error messages
   → Keep user's input (so they don't retype)
```

This is the basic flow of how web applications work!

