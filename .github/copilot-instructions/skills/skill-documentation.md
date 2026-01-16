# Skill: Documentation Best Practices

> **Scope:** Documentation standards, patterns, and practices for Flask/Jinja2 web applications, covering code comments, API docs, README files, and project documentation.

---

## 1. Documentation Hierarchy

### Documentation Levels

```
Project Documentation
├── README.md              # Project overview, quick start
├── CHANGELOG.md           # Version history, changes
├── CONTRIBUTING.md        # How to contribute
├── docs/
│   ├── architecture.md    # System design
│   ├── api.md             # API reference
│   ├── deployment.md      # Deployment guide
│   └── user-guide.md      # End-user documentation
│
├── Code Documentation
│   ├── Module docstrings  # File-level docs
│   ├── Function docstrings# Function/method docs
│   ├── Inline comments    # Complex logic explanation
│   └── Type hints         # Parameter/return types
│
└── Frontend Documentation
    ├── JSDoc comments     # JavaScript documentation
    ├── CSS comments       # Style documentation
    └── Template comments  # Jinja2 macro docs
```

### Documentation Purpose

| Type | Audience | Purpose | Update Frequency |
|------|----------|---------|------------------|
| README | New developers, users | Quick start, overview | Major changes |
| CHANGELOG | All stakeholders | Track changes | Every release |
| API docs | Frontend devs, integrators | Endpoint reference | API changes |
| Code comments | Developers | Explain "why" | With code changes |
| Architecture | Team leads, new devs | System understanding | Architecture changes |

---

## 2. README.md Structure

### Template

```markdown
# Project Name

Brief description of what the project does and its main purpose.

## Features

- ✅ Feature 1 with brief explanation
- ✅ Feature 2 with brief explanation
- ✅ Feature 3 with brief explanation

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend build)

### Installation

```bash
# Clone repository
git clone https://github.com/username/project.git
cd project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db upgrade
flask db-utils seed

# Run development server
flask run
```

### Configuration

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
```

## Usage

Brief usage examples or link to user guide.

## Project Structure

```
app/
├── models/      # Database models
├── routes/      # View functions
├── services/    # Business logic
├── templates/   # Jinja2 templates
└── static/      # CSS, JS, images
```

## Development

### Running Tests

```bash
pytest                    # All tests
pytest tests/unit/        # Unit tests only
pytest --cov=app          # With coverage
```

### Code Style

- Python: Black formatter, isort for imports
- JavaScript: ESLint with Prettier
- CSS: Stylelint

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
```

---

## 3. CHANGELOG.md Format

### Keep a Changelog Standard

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New patient search functionality
- Export to PDF feature

### Changed
- Improved dashboard loading performance

### Fixed
- Session date validation for future dates

## [2.8.0] - 2024-01-15

### Added
- Dark/light theme toggle with system preference detection
- Keyboard shortcuts for common actions (Ctrl+N for new patient)
- Session payment status filters on dashboard

### Changed
- Migrated JavaScript to ES6 modules architecture
- Updated Bootstrap to 5.3.2
- Improved form validation error messages (Spanish)

### Fixed
- Calendar not showing correct month on page load
- Mobile menu not closing after navigation
- CSRF token expiration on long sessions

### Security
- Updated dependencies to address CVE-2024-XXXX

## [2.7.0] - 2024-01-01

### Added
- Modular CSS architecture with component files
- Patient notes field with rich text support

### Deprecated
- Legacy `custom.css` file (use `main.css` entry point)

### Removed
- jQuery dependency (replaced with vanilla JS)

[Unreleased]: https://github.com/username/project/compare/v2.8.0...HEAD
[2.8.0]: https://github.com/username/project/compare/v2.7.0...v2.8.0
[2.7.0]: https://github.com/username/project/releases/tag/v2.7.0
```

### Change Categories

| Category | Use For |
|----------|---------|
| **Added** | New features |
| **Changed** | Changes in existing functionality |
| **Deprecated** | Soon-to-be removed features |
| **Removed** | Removed features |
| **Fixed** | Bug fixes |
| **Security** | Security vulnerability fixes |

---

## 4. Python Documentation

