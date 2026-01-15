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

### 6. Date Formatting (Always Spanish)
All dates must be formatted in Spanish for display. **Never rely on system locale**.

**Backend (Python)**:
```python
# ✅ Use format_date from app.utils.formatters
from app.utils.formatters import format_date

# Returns: "Lunes 15/01/2024"
formatted = format_date(session.session_date)
```

**Frontend (JavaScript)**:
```javascript
// ✅ Use formatDisplayDate from api.js
// Returns: "Lunes 15/01/2024"
const formatted = formatDisplayDate('2024-01-15');
```

**NEVER use**:
- `strftime('%A')` - depends on system locale
- `toLocaleDateString()` without explicit Spanish weekday lookup
- Any locale-dependent date formatting

### 7. Constants Management
All magic numbers, strings, and reusable values MUST be defined in `app/utils/constants.py`.

```python
# ✅ CORRECT - Define constants in constants.py
# In app/utils/constants.py:
SPANISH_DAYS = ["Lunes", "Martes", ...]
MAX_PRICE = 1_000_000

# In other files, import from constants:
from app.utils.constants import SPANISH_DAYS, MAX_PRICE

# ❌ AVOID - Defining constants in other files
# Don't define reusable constants in formatters.py, services, etc.
```

**What belongs in constants.py**:
- Feature flags (ALLOW_DELETE, etc.)
- Filter values and labels
- Pagination settings
- Rate limiting values
- Audit action types
- User roles
- Payment status values
- Flash message categories
- Validation limits (min/max values)
- Date format strings
- Spanish day/month names
- Any value used in multiple files

### 8. Template and JavaScript Synchronization (CRITICAL)
The `static/js/api.js` file dynamically generates HTML that must match template structure.

**⚠️ ALWAYS check `api.js` when modifying these templates:**
- `templates/patients/list.html` - Session cards, patient cards, carousels
- Any template with AJAX/dynamic content updates

**Functions in `api.js` that generate HTML:**
| Function | Generates HTML for |
|----------|-------------------|
| `updateSessionButtons()` | Session card footer buttons |
| `removeSessionFromUI()` | Carousel indicator updates |
| `removePatientFromUI()` | Empty state messages |
| `renderPatientsList()` | Full patient grid from dashboard API |
| `renderSessionsCarousel()` | Session carousel per patient |

**When modifying session/patient card templates:**
1. Update the template HTML structure
2. **Immediately update corresponding `api.js` functions**
3. Ensure CSS classes match between template and JS
4. Verify button labels, icons, and aria-labels match
5. Test both server-rendered and JS-updated states

**Example sync points:**
```html
<!-- Template (list.html) -->
<button class="btn btn-success flex-fill toggle-payment-btn">
    <i class="bi bi-check-circle me-1"></i>Pagado
</button>
```
```javascript
// api.js - must match exactly
btnGroup.innerHTML = `
    <button class="btn btn-success flex-fill toggle-payment-btn">
        <i class="bi bi-check-circle me-1"></i>Pagado
    </button>
`;
```

### 9. Template Organization
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
| `app/api/v1/resources.py` | REST API endpoints |
| `app/validators/forms.py` | Flask-WTF form definitions |
| `templates/base.html` | Base template with navigation |
| `templates/auth/*.html` | Authentication templates (login, register) |
| `templates/patients/*.html` | Patient management templates |
| `templates/sessions/*.html` | Session management templates |
| `templates/errors/*.html` | Error pages (403, 404, 500) |
| `static/js/api.js` | JavaScript API client for AJAX operations |
| `tests/conftest.py` | Pytest fixtures |
| `tests/integration/test_api.py` | API endpoint tests |

---

## JavaScript API Client (`static/js/api.js`)

The application uses a JavaScript API client for CRUD operations without page refresh.

### Available Functions

#### Patient Operations
```javascript
// Get a patient by ID
const patient = await getPatient(patientId);

// Update a patient
const updated = await updatePatient(patientId, { name, notes });

// Delete a patient (soft delete)
await deletePatient(patientId);
```

#### Session Operations
```javascript
// Get a session by ID
const session = await getSession(sessionId);

// Update a session
const updated = await updateSession(sessionId, { 
    session_date, 
    session_price, 
    pending, 
    notes 
});

// Delete a session (soft delete)
await deleteSession(sessionId);

// Toggle payment status
const result = await toggleSessionPayment(sessionId);
```

