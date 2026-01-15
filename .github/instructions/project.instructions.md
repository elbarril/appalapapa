---
applyTo: '**'
---

# Project: Therapy Session Management Application

## Overview

Flask web app for managing patient therapy sessions with payment tracking.

- **Backend**: Flask 3.x, SQLAlchemy ORM, Flask-WTF forms
- **Frontend**: Jinja2, Bootstrap 5, modular CSS
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Language**: Spanish UI, English code

---

## Project Structure

```
app/
├── __init__.py          # App factory (create_app)
├── config.py            # Configuration classes
├── models/              # SQLAlchemy models (User, Person, TherapySession, AuditLog)
├── services/            # Business logic (patient_service, session_service, auth_service)
├── routes/              # Blueprints (auth, patients, sessions)
├── api/v1/              # REST API endpoints
├── validators/forms.py  # Flask-WTF form definitions
└── utils/constants.py   # All constants (SPANISH_DAYS, etc.)

static/css/
├── main.css             # Entry point - imports all modules
├── base/                # _variables.css, _reset.css, _typography.css
├── components/          # _navbar.css, _cards.css, _buttons.css, _forms.css, 
│                        # _modals.css, _carousel.css, _alerts.css, _badges.css
├── layout/              # _header.css, _footer.css, _containers.css
├── pages/               # _auth.css, _dashboard.css, _errors.css
├── themes/              # _light.css, _dark.css
└── utilities/           # _accessibility.css, _animations.css, _helpers.css

static/js/
├── main.js              # Entry point (ES6 module)
└── modules/
    ├── api/             # API client, patients, sessions, dashboard
    ├── ui/              # Toast, modal, carousel, accessibility
    ├── components/      # patientCard, sessionCard, filterButtons, dashboardRenderer
    └── utils/           # formatters, validators, helpers

templates/
├── base.html            # Base template with nav
├── auth/                # login.html, register.html, etc.
├── patients/            # list.html (dashboard), form_person.html
├── sessions/            # form_session.html, form_edit.html
└── errors/              # 403.html, 404.html, 500.html

tests/
├── unit/                # test_models.py, test_services.py, test_validators.py
└── integration/         # test_api.py, test_*_routes.py
```

---

## Coding Conventions

### Database Access
```python
# ✅ Use service layer
from app.services.patient_service import PatientService
success, person, message = PatientService.create(name='John', user_id=user.id)

# ❌ Don't access DB directly in routes
```

### Form Validation
```python
# ✅ Use Flask-WTF
from app.validators.forms import PersonForm
form = PersonForm()
if form.validate_on_submit():
    name = form.name.data.strip()
```

### Error Handling
```python
try:
    success, result, message = SomeService.do_something()
    flash(message, 'success' if success else 'error')
except Exception as e:
    current_app.logger.error(f"Error: {e}")
    flash("Error inesperado.", "error")
    db.session.rollback()
```

### Date Formatting (Always Spanish)
```python
# ✅ Backend: use format_date from app.utils.formatters
from app.utils.formatters import format_date
formatted = format_date(session.session_date)  # "Lunes 15/01/2024"
```
```javascript
// ✅ Frontend: use formatDisplayDate from api.js
const formatted = formatDisplayDate('2024-01-15');  // "Lunes 15/01/2024"
```

### Constants
All constants go in `app/utils/constants.py`:
- SPANISH_DAYS, SPANISH_MONTHS
- MAX_PRICE, PAGINATION settings
- USER_ROLES, PAYMENT_STATUS

---

## CSS Architecture (v2.7.0+)

### File Organization

| Directory | Purpose | Files |
|-----------|---------|-------|
| `base/` | Design tokens | `_variables.css`, `_reset.css`, `_typography.css` |
| `components/` | UI components | `_navbar.css`, `_cards.css`, `_buttons.css`, `_forms.css`, `_modals.css`, `_carousel.css`, `_alerts.css`, `_badges.css` |
| `layout/` | Page structure | `_header.css`, `_footer.css`, `_containers.css` |
| `pages/` | Page-specific | `_auth.css`, `_dashboard.css`, `_errors.css` |
| `themes/` | Theme variables | `_light.css`, `_dark.css` |
| `utilities/` | Helpers | `_accessibility.css`, `_animations.css`, `_helpers.css` |

### Adding New Styles

1. Identify the appropriate file based on component type
2. Use CSS variables from `_variables.css`:
   ```css
   .my-component {
       color: var(--text-primary);
       padding: var(--spacing-md);
       border-radius: var(--radius-md);
   }
   ```
3. Theme-specific overrides go in `_light.css` or `_dark.css`:
   ```css
   [data-bs-theme="light"] .my-component {
       background-color: var(--mlc-cream);
   }
   ```

### Key CSS Variables

```css
/* Colors */
--mlc-teal: #3F4A49;
--mlc-beige: #DCD9D0;
--mlc-cream: #F5F3EF;

/* Typography (WCAG 2.1 AA: 14px min) */
--font-size-xs: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */

/* Spacing */
--spacing-sm: 0.5rem;
--spacing-md: 1rem;
--spacing-lg: 1.5rem;
```

---

## Template/JavaScript Sync

When modifying `templates/patients/list.html`, also update `static/js/api.js`:

| Template Element | JS Function |
|------------------|-------------|
| Session card buttons | `updateSessionButtons()` |
| Patient grid | `renderPatientsList()` |
| Session carousel | `renderSessionsCarousel()` |

---

## Commands

### CLI
```powershell
.\venv\Scripts\Activate.ps1; flask db-utils seed     # Seed test data
.\venv\Scripts\Activate.ps1; flask user create EMAIL # Create user
```

### Testing
```powershell
.\venv\Scripts\Activate.ps1; pytest                  # All tests
.\venv\Scripts\Activate.ps1; pytest tests/unit/      # Unit only
.\venv\Scripts\Activate.ps1; pytest tests/integration/ # Integration only
```

---

## Frontend Verification

Use MCP Chrome DevTools for each UI change:

1. **Navigate**: `mcp_chrome-devtoo_new_page` → `http://localhost:5000/`
2. **Login**: credentials `test@example.com` / `test123`
3. **Screenshot**: `mcp_chrome-devtoo_take_screenshot`
4. **Theme toggle**: Test both dark and light modes
5. **Responsive**: Test at 375px, 768px, 1200px

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `app/__init__.py` | App factory |
| `app/services/*.py` | Business logic |
| `app/utils/constants.py` | All constants |
| `static/css/main.css` | CSS entry point |
| `static/css/base/_variables.css` | Design tokens |
| `static/js/api.js` | JavaScript API client |
| `templates/base.html` | Base template |
| `tests/conftest.py` | Test fixtures |

---

## Anti-Patterns

❌ Direct DB access in routes (use services)
❌ Constants outside `constants.py`
❌ Inline styles or `!important`
❌ Locale-dependent date formatting
❌ Template changes without `api.js` sync
❌ Skipping theme testing (dark + light)
❌ Hardcoded Spanish text in multiple files
