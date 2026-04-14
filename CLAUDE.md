# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly - A Flask-based expense tracker web application (educational project). Students implement features following a step-by-step guide.

## Commands

```bash
# Run the application
python app.py

# Run tests
pytest
```

## Architecture

- **Framework**: Flask 3.1.3
- **Database**: SQLite (via `database/db.py` - students implement this)
- **Frontend**: Jinja2 templates + vanilla JavaScript
- **Testing**: pytest with pytest-flask

### Structure

```
app.py              # Main Flask app with routes
database/
  db.py             # Database layer (get_db, init_db, seed_db)
templates/          # Jinja2 HTML templates
static/
  css/              # Stylesheets (style.css, landing.css)
  js/               # Client-side JavaScript (main.js)
```

### Routes

- `/` - Landing page
- `/register`, `/login` - Authentication pages
- `/profile` - User profile
- `/expenses/*` - Expense CRUD operations
- `/terms`, `/privacy` - Legal pages
- `/logout` - Sign out

### Development Status

Core infrastructure is in place. Students implement:
- Database schema and seed data (`database/db.py`)
- Authentication (sessions, password hashing)
- Expense CRUD operations
- Profile page functionality