#### Dashboard Operations
```javascript
// Get dashboard data with filter
const data = await getDashboardData('all'); // 'all', 'pending', 'paid'

// Apply filter and refresh list dynamically
await applyFilter('pending'); // Updates URL and re-renders patient list
```

#### UI Helpers
```javascript
// Show toast notification
showToast(message, type);  // type: 'success', 'error', 'warning', 'info'

// Format date for display
const formatted = formatDisplayDate('2026-01-14');

// Format price
const price = formatPrice(150.00);
```

### Modal Functions (Used in list.html)
```javascript
// Open edit patient modal
openEditPatientModal(patientId, patientName);

// Open delete patient confirmation
openDeletePatientModal(patientId, patientName);

// Open edit session modal
openEditSessionModal(sessionId, personId);

// Open delete session confirmation
openDeleteSessionModal(sessionId, sessionDate);

// Toggle payment status
togglePayment(sessionId);
```

### Adding to Templates
```html
{% block extra_js %}
    <script src="{{ url_for('static', filename='js/api.js') }}"></script>
{% endblock extra_js %}
```

---

## Environment Variables (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `FLASK_CONFIG` | Configuration name | `development` |
| `DATABASE_URL` | Database connection | `sqlite:///instance/database.db` |
| `SENTRY_DSN` | Sentry error tracking (prod) | `https://...` |

---

## CLI Commands

**IMPORTANT**: Always activate the virtual environment before running Flask commands.

```powershell
# Windows PowerShell - Always activate venv first, then run command
.\venv\Scripts\Activate.ps1; flask db init-db          # Initialize tables
.\venv\Scripts\Activate.ps1; flask db seed             # Seed sample data
.\venv\Scripts\Activate.ps1; flask db backup           # Backup database

# Users
.\venv\Scripts\Activate.ps1; flask user create EMAIL   # Create new user
.\venv\Scripts\Activate.ps1; flask user list           # List all users
.\venv\Scripts\Activate.ps1; flask user set-role EMAIL ROLE
```

```bash
# macOS/Linux - Always activate venv first
source venv/bin/activate && flask db init-db
source venv/bin/activate && flask db seed
# etc.
```

---

## Testing Commands

**CRITICAL**: Always activate virtual environment BEFORE running pytest. Chain commands to avoid failures.

```powershell
# Windows PowerShell - Chain venv activation with pytest
.\venv\Scripts\Activate.ps1; pytest                    # All tests
.\venv\Scripts\Activate.ps1; pytest -v                 # Verbose
.\venv\Scripts\Activate.ps1; pytest --cov=app          # With coverage
.\venv\Scripts\Activate.ps1; pytest tests/unit/        # Unit tests only
.\venv\Scripts\Activate.ps1; pytest tests/integration/ # Integration tests only
```

```bash
# macOS/Linux
source venv/bin/activate && pytest                    # All tests
source venv/bin/activate && pytest -v                 # Verbose
source venv/bin/activate && pytest --cov=app          # With coverage
```

**Why chain commands?** Running `pytest` without activating venv first will fail because the dependencies are not available in the system Python.

---

## Visual Verification with MCP Chrome DevTools (Frontend Changes)

⚠️ **CRITICAL: Test with Chrome DevTools AFTER EVERY SINGLE UI CHANGE before proceeding to the next change.**

When modifying templates or frontend files, **always use MCP Chrome DevTools** to verify changes work correctly in the browser. This is **MANDATORY** for frontend verification.

### MCP Chrome DevTools Verification Workflow (REQUIRED FOR EACH CHANGE)

**⚠️ WORKFLOW: Make ONE change → Verify with Chrome → Fix if needed → Proceed to next change**

**DO NOT batch multiple UI changes without verification between each one.**

**For EACH individual frontend modification:**

1. **Navigate to the page**:
   ```
   mcp_chrome-devtoo_new_page → url: "http://localhost:5000/"
   ```

2. **Login if needed** (for authenticated pages):
   ```
   mcp_chrome-devtoo_take_snapshot  → Get current page elements
   mcp_chrome-devtoo_fill_form      → Fill login form with test credentials
   mcp_chrome-devtoo_click          → Click login button
   ```
   - Test credentials: `test@example.com` / `test123`

3. **Take a snapshot** to understand page structure:
   ```
   mcp_chrome-devtoo_take_snapshot
   ```

4. **Take a screenshot** to verify visual appearance:
   ```
   mcp_chrome-devtoo_take_screenshot
   ```