### Module Docstrings

```python
# app/services/patient_service.py

"""
Patient Service Module

This module provides the business logic layer for patient (Person) operations.
It handles CRUD operations, validation, and data transformation between
the database models and the presentation layer.

Usage:
    from app.services.patient_service import PatientService
    
    # Create a new patient
    success, patient, message = PatientService.create(
        name='Juan Pérez',
        user_id=current_user.id
    )
    
    # Get paginated patients
    patients = PatientService.get_all_paginated(
        user_id=current_user.id,
        page=1,
        per_page=20
    )

Note:
    All methods return a tuple of (success: bool, result: Any, message: str)
    for consistent error handling across the application.

See Also:
    - app.models.person.Person: The Patient model
    - app.routes.patients: Route handlers using this service
"""

from typing import Optional, Tuple, Any
from app.models import Person, db
from app.utils.constants import PAGINATION_DEFAULT_PER_PAGE
```

### Function Docstrings (Google Style)

```python
def create(
    name: str,
    user_id: int,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    notes: Optional[str] = None
) -> Tuple[bool, Optional[Person], str]:
    """
    Create a new patient record.
    
    Creates a new Person instance associated with the given user.
    Performs input validation and handles database operations.
    
    Args:
        name: The patient's full name. Required, max 100 characters.
        user_id: The ID of the user (therapist) who owns this patient.
        phone: Optional phone number. Will be normalized to digits only.
        email: Optional email address. Must be valid format if provided.
        notes: Optional notes about the patient.
    
    Returns:
        A tuple containing:
            - success (bool): True if creation succeeded
            - patient (Person | None): The created patient or None on failure
            - message (str): Success or error message in Spanish
    
    Raises:
        This method catches all exceptions and returns them as error tuples.
        Check the success boolean rather than catching exceptions.
    
    Example:
        >>> success, patient, msg = PatientService.create(
        ...     name='María García',
        ...     user_id=1,
        ...     phone='11-2345-6789'
        ... )
        >>> if success:
        ...     print(f'Created patient: {patient.name}')
        ... else:
        ...     print(f'Error: {msg}')
    
    Note:
        - Names are automatically stripped and title-cased
        - Phone numbers are normalized to digits only
        - Email addresses are converted to lowercase
    """
    try:
        # Validate required fields
        if not name or not name.strip():
            return False, None, "El nombre es requerido."
        
        # Create patient
        patient = Person(
            name=name.strip().title(),
            user_id=user_id,
            phone=normalize_phone(phone) if phone else None,
            email=email.lower().strip() if email else None,
            notes=notes
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return True, patient, "Paciente creado exitosamente."
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating patient: {e}")
        return False, None, "Error al crear el paciente."
```

### Class Docstrings

```python
class PatientService:
    """
    Service layer for patient-related operations.
    
    This class provides a clean interface between the routes/views and
    the database models, encapsulating all business logic for patient
    management.
    
    All methods are static and follow the pattern of returning
    (success, result, message) tuples for consistent error handling.
    
    Attributes:
        None - This is a stateless service class with only static methods.
    
    Example:
        # In a route handler
        @bp.route('/patients', methods=['POST'])
        @login_required
        def create_patient():
            form = PersonForm()
            if form.validate_on_submit():
                success, patient, message = PatientService.create(
                    name=form.name.data,
                    user_id=current_user.id
                )
                flash(message, 'success' if success else 'error')
                if success:
                    return redirect(url_for('patients.list'))
            return render_template('patients/form.html', form=form)
    
    Note:
        This service handles soft deletes. Deleted patients have their
        `deleted_at` timestamp set but remain in the database.
    
    See Also:
        - SessionService: For therapy session operations
        - AuthService: For authentication operations
    """
```

### Inline Comments

