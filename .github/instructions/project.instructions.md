---
applyTo: '**'
---

# Project Context: Therapy Session Management Application

## Overview
Flask-based web application for managing patient therapy sessions with payment tracking. **Modular architecture** with factory pattern, blueprints, service layer, and SQLAlchemy ORM.

## Current Architecture (Post-Refactoring)

### Application Structure
- **Type**: Modular Flask application with factory pattern
- **Database**: SQLite (dev), PostgreSQL (prod), SQLAlchemy 2.0+ ORM
- **Frontend**: Jinja2 templates with Bootstrap 5
- **Authentication**: Flask-Login with session management
- **Security**: Flask-WTF CSRF, Flask-Limiter rate limiting
- **Language**: Spanish UI, English code/comments

### Project Structure
```
appalapapa/
├── app/                          # Application package
│   ├── __init__.py              # App factory (create_app)
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Flask extensions
│   ├── api/v1/                  # REST API endpoints
│   ├── cli/                     # CLI commands
│   ├── middleware/              # Error handlers, security
│   ├── models/                  # SQLAlchemy models
│   ├── routes/                  # View blueprints
│   ├── services/                # Business logic layer
│   ├── utils/                   # Utilities (constants, formatters)
│   └── validators/              # Flask-WTF forms
├── templates/                   # Jinja2 templates (organized by module)
│   ├── base.html               # Base template with nav
│   ├── auth/                   # Authentication templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── reset_password.html
│   │   └── change_password.html
│   ├── patients/               # Patient management templates
│   │   ├── list.html           # Main dashboard
│   │   ├── form_person.html
│   │   └── delete_person.html
│   ├── sessions/               # Session management templates
│   │   ├── form_session.html
│   │   └── form_edit.html
│   └── errors/                 # Error pages (403, 404, 500)
├── static/                      # Static assets (CSS, JS)
├── tests/                       # pytest test suite
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── requirements/                # Dependency files by environment
├── run.py                       # Development entry point
├── wsgi.py                      # Production WSGI entry
├── Dockerfile                   # Docker configuration
└── docker-compose.yml           # Docker Compose
```

### Database Schema (SQLAlchemy Models)
- **User**: User accounts with roles (admin/therapist/viewer)
- **Person**: Patient records with soft delete support
- **TherapySession**: Therapy sessions (date, price, pending status)
- **AuditLog**: Audit trail for all CRUD operations

---

## Implemented Best Practices

### 1. Security ✅
- **Environment variables**: All secrets via `.env` file
- **Password hashing**: Werkzeug's secure password hashing
- **CSRF protection**: Flask-WTF on all forms
- **Rate limiting**: Flask-Limiter on authentication routes
- **SQL injection prevention**: SQLAlchemy ORM (no raw SQL)
- **Security headers**: Custom middleware for X-Frame-Options, etc.
- **Role-based access**: Admin, Therapist, Viewer roles

### 2. Architecture ✅
- **Factory pattern**: `create_app()` for testability
- **Blueprints**: Organized route separation (auth, patients, sessions)
- **Service layer**: Business logic decoupled from routes
- **Soft delete**: Recoverable data with `SoftDeleteMixin`
- **Audit logging**: Track all data changes with user attribution
- **Database migrations**: Flask-Migrate (Alembic)

### 3. Code Quality ✅
- **Type hints**: On all function signatures
- **Form validation**: Flask-WTF with custom validators
- **Error handling**: Centralized error handlers
- **Logging**: Configured logging with levels
- **Constants**: Named constants in `utils/constants.py`

### 4. Testing ✅
- **pytest**: Unit and integration tests
- **Fixtures**: Reusable test data in `conftest.py`
- **Coverage**: pytest-cov for coverage reports

### 5. DevOps ✅
- **Docker**: Multi-stage build for dev/prod
- **CI/CD**: GitHub Actions pipeline
- **Environment configs**: dev/test/prod separation

### 6. Accessibility (WCAG 2.1 AA) ✅
- **Semantic HTML**: Proper heading hierarchy, landmark elements
- **ARIA Labels**: All interactive elements have accessible names
- **Keyboard Navigation**: Full functionality without mouse
- **Color Contrast**: Minimum 4.5:1 ratio for text
- **Focus Indicators**: Visible focus states for all interactive elements
- **Form Accessibility**: Labels linked to inputs, error announcements

### 7. Minimalist UI Design ✅
- **Visual Simplicity**: Clean layouts with purposeful whitespace
- **Limited Colors**: 3-4 primary colors maximum
- **Typography**: Consistent font sizing scale
- **Content-First**: UI serves content, not decoration
- **Progressive Disclosure**: Essential info first, details on demand