5. **Test CSS changes live** before modifying templates:
   ```
   mcp_chrome-devtoo_evaluate_script → Inject CSS/JS to test changes
   ```

6. **Test both themes** (MANDATORY):
   - Click the theme toggle button to switch between dark/light mode
   - Take screenshots in **BOTH** modes to verify consistency
   ```
   mcp_chrome-devtoo_click → uid of theme toggle button
   mcp_chrome-devtoo_take_screenshot
   ```

7. **Test responsive design**:
   ```
   mcp_chrome-devtoo_resize_page → width: 375, height: 667  (mobile)
   mcp_chrome-devtoo_take_screenshot
   mcp_chrome-devtoo_resize_page → width: 768, height: 1024 (tablet)
   mcp_chrome-devtoo_take_screenshot
   mcp_chrome-devtoo_resize_page → width: 1200, height: 800 (desktop)
   mcp_chrome-devtoo_take_screenshot
   ```

8. **Verify interactions work**:
   ```
   mcp_chrome-devtoo_click  → Test buttons, links
   mcp_chrome-devtoo_hover  → Test hover states
   mcp_chrome-devtoo_fill   → Test form inputs
   ```

9. **ONLY after verification passes, proceed to the next change**

⚠️ **Repeat steps 1-8 for EACH individual UI modification. Never batch multiple changes without verification.**

### Test Credentials for Development

| Email | Password | Role | Notes |
|-------|----------|------|-------|
| `test@example.com` | `test123` | admin | Created by `flask db-utils seed` |

**Setup test user** (if not exists):
```powershell
# Windows
.\venv\Scripts\Activate.ps1; flask db-utils seed
```
```bash
# macOS/Linux
source venv/bin/activate && flask db-utils seed
```

### Dark Mode / Light Mode Testing (MANDATORY)

**Every frontend change MUST be verified in both themes:**

1. **Default is dark mode** (`data-bs-theme="dark"`)
2. **Test in dark mode first**, take screenshot
3. **Click theme toggle** (sun/moon icon in navbar)
4. **Test in light mode**, take screenshot
5. **Verify both screenshots** show correct styling

**Theme-Aware CSS Guidelines:**
```html
<!-- ✅ DO: Use Bootstrap theme-adaptive classes -->
<div class="bg-body">           <!-- Adapts to theme -->
<div class="text-body">          <!-- Adapts to theme -->
<div class="border-secondary">   <!-- Adapts to theme -->
<small class="text-body-secondary">  <!-- Adapts to theme -->

<!-- ❌ DON'T: Use hardcoded colors -->
<div class="bg-light">           <!-- Breaks in dark mode -->
<div class="bg-dark">            <!-- Breaks in light mode -->
<span style="color: #333;">      <!-- Won't adapt -->
```

**Button Consistency Across Themes:**
| Action | Class | Works in Both Themes |
|--------|-------|---------------------|
| Edit | `btn-outline-secondary` | ✅ |
| Success/Confirm | `btn-success` | ✅ |
| Warning/Pending | `btn-outline-warning` | ✅ |
| Danger/Delete | `btn-outline-danger` | ✅ |
| Primary action | `btn-primary` | ✅ |

### Fallback: VS Code Simple Browser

If MCP Chrome DevTools is unavailable, use VS Code's Simple Browser:

1. **Start the server**:
   ```powershell
   .\venv\Scripts\Activate.ps1; flask run
   ```

2. **Open Simple Browser**: `http://localhost:5000`
   - Note: Simple Browser is view-only (cannot fill forms)
   - Login via external browser first for authenticated pages

3. **Take screenshots** using VS Code's screenshot capabilities

### Visual Verification Checklist

⚠️ **Apply this checklist AFTER EVERY SINGLE UI CHANGE, not just at the end of the task.**

Before proceeding to the next change, verify:

- [ ] **Screenshot taken**: Captured current state with Chrome DevTools
- [ ] **Change looks correct**: Visual appearance matches expectation
- [ ] **Dark mode**: UI renders correctly
- [ ] **Light mode**: UI renders correctly (click theme toggle)
- [ ] **Mobile (375px)**: Layout is responsive (if applicable to change)
- [ ] **Desktop (1200px+)**: Layout uses available space well
- [ ] **Buttons**: Full width, equal sizing, visible text + icons
- [ ] **Text**: Readable, properly aligned, not truncated
- [ ] **Forms**: Labels visible, inputs styled correctly
- [ ] **Accessibility**: ARIA labels present, focus indicators visible
- [ ] **Interactions**: Buttons clickable, modals open correctly