```python
def calculate_monthly_stats(user_id: int, month: date) -> dict:
    """Calculate monthly statistics for a user."""
    
    # Get the date range for the month
    # We use monthrange to handle varying month lengths correctly
    _, last_day = monthrange(month.year, month.month)
    start_date = date(month.year, month.month, 1)
    end_date = date(month.year, month.month, last_day)
    
    # Query sessions with eager loading to avoid N+1
    # This single query replaces what would be multiple queries
    sessions = TherapySession.query.options(
        joinedload(TherapySession.person)
    ).filter(
        TherapySession.user_id == user_id,
        TherapySession.session_date.between(start_date, end_date),
        TherapySession.deleted_at.is_(None)  # Exclude soft-deleted
    ).all()
    
    # Calculate totals
    # Note: We use Decimal for currency to avoid floating-point errors
    total_earned = sum(s.price for s in sessions if s.paid)
    total_pending = sum(s.price for s in sessions if not s.paid)
    
    # Group by patient for the breakdown
    # Using defaultdict avoids KeyError checking
    by_patient = defaultdict(list)
    for session in sessions:
        by_patient[session.person_id].append(session)
    
    return {
        'total_sessions': len(sessions),
        'total_earned': total_earned,
        'total_pending': total_pending,
        'unique_patients': len(by_patient),
        'sessions_by_patient': dict(by_patient)
    }
```

---

## 5. JavaScript Documentation (JSDoc)

### Module Documentation

```javascript
/**
 * Patient API Module
 * 
 * Provides functions for interacting with the patient API endpoints.
 * All functions are async and return parsed JSON responses.
 * 
 * @module api/patients
 * @author Development Team
 * @since 2.8.0
 * 
 * @example
 * import { fetchPatients, createPatient } from './modules/api/patients.js';
 * 
 * // Fetch paginated patients
 * const { patients, total } = await fetchPatients({ page: 1 });
 * 
 * // Create new patient
 * const newPatient = await createPatient({ name: 'Juan Pérez' });
 */

import { apiClient, handleApiError } from './client.js';
```

### Function Documentation

```javascript
/**
 * Fetch paginated list of patients.
 * 
 * Retrieves patients for the current user with pagination support.
 * Results are cached for 5 minutes to reduce server load.
 * 
 * @async
 * @function fetchPatients
 * @param {Object} [options={}] - Fetch options
 * @param {number} [options.page=1] - Page number (1-indexed)
 * @param {number} [options.perPage=20] - Items per page (max 100)
 * @param {string} [options.search] - Optional search query
 * @param {boolean} [options.activeOnly=true] - Only return active patients
 * @returns {Promise<PaginatedResponse<Patient>>} Paginated patient list
 * @throws {ApiError} When the request fails
 * 
 * @example
 * // Basic usage
 * const result = await fetchPatients();
 * console.log(result.patients); // Array of patients
 * console.log(result.total);    // Total count
 * 
 * @example
 * // With pagination
 * const result = await fetchPatients({ page: 2, perPage: 10 });
 * 
 * @example
 * // With search
 * const result = await fetchPatients({ search: 'García' });
 * 
 * @see {@link createPatient} for creating new patients
 * @see {@link updatePatient} for updating existing patients
 */
export async function fetchPatients(options = {}) {
    const {
        page = 1,
        perPage = 20,
        search = '',
        activeOnly = true
    } = options;
    
    const params = new URLSearchParams({
        page: String(page),
        per_page: String(Math.min(perPage, 100)),
        active_only: String(activeOnly)
    });
    
    if (search) {
        params.set('search', search);
    }
    
    return apiClient.get(`/patients?${params}`);
}
```

### Type Definitions

```javascript
/**
 * @typedef {Object} Patient
 * @property {number} id - Unique patient ID
 * @property {string} name - Patient's full name
 * @property {string} [phone] - Phone number (optional)
 * @property {string} [email] - Email address (optional)
 * @property {string} [notes] - Additional notes (optional)
 * @property {boolean} isActive - Whether patient is active
 * @property {string} createdAt - ISO 8601 creation timestamp
 * @property {string} updatedAt - ISO 8601 last update timestamp
 */

/**
 * @typedef {Object} PaginatedResponse
 * @template T
 * @property {T[]} items - Array of items for current page
 * @property {number} total - Total number of items
 * @property {number} page - Current page number
 * @property {number} pages - Total number of pages
 * @property {boolean} hasNext - Whether there's a next page
 * @property {boolean} hasPrev - Whether there's a previous page
 */

/**
 * @typedef {Object} ApiError
 * @property {number} status - HTTP status code
 * @property {string} message - Error message
 * @property {Object} [errors] - Field-specific validation errors
 */
```

