---
applyTo: '**'
---

# Project Context: Therapy Session Management Application

## Overview
Flask-based web application for managing patient therapy sessions with payment tracking. Single-file monolithic architecture using SQLite database.

## Current Architecture

### Application Structure
- **Type**: Monolithic Flask application
- **Database**: SQLite (file-based: `database.db`)
- **Frontend**: Jinja2 templates with Bootstrap 5
- **Authentication**: Session-based with hardcoded credentials
- **Language**: Spanish UI, Python codebase

### Database Schema
- **users**: User accounts (email, hashed password)
- **persons**: Patient records (name only)
- **sessions**: Therapy sessions (date, price, pending status)

---

## Good Practices Detected

### 1. Security
✅ **Password hashing** using Werkzeug's `generate_password_hash` and `check_password_hash`
✅ **Login decorator** (`@login_required`) for route protection
✅ **Foreign key constraints** with `ON DELETE CASCADE` for data integrity
✅ **SQL injection protection** via parameterized queries (`?` placeholders)

### 2. Code Organization
✅ **Decorator pattern** for authentication (`@login_required`)
✅ **Context managers** for database connections (`with sqlite3.connect()`)
✅ **Template inheritance** (base.html extended by all templates)
✅ **Separation of concerns**: formatting functions (`format_date`, `format_price`)
✅ **DRY principle**: filter constants (`FILTERS`, `ALL_FILTER`, etc.)

### 3. User Experience
✅ **Flash messages** for user feedback on operations
✅ **Persistent sessions** (365 days) for convenience
✅ **Bootstrap styling** for responsive, professional UI
✅ **Confirmation page** for destructive operations (delete person)

---

## Critical Issues & Bad Practices

### 🔴 SECURITY VULNERABILITIES (HIGH PRIORITY)

#### 1. Hardcoded Secret Key
```python
app.secret_key = 'lui-psi-app'  # ❌ NEVER commit secrets to code
```
**Risk**: Session hijacking, XSS attacks
**Fix**: Use environment variables with strong random keys
```python
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
```

#### 2. Hardcoded Email Whitelist
```python
ALLOWED_EMAILS = {'emidesouches@gmail.com', 'luimuntaner@gmail.com'}  # ❌ PII in code
```
**Risk**: Privacy violation, GDPR non-compliance, inflexible
**Fix**: Move to database table or environment variable

#### 3. Weak Security Question
```python
if '-08-17' not in security:  # ❌ Trivial to guess
```
**Risk**: Account takeover
**Fix**: Implement proper password reset with email verification or remove feature

#### 4. Debug Mode in Production
```python
app.run(debug=True)  # ❌ Exposes stack traces & debugger
```
**Risk**: Information disclosure
**Fix**: Use environment-based configuration

#### 5. No CSRF Protection
**Risk**: Cross-site request forgery attacks on all POST forms
**Fix**: Use `Flask-WTF` with CSRF tokens

---

### 🟠 SCALABILITY & ARCHITECTURE ISSUES

#### 1. Database Connection Anti-pattern
```python
# ❌ Opens new connection on EVERY request
with sqlite3.connect("database.db") as conn:
```
**Problems**:
- No connection pooling
- SQLite not suitable for concurrent writes
- No migration system
- Hardcoded database path repeated 15+ times

**Fix**: 
- Use Flask-SQLAlchemy for ORM and connection pooling
- Implement configuration management
- Add migration system (Flask-Migrate/Alembic)
- Consider PostgreSQL for production

#### 2. Monolithic File Structure
**Problems**:
- All 293 lines in single `app.py`
- No separation of models, views, controllers
- Difficult to test
- No business logic layer

**Recommended Structure**:
```
app/
├── __init__.py          # App factory
├── models.py            # Database models
├── routes/
│   ├── auth.py          # Authentication routes
│   ├── patients.py      # Patient management
│   └── sessions.py      # Session management
├── services/            # Business logic
├── config.py            # Configuration classes
└── extensions.py        # Flask extensions
```

#### 3. No Environment Configuration
**Problems**:
- No `.env` file support
- Hardcoded values throughout
- Can't differentiate dev/staging/production

**Fix**: Use `python-decouple` or `Flask-Environ`

#### 4. Missing Data Validation
```python
person_id = request.form.get('person_id')  # ❌ No validation
session_price = request.form.get('session_price')  # ❌ Can be negative/text
```
**Fix**: Use `Flask-WTF` forms with validators

---

### 🟡 CODE QUALITY ISSUES

#### 1. No Error Handling
```python
# ❌ No try/except around database operations
cursor.execute("DELETE FROM sessions WHERE id = ?", (id,))
```
**Problems**: 
- App crashes on DB errors
- No user-friendly error messages
- No logging

#### 2. Raw SQL Everywhere
```python
# ❌ No abstraction layer
query = "SELECT persons.id, persons.name, sessions.id..."
```
**Problems**:
- Hard to maintain
- No type safety
- Prone to errors
- Complex joins in views

**Fix**: Use SQLAlchemy ORM

#### 3. Magic Strings and Numbers
```python
if '-08-17' not in security:  # ❌ What is this date?
session.permanent_session_lifetime = timedelta(days=365)  # ❌ Why 365?
```
**Fix**: Use named constants with comments

#### 4. Inconsistent Naming
```python
ALLOW_DELETE = True  # Constant (good)
grouped_sessions = defaultdict(list)  # Variable (good)
ALLOWED_EMAILS = {...}  # Constant but data (inconsistent)
```

#### 5. Weak Security Question Implementation
```python
if '-08-17' not in security:  # ❌ Substring match, predictable
```

#### 6. No Input Sanitization
```python
name = request.form.get('name')  # ❌ No strip(), title(), or length check
```

---

### 🟡 MISSING FEATURES FOR PRODUCTION

#### 1. No Logging System
- No audit trail for data changes
- No error tracking
- Can't debug production issues

**Fix**: Implement `logging` module or use Sentry

#### 2. No Testing
- No unit tests
- No integration tests
- No fixtures

**Fix**: Add pytest with test structure

#### 3. No API Versioning
- No REST API (only HTML)
- No mobile app support

#### 4. No Backup Strategy
- SQLite file can be corrupted/lost
- No automated backups

#### 5. No Rate Limiting
- Vulnerable to brute force attacks
- No protection against abuse

**Fix**: Use `Flask-Limiter`

#### 6. No Email Verification
- Registration has no email confirmation
- Password reset has no email token

#### 7. No User Roles/Permissions
- All logged-in users have full access
- No admin vs. regular user distinction

#### 8. No Soft Deletes
```python
cursor.execute("DELETE FROM sessions WHERE id = ?", (id,))  # ❌ Permanent
```
**Risk**: Accidental data loss with no recovery

---

### 🔵 FRONTEND ISSUES

#### 1. No Frontend Validation
- Forms have no client-side validation
- Poor UX (unnecessary server round-trips)

#### 2. No JavaScript Framework
- Limited interactivity
- No real-time updates
- Entire page reload for every action

#### 3. Hardcoded Bootstrap Files
```html
<link rel="stylesheet" href="{{ url_for('static', filename='/css/bootstrap.min.css') }}">
```
**Problem**: No version control, no CDN fallback, outdated

#### 4. No Accessibility Features
- No ARIA labels
- No keyboard navigation hints
- No screen reader support

---

## Coding Conventions to Follow

### 1. Database Access
```python
# ❌ AVOID
with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute(...)

# ✅ USE (with SQLAlchemy)
from app.models import Session
session = Session.query.filter_by(id=id).first()
```

### 2. Error Handling Pattern
```python
# ✅ Always wrap operations
try:
    # Database/file operations
    pass
except SQLAlchemyError as e:
    current_app.logger.error(f"Database error: {e}")
    flash("Error al procesar la solicitud. Intente nuevamente.", "error")
    db.session.rollback()
    return redirect(url_for('index'))
```

### 3. Configuration Management
```python
# ✅ Use config classes
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

### 4. Route Organization
```python
# ✅ Use blueprints
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass
```

### 5. Form Validation
```python
# ✅ Use Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired, Email, NumberRange