**Only proceed to the next change after verification passes.**

### Common Issues to Check
- Navigation arrows overlapping content (carousels)
- Text overflow/truncation
- Button alignment and spacing
- Card/grid layout responsiveness
- Flash message visibility
- Missing focus indicators
- Poor color contrast
- **Dark mode compatibility**: Colors adapt correctly
- **Light mode compatibility**: Colors adapt correctly
- **Theme switcher**: Toggle works and persists across page reloads

---

## Backend Testing Workflow (Backend Changes ONLY)

⚠️ **IMPORTANT: Only run backend tests when backend files are modified.**

**When to run pytest:**
- ✅ After modifying files in `app/models/`, `app/services/`, `app/routes/`, `app/validators/`, `app/utils/`, `app/middleware/`, `app/api/`
- ❌ **DO NOT run pytest for frontend-only changes** (templates, CSS, JavaScript)

**If the request is ONLY for frontend/UI changes:**
- Skip `pytest` entirely
- Focus on MCP Chrome DevTools visual verification after EACH change
- Only verify in browser, not with backend tests

When modifying any backend file, **always run tests** to verify:

### Mandatory Testing Steps (Backend Only)
1. **Run full test suite** (always activate venv first):
   ```powershell
   # Windows PowerShell - chain venv activation
   .\venv\Scripts\Activate.ps1; pytest
   ```
   ```bash
   # macOS/Linux
   source venv/bin/activate && pytest
   ```

2. **Run specific test category** based on change:
   ```powershell
   # For model changes
   .\venv\Scripts\Activate.ps1; pytest tests/unit/test_models.py -v
   
   # For service changes
   .\venv\Scripts\Activate.ps1; pytest tests/unit/test_services.py -v
   
   # For route changes
   .\venv\Scripts\Activate.ps1; pytest tests/integration/ -v
   
   # For form/validator changes
   .\venv\Scripts\Activate.ps1; pytest tests/unit/test_validators.py -v
   ```

3. **Check for failures**: All tests must pass before marking complete

4. **Add new tests**: If new functionality lacks test coverage, write tests

5. **Run with coverage** (optional but recommended):
   ```powershell
   .\venv\Scripts\Activate.ps1; pytest --cov=app --cov-report=term-missing
   ```

### When to Run Tests
- ✅ After modifying any file in `app/models/`
- ✅ After modifying any file in `app/services/`
- ✅ After modifying any file in `app/routes/`
- ✅ After modifying any file in `app/validators/`
- ✅ After modifying any file in `app/utils/`
- ✅ After modifying any file in `app/middleware/`
- ✅ After modifying any file in `app/api/`

### Test File Organization
| Component Modified | Test File |
|--------------------|-----------|
| API endpoints (`app/api/`) | `tests/integration/test_api.py` |
| Patient routes | `tests/integration/test_patient_routes.py` |
| Session routes | `tests/integration/test_session_routes.py` |
| Auth routes | `tests/integration/test_auth_routes.py` |
| Models | `tests/unit/test_models.py` |
| Services | `tests/unit/test_services.py` |
| Validators/Forms | `tests/unit/test_validators.py` |

### When to Add New Tests
- ✅ New API endpoint added → Add test in `test_api.py`
- ✅ New route added → Add test in appropriate route test file
- ✅ New service method → Add test in `test_services.py`
- ✅ New model method → Add test in `test_models.py`
- ✅ Bug fixed → Add regression test to prevent recurrence
- ✅ Feature modified → Update existing tests to reflect changes

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
❌ Batch multiple UI changes without Chrome DevTools verification between each
❌ Proceed to next UI change without verifying the current one first
❌ Run pytest for frontend-only changes (waste of time, not relevant)
❌ Skip running pytest after backend modifications
❌ Ignore test failures and proceed with changes
❌ Create UI elements without ARIA labels
❌ Use color alone to convey information
❌ Skip keyboard navigation testing
❌ Create cluttered, complex UI layouts
❌ Add decorative elements that don't serve function
❌ Define constants outside `app/utils/constants.py`
❌ Use locale-dependent date formatting (strftime %A, toLocaleDateString)
❌ Modify template HTML structure without updating `api.js`
❌ Hardcode Spanish day/month names in multiple files