### Class Documentation

```javascript
/**
 * Toast notification manager.
 * 
 * Displays temporary notification messages to the user.
 * Supports multiple toast types and automatic dismissal.
 * 
 * @class ToastManager
 * @example
 * const toasts = new ToastManager('#toast-container');
 * toasts.show('Guardado exitosamente', 'success');
 * toasts.show('Error al guardar', 'error', { duration: 5000 });
 */
class ToastManager {
    /**
     * Create a toast manager.
     * 
     * @param {string|HTMLElement} container - Container selector or element
     * @param {Object} [options={}] - Default options
     * @param {number} [options.duration=3000] - Default display duration in ms
     * @param {string} [options.position='bottom-right'] - Toast position
     * @throws {Error} If container element not found
     */
    constructor(container, options = {}) {
        this.container = typeof container === 'string' 
            ? document.querySelector(container) 
            : container;
            
        if (!this.container) {
            throw new Error(`Toast container not found: ${container}`);
        }
        
        this.defaults = {
            duration: 3000,
            position: 'bottom-right',
            ...options
        };
    }
    
    /**
     * Display a toast notification.
     * 
     * @param {string} message - Message to display
     * @param {('success'|'error'|'warning'|'info')} [type='info'] - Toast type
     * @param {Object} [options={}] - Override default options
     * @param {number} [options.duration] - Display duration in ms
     * @param {boolean} [options.dismissible=true] - Show close button
     * @returns {HTMLElement} The created toast element
     */
    show(message, type = 'info', options = {}) {
        // Implementation...
    }
}
```

---

## 6. CSS Documentation

### File Header Comments

```css
/**
 * Cards Component
 * 
 * Styles for card-based layouts including patient cards,
 * session cards, and generic content cards.
 * 
 * @file static/css/components/_cards.css
 * @requires base/_variables.css
 * @since 2.7.0
 * 
 * Structure:
 * - .card                  Base card styles
 * - .card--patient         Patient-specific card variant
 * - .card--session         Session-specific card variant
 * - .card__header          Card header section
 * - .card__body            Card main content
 * - .card__footer          Card footer with actions
 * 
 * Usage:
 *   <article class="card card--patient">
 *     <header class="card__header">...</header>
 *     <div class="card__body">...</div>
 *     <footer class="card__footer">...</footer>
 *   </article>
 */
```

### Section Comments

```css
/* ==========================================================================
   Card Base Styles
   ========================================================================== */

.card {
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
}

/* Card Header
   --------------------------------------------------------------------------
   Contains title, status badge, and optional actions.
   Uses flexbox for alignment with space-between.
   ========================================================================== */

.card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
    border-bottom: 1px solid var(--card-border);
}

/* Card Variants
   --------------------------------------------------------------------------
   Modifier classes for different card types.
   Each variant may override colors, spacing, or add specific elements.
   ========================================================================== */

/**
 * Patient Card Variant
 * 
 * Used in the patient list/grid on the dashboard.
 * Includes avatar placeholder and status indicator.
 */
.card--patient {
    /* Slightly larger padding for patient cards */
    --card-padding: var(--spacing-lg);
}

/**
 * Session Card Variant
 * 
 * Used in the session carousel and session lists.
 * Includes payment status indicator with color coding.
 */
.card--session {
    /* Compact padding for carousel display */
    --card-padding: var(--spacing-md);
}
```

### Variable Documentation