### 8. Dark Mode Support ✅
- **Default Theme**: Dark mode is the default (`data-bs-theme="dark"`)
- **Theme Switcher**: Sun/moon toggle button in navbar
- **Persistence**: User preference saved to localStorage
- **Bootstrap 5.3 Theming**: Uses native `data-bs-theme` attribute
- **Adaptive Classes**: Use theme-aware classes (see guidelines below)

#### Dark Mode UI Guidelines
When creating or modifying UI components:

```html
<!-- ✅ DO: Use theme-adaptive classes -->
<div class="card-header border-bottom">  <!-- Not bg-light -->
<small class="text-body-secondary">      <!-- Not text-muted -->
<button class="btn btn-outline-light">   <!-- High contrast in dark -->

<!-- ❌ DON'T: Use hardcoded colors -->
<div class="bg-light">                   <!-- Breaks in dark mode -->
<span style="color: #666;">              <!-- Won't adapt -->
<button style="filter: invert(50%);">    <!-- Hacky, unreliable -->
```

**Button Color Semantic Guide**:
| Action | Class | Reason |
|--------|-------|--------|
| Edit/neutral | `btn-outline-secondary` | Good contrast in both light and dark modes |
| Success/paid | `btn-success` | Green = positive confirmation |
| Warning/pending | `btn-outline-warning` | Yellow = attention needed |
| Danger/delete | `btn-outline-danger` | Red = destructive action |
| Navigation | `btn-outline-secondary` | Subtle, non-competing |

---

## Coding Conventions

### 1. Database Access (Use Services)
```python
# ✅ CORRECT - Use service layer
from app.services.patient_service import PatientService

success, person, message = PatientService.create(name='John Doe', user_id=user.id)

# ❌ AVOID - Direct database access in routes
db.session.add(Person(name='John Doe'))
```

### 2. Error Handling Pattern
```python
# ✅ Always use try/except with logging
try:
    success, result, message = SomeService.do_something()
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
except Exception as e:
    current_app.logger.error(f"Error: {e}")
    flash("Error inesperado. Intente nuevamente.", "error")
    db.session.rollback()
```

### 3. Route Organization
```python
# ✅ Use blueprints with prefixes
from flask import Blueprint

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # ...
```

### 4. Form Validation
```python
# ✅ Use Flask-WTF forms
from app.validators.forms import PersonForm

form = PersonForm()
if form.validate_on_submit():
    name = form.name.data.strip()
```

### 5. Spanish UI / English Code
```python
# ✅ UI messages in Spanish
flash("Paciente creado exitosamente.", "success")

# ✅ Code and comments in English
def create_patient(name: str) -> Person:
    """Create a new patient record."""
    pass
```

