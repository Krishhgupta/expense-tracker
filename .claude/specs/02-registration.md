# Spec: Registration

## Overview

Implement user registration so new visitors can create a Spendly account. This step upgrades the existing stub GET /register route into a fully functional form that accepts a POST, validates input, hashes the password, and inserts a new row into the users table. On success the user is shown with a success message and then redirected to the login page. This is the entry point for all authenticated features that follow.

## Depends on

- Step 01 – Database setup (`users` table,
  get_db()`)

## Routes
- `GET /register` – render registration
  form – public (already exists as stub,
  upgrade it)
- `POST /register` – process registration
  form, insert user, redirect to `/login` –
  public

## Implementation Details

### Registration Form

The `templates/register.html` file already exists. It should include:
- Form with POST method to `/register`
- Fields: name, email, password
- CSRF protection (Flask's built-in protection or manual token)
- Display error messages for validation failures
- Link to login page for existing users

### Backend Logic (app.py)

The `/register` route needs to handle both GET and POST:

**GET**: Render the registration template

**POST**:
1. Extract form data (name, email, password)
2. Validate:
   - All fields are non-empty
   - Email format is valid
   - Password meets minimum length (e.g., 6 characters)
3. Check if email already exists in database
4. Hash password using `werkzeug.security.generate_password_hash`
5. Insert new user into database
6. Redirect to login page on success
7. Re-render form with error messages on failure

### Database Query

Use parameterized query to insert new user:
```python
cursor.execute(
    "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
    (name, email, password_hash)
)
```

Handle `sqlite3.IntegrityError` for duplicate email addresses.

## Constraints

- No SQLAlchemy or ORMs - use raw SQLite with parameterized queries only
- Passwords must be hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables for styling - never hardcoded hex values
- All templates must extend `base.html`
- Email uniqueness enforced by database constraint

## Definition of Done

- [ ] GET /register displays the registration form
- [ ] Form includes name, email, and password fields
- [ ] POST /register validates all fields are non-empty
- [ ] Email format is validated
- [ ] Password minimum length is enforced
- [ ] Duplicate email addresses are rejected with user-friendly error
- [ ] Password is hashed before storage
- [ ] New user is inserted into database successfully
- [ ] Successful registration redirects to login page
- [ ] Errors are displayed on the registration form
- [ ] Registration page links to login page
- [ ] All SQL queries use parameterized statements