```css
/**
 * Design Tokens
 * 
 * Central location for all CSS custom properties.
 * Organized by category for easy discovery and maintenance.
 * 
 * Categories:
 * - Colors: Brand colors, semantic colors, theme colors
 * - Typography: Font families, sizes, weights, line heights
 * - Spacing: Margin/padding scale based on 4px unit
 * - Borders: Radius values, border widths
 * - Shadows: Elevation levels for depth
 * - Transitions: Duration and easing functions
 * - Z-index: Stacking order management
 * 
 * @file static/css/base/_variables.css
 */

:root {
    /* ==========================================================================
       Brand Colors
       ========================================================================== */
    
    /**
     * Primary brand color - Teal
     * Used for: Primary buttons, links, active states
     * Contrast: Passes WCAG AA with white text
     */
    --mlc-teal: #3F4A49;
    
    /**
     * Secondary brand color - Beige
     * Used for: Borders, dividers, subtle backgrounds
     */
    --mlc-beige: #DCD9D0;
    
    /**
     * Background color - Cream
     * Used for: Page background in light mode
     */
    --mlc-cream: #F5F3EF;
    
    /* ==========================================================================
       Semantic Colors
       ========================================================================== */
    
    /** Success state - confirmations, positive feedback */
    --color-success: #198754;
    
    /** Warning state - cautions, pending actions */
    --color-warning: #ffc107;
    
    /** Error state - errors, destructive actions */
    --color-danger: #dc3545;
    
    /** Info state - neutral information */
    --color-info: #0dcaf0;
    
    /* ==========================================================================
       Typography Scale
       
       Based on a 1.25 ratio (Major Third)
       Base size: 16px (1rem)
       ========================================================================== */
    
    --font-size-xs: 0.75rem;    /* 12px - captions, badges */
    --font-size-sm: 0.875rem;   /* 14px - small text, labels */
    --font-size-base: 1rem;     /* 16px - body text */
    --font-size-lg: 1.125rem;   /* 18px - lead text */
    --font-size-xl: 1.25rem;    /* 20px - h4 */
    --font-size-2xl: 1.5rem;    /* 24px - h3 */
    --font-size-3xl: 1.875rem;  /* 30px - h2 */
    --font-size-4xl: 2.25rem;   /* 36px - h1 */
}
```

---

## 7. Jinja2 Template Documentation

### Macro Documentation

```html
{#
================================================================================
Form Field Macro

Renders a complete form field with label, input, help text, and error display.
Handles all Bootstrap 5 form styling and accessibility requirements.

Parameters:
    field (WTForms Field, required):
        The WTForms field instance to render.
    
    label (str, optional):
        Override the field's default label. If not provided,
        uses field.label.text.
    
    placeholder (str, optional):
        Placeholder text for the input. Default: none.
    
    help_text (str, optional):
        Help text displayed below the input. Default: none.
    
    input_class (str, optional):
        Additional CSS classes for the input element.
        Default: empty string.
    
    wrapper_class (str, optional):
        Additional CSS classes for the form-group wrapper.
        Default: 'mb-3'.
    
    required (bool, optional):
        Show required indicator (*). Auto-detected from validators
        if not specified.
    
    autofocus (bool, optional):
        Add autofocus attribute. Default: false.

Usage:
    {% from 'macros/_forms.html' import form_field %}
    
    {# Basic usage #}
    {{ form_field(form.name) }}
    
    {# With all options #}
    {{ form_field(
        form.email,
        label='Correo electrónico',
        placeholder='ejemplo@correo.com',
        help_text='Usaremos este correo para notificaciones',
        input_class='form-control-lg',
        autofocus=true
    ) }}

Accessibility:
    - Automatically associates label with input via 'for' attribute
    - Adds aria-describedby for help text and errors
    - Marks required fields with aria-required="true"
    - Uses aria-invalid="true" for fields with errors

See Also:
    - form_select: For dropdown fields
    - form_textarea: For multiline text
    - form_checkbox: For boolean fields
================================================================================
#}

{% macro form_field(
    field,
    label=none,
    placeholder=none,
    help_text=none,
    input_class='',
    wrapper_class='mb-3',
    required=none,
    autofocus=false
) %}
    {# Implementation #}
{% endmacro %}
```

### Block Documentation