### 6. Template Organization
```
templates/
├── base.html           # Base template (extends nothing)
├── auth/               # Authentication templates
├── patients/           # Patient management templates
├── sessions/           # Session management templates
└── errors/             # Error pages (403, 404, 500)

# ✅ All templates extend base.html
{% extends 'base.html' %}

# ✅ Use block main for content
{% block main %}...{% endblock main %}

# ✅ Always include CSRF token in forms
{{ form.hidden_tag() }}

# ✅ Use blueprint-based url_for
{{ url_for('auth.login') }}
{{ url_for('patients.index') }}
{{ url_for('sessions.add_session') }}
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `CHANGELOG.md` | Version history and release notes |
| `README.md` | Project overview and documentation |
| `app/__init__.py` | App factory, register extensions/blueprints |
| `app/config.py` | Configuration classes (dev/test/prod) |
| `app/extensions.py` | Flask extension instances |
| `app/models/*.py` | SQLAlchemy models with mixins |
| `app/services/*.py` | Business logic (auth, patient, session) |
| `app/routes/*.py` | View blueprints |
| `app/validators/forms.py` | Flask-WTF form definitions |
| `templates/base.html` | Base template with navigation |
| `templates/auth/*.html` | Authentication templates (login, register) |
| `templates/patients/*.html` | Patient management templates |
| `templates/sessions/*.html` | Session management templates |
| `templates/errors/*.html` | Error pages (403, 404, 500) |
| `tests/conftest.py` | Pytest fixtures |

---

## Environment Variables (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `FLASK_CONFIG` | Configuration name | `development` |
| `DATABASE_URL` | Database connection | `sqlite:///instance/database.db` |
| `ALLOWED_EMAILS` | Allowed registration emails | `user@example.com` |
| `SENTRY_DSN` | Sentry error tracking (prod) | `https://...` |

---

## CLI Commands

```bash
# Database
flask db init-db          # Initialize tables
flask db seed             # Seed sample data
flask db backup           # Backup database

# Users
flask user create EMAIL   # Create new user
flask user list           # List all users
flask user set-role EMAIL ROLE
```

---

## Testing Commands

```bash
# Activate virtual environment first
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux

# Run tests
pytest                    # All tests
pytest -v                 # Verbose
pytest --cov=app          # With coverage
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
```

---

## Visual Verification with Screenshots (Frontend Changes)

When modifying templates or frontend files, **always take screenshots** to verify:

### Test Credentials for Development

To access authenticated pages for visual verification, use:

| Email | Password | Role | Notes |
|-------|----------|------|-------|
| `test@example.com` | `test123` | admin | Created by `flask db-utils seed` |

**Setup test user** (if not exists):
```bash
flask db-utils seed
```

### Screenshot Verification Workflow
1. **Start the server** (if not running):
   ```bash
   flask run
   # or
   python run.py
   ```

2. **Login first** (for authenticated pages):
   - Open browser at `http://localhost:5000/auth/login`
   - Use test credentials: `test@example.com` / `test123`
   - Note: VS Code Simple Browser is view-only; use external browser for login

3. **Open in Simple Browser**: Use VS Code's internal browser at `http://localhost:5000`
   - Simple Browser shares session with external browser if same port
   - For unauthenticated pages (login, register, errors), Simple Browser works directly

4. **Take a screenshot**: Capture the current state of the UI

5. **Verify visually**:
   - Layout renders correctly without overlapping
   - Text is readable and properly aligned
   - Buttons and links are visible and functional
   - Forms display correctly with labels

5. **Check accessibility**:
   - Keyboard navigation works (Tab, Enter, Escape)
   - Focus indicators are visible
   - Color contrast is sufficient
   - ARIA labels are present on interactive elements

6. **Test responsive design**: Check at different viewport widths:
   - Mobile: ~375px
   - Tablet: ~768px  
   - Desktop: ~1200px+

7. **If errors found**: 
   - Fix the issue
   - **Take another screenshot** to confirm the fix
   - Repeat until no issues remain

8. **Complete**: Only mark task done after screenshot verification passes

### Common Issues to Check
- Navigation arrows overlapping content (carousels)
- Text overflow/truncation
- Button alignment and spacing
- Card/grid layout responsiveness
- Flash message visibility
- Missing focus indicators
- Poor color contrast
- **Dark mode compatibility**: Check UI in both light and dark themes
- **Theme switcher**: Verify theme toggle works and persists across page reloads

---

## Backend Testing Workflow (Backend Changes)

When modifying any backend file, **always run tests** to verify:

### Mandatory Testing Steps
1. **Run full test suite**:
   ```bash
   pytest
   ```

2. **Run specific test category** based on change:
   ```bash
   # For model changes
   pytest tests/unit/test_models.py -v
   
   # For service changes
   pytest tests/unit/test_services.py -v
   
   # For route changes
   pytest tests/integration/ -v
   
   # For form/validator changes
   pytest tests/unit/test_validators.py -v
   ```

3. **Check for failures**: All tests must pass before marking complete

4. **Add new tests**: If new functionality lacks test coverage, write tests

5. **Run with coverage** (optional but recommended):
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

### When to Run Tests
- ✅ After modifying any file in `app/models/`
- ✅ After modifying any file in `app/services/`
- ✅ After modifying any file in `app/routes/`
- ✅ After modifying any file in `app/validators/`
- ✅ After modifying any file in `app/utils/`
- ✅ After modifying any file in `app/middleware/`
- ✅ After modifying any file in `app/api/`

---

## DO NOT DO (Anti-patterns)

❌ Hardcode secrets or emails in source code
❌ Use `debug=True` in production
❌ Skip CSRF protection on forms
❌ Access database directly in routes (use services)
❌ Commit `.env` file to Git
❌ Skip input validation
❌ Mix Spanish/English in user-facing text
❌ Create raw SQL queries (use ORM)
❌ Skip tests for new features
❌ Delete data permanently without soft delete
❌ Skip CHANGELOG.md updates for new features
❌ Skip screenshot verification after frontend changes
❌ Assume frontend changes work without visual testing
❌ Skip running pytest after backend modifications
❌ Ignore test failures and proceed with changes
❌ Create UI elements without ARIA labels
❌ Use color alone to convey information
❌ Skip keyboard navigation testing
❌ Create cluttered, complex UI layouts
❌ Add decorative elements that don't serve function