class SessionForm(FlaskForm):
    person_id = IntegerField('Person', validators=[DataRequired()])
    session_date = DateField('Date', validators=[DataRequired()])
    session_price = DecimalField('Price', validators=[
        DataRequired(), 
        NumberRange(min=0, message="El precio debe ser positivo")
    ])
```

### 6. Spanish UI Consistency
- All user-facing messages in Spanish
- All code/comments in English
- Flash messages follow: `flash("Mensaje descriptivo.", "category")`

### 7. Template Patterns
```django
{# ✅ Use Bootstrap utility classes #}
<div class="d-flex justify-content-between align-items-center">
    {# Content #}
</div>

{# ✅ Consistent button styling #}
<a href="..." class="btn btn-sm btn-primary bg-gradient">
    <strong>Texto del Botón</strong>
</a>
```

---

## Immediate Action Items (Priority Order)

### Phase 1: Security (URGENT)
1. Move `SECRET_KEY` to environment variable
2. Move `ALLOWED_EMAILS` to database or config
3. Add CSRF protection (Flask-WTF)
4. Remove weak security question or implement proper reset
5. Add rate limiting to login/register

### Phase 2: Architecture
1. Implement configuration management (dev/prod)
2. Add SQLAlchemy ORM
3. Restructure into modular architecture
4. Add database migrations (Flask-Migrate)
5. Implement logging system

### Phase 3: Validation & Error Handling
1. Add Flask-WTF forms with validation
2. Add comprehensive error handling
3. Add input sanitization
4. Implement soft deletes

### Phase 4: Testing & Documentation
1. Set up pytest framework
2. Write unit tests for models
3. Write integration tests for routes
4. Add API documentation
5. Create deployment guide

### Phase 5: Features
1. Add user roles (admin/user)
2. Implement email verification
3. Add audit logging
4. Add export functionality (PDF/CSV)
5. Add backup automation

---

## Files That Need Immediate Attention

1. **app.py** (Lines 71, 68): Remove hardcoded secrets
2. **app.py** (Line 292): Remove debug mode
3. **app.py** (Lines 131-135): Fix weak security question
4. **app.py** (All routes): Add CSRF protection
5. **README.md**: Typo on line 6 (`sctivate` → `activate`)
6. **requirements.txt**: Add missing dependencies (python-decouple, Flask-WTF, Flask-SQLAlchemy)

---

## DO NOT DO (Anti-patterns to Avoid)

❌ Hardcode sensitive data (emails, passwords, keys)
❌ Use `debug=True` in production
❌ Skip input validation
❌ Ignore error handling
❌ Commit database files to Git
❌ Use raw SQL without parameterization
❌ Skip CSRF protection on forms
❌ Store plaintext passwords
❌ Use SQLite for production with multiple users
❌ Mix Spanish/English in user-facing text
❌ Create database connections in views
❌ Skip logging for critical operations
❌ Allow negative prices or invalid dates
❌ Use substring matching for security (`if '-08-17' not in`)
❌ Delete data permanently without confirmation or soft delete

---

## Future Agents: Where to Find Things

- **Database connection**: Repeated in every route (needs refactoring to models)
- **Authentication**: `login_required` decorator (line 16-24)
- **Filtering logic**: Index route (lines 153-183)
- **Date formatting**: `format_date()` function (line 11)
- **Price formatting**: `format_price()` function (line 14)
- **Constants**: Lines 56-68 (ALLOW_DELETE, FILTERS, ALLOWED_EMAILS)
- **Templates**: `templates/` directory, all extend `base.html`
- **Static assets**: `static/css/` and `static/js/` (Bootstrap only)

---

## Technology Stack Summary

**Backend**: Flask 3.1.0, Python 3.x
**Database**: SQLite3 (stdlib)
**Security**: Werkzeug password hashing
**Templates**: Jinja2
**Frontend**: Bootstrap 5.x, minimal custom JS
**Session**: Flask built-in sessions (cookie-based)

**Missing Critical Dependencies**:
- Flask-WTF (forms & CSRF)
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (migrations)
- python-decouple (config)
- Flask-Limiter (rate limiting)
- gunicorn (production server)