```html
{#
================================================================================
Base Template

The root template that all pages extend. Provides the HTML skeleton,
common meta tags, CSS/JS includes, and extensible blocks.

Blocks:
    title         - Page title (appears in browser tab)
    meta          - Additional meta tags
    styles        - Additional CSS (after main.css)
    content       - Main page content
    scripts       - Additional JS (after main.js)
    modals        - Modal dialogs (at end of body)

Required Context:
    None - this template doesn't require any variables

Example:
    {% extends 'base.html' %}
    
    {% block title %}Pacientes{% endblock %}
    
    {% block content %}
    <main class="container">
        <h1>Lista de Pacientes</h1>
        ...
    </main>
    {% endblock %}

Notes:
    - Theme toggle is automatically included in navbar
    - Flash messages are automatically displayed
    - CSRF token is available as csrf_token() in forms
================================================================================
#}

<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
    <!-- Head content -->
</head>
</html>
```

---

## 8. API Documentation

### OpenAPI/Swagger Style

```yaml
# docs/api.yaml

openapi: 3.0.3
info:
  title: MLC Therapy API
  description: |
    REST API for the therapy session management application.
    
    ## Authentication
    All endpoints require authentication via session cookie.
    Login at `/login` to obtain a session.
    
    ## Error Handling
    Errors return JSON with `error` and `message` fields.
    
    ## Pagination
    List endpoints support `page` and `per_page` query parameters.
  version: 1.0.0

paths:
  /api/v1/patients:
    get:
      summary: List patients
      description: |
        Returns a paginated list of patients belonging to the 
        authenticated user.
      tags:
        - Patients
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
          description: Page number (1-indexed)
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
          description: Items per page
        - name: search
          in: query
          schema:
            type: string
          description: Search by patient name
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PatientListResponse'
        '401':
          description: Not authenticated
    
    post:
      summary: Create patient
      tags:
        - Patients
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatientCreate'
      responses:
        '201':
          description: Patient created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Patient'
        '400':
          description: Validation error
        '401':
          description: Not authenticated

components:
  schemas:
    Patient:
      type: object
      properties:
        id:
          type: integer
          example: 1
        name:
          type: string
          example: "Juan Pérez"
        phone:
          type: string
          nullable: true
          example: "11-2345-6789"
        email:
          type: string
          nullable: true
          example: "juan@example.com"
        is_active:
          type: boolean
          example: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
```

### Inline API Documentation

```python
# app/api/v1/resources.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

api_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_bp.route('/patients', methods=['GET'])
@login_required
def list_patients():
    """
    List patients for the authenticated user.
    
    GET /api/v1/patients
    
    Query Parameters:
        page (int): Page number, default 1
        per_page (int): Items per page, default 20, max 100
        search (str): Filter by name (case-insensitive contains)
        active_only (bool): Only return active patients, default true
    
    Returns:
        200: {
            "patients": [...],
            "total": 42,
            "page": 1,
            "pages": 3,
            "has_next": true,
            "has_prev": false
        }
        401: {"error": "unauthorized", "message": "Login required"}
    
    Example:
        curl -X GET "http://localhost:5000/api/v1/patients?page=1&per_page=10" \\
             -H "Cookie: session=..."
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    search = request.args.get('search', '')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    # Query implementation...
    
    return jsonify({
        'patients': [p.to_dict() for p in patients.items],
        'total': patients.total,
        'page': patients.page,
        'pages': patients.pages,
        'has_next': patients.has_next,
        'has_prev': patients.has_prev
    })
```

---

## 9. Documentation Checklist

### Project Documentation
- [ ] README.md with quick start guide
- [ ] CHANGELOG.md following Keep a Changelog
- [ ] CONTRIBUTING.md for contributors
- [ ] LICENSE file
- [ ] Architecture documentation

### Code Documentation
- [ ] Module docstrings in all Python files
- [ ] Function docstrings with Args/Returns/Raises
- [ ] Inline comments for complex logic
- [ ] Type hints on all functions

### Frontend Documentation
- [ ] JSDoc on all exported functions
- [ ] Type definitions for complex objects
- [ ] CSS file header comments
- [ ] Jinja2 macro documentation

### API Documentation
- [ ] All endpoints documented
- [ ] Request/response examples
- [ ] Error codes explained
- [ ] Authentication documented

---

## Related Skills

- [JSDoc Documentation](skill-jsdoc-documentation.md)
- [Style Guide](skill-style-guide.md)
- [Component Design](skill-component-design.md)
- [Error Handling](skill-error-handling.md)
