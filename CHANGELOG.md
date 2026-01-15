# Changelog

All notable changes to the Therapy Session Management Application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.1] - 2026-01-14

### Fixed
- **Docker Build Issues**: Fixed production Docker image build failures
  - Added missing `templates/` and `static/` directories to production stage
  - Removed non-existent `migrations/` folder reference from Dockerfile
  - Changed healthcheck from `curl` to Python `urllib` (avoids extra package install)
  - Added `logs/` directory creation in production image
  - Created `.dockerignore` to optimize build context and reduce image size
  
- **Configuration Consistency**: Fixed environment variable handling
  - Unified `FLASK_CONFIG` and `FLASK_ENV` support across all entry points
  - `wsgi.py`, `run.py`, and `create_app()` now consistently check both variables
  - Added SQLite fallback in production config for container testing scenarios
  
- **Docker Compose Production**: Improved production deployment configuration
  - Fixed `DATABASE_URL` to properly connect to PostgreSQL service using service name
  - Uses environment variable interpolation for database credentials

---

## [2.2.0] - 2026-01-14

### Added
- **Dark Mode with Theme Switcher**: Full dark mode support with user preference persistence
  - Dark mode enabled by default using Bootstrap 5.3's `data-bs-theme` attribute
  - Theme switcher button in navbar (sun/moon icons) for toggling between light and dark modes
  - User preference saved to localStorage and persists across sessions
  - Smooth CSS transitions when switching themes
  - Full accessibility: keyboard navigation, ARIA labels, focus indicators
  - Script runs before page load to prevent flash of incorrect theme

### Changed
- **Improved Dark Mode UI Compatibility**: Updated all UI components for proper dark mode support
  - Patient card headers: Removed `bg-light` class, now use theme-adaptive `border-bottom`
  - Filter buttons: Changed to `btn-outline-light` for better visibility in dark mode
  - Session action buttons: Updated color scheme for better contrast
    - Edit button: `btn-outline-light` (high contrast)
    - Mark as paid: `btn-success` (green, semantic match to PAGADO badge)
    - Mark as pending: `btn-outline-warning` (yellow, semantic match to pending state)
  - Carousel navigation: Replaced `filter: invert()` hack with Bootstrap Icons (`bi-chevron-left/right`)
  - Text colors: Updated from `text-muted` to `text-body-secondary` for theme adaptability
  - Delete buttons: Changed to `btn-outline-danger` for cleaner minimalist look

### Fixed
- **Accessibility Improvements**:
  - Filter buttons now wrapped in `btn-group` with `role="group"` and `aria-label`
  - Carousel navigation buttons have descriptive `aria-label` including patient name
  - Patient header layout improved with proper flex spacing (`gap-2`, `flex-grow-1`)

---

## [2.1.2] - 2026-01-14

### Changed
- **Icon-Only Action Buttons**: Replaced text buttons with accessible icon-only buttons
  - Patient edit/delete buttons now use Bootstrap Icons (`bi-pencil`, `bi-trash`)
  - Session edit/mark/delete buttons use icons (`bi-pencil-square`, `bi-check-circle`, `bi-clock-history`, `bi-trash`)
  - Added Bootstrap Icons CDN to base template
  - Full accessibility preserved with `aria-label`, `title`, and `visually-hidden` text
  - Button groups use `role="group"` with descriptive `aria-label`

---

## [2.1.1] - 2026-01-14

### Fixed
- **Session Persistence**: Fixed issue where users were logged out when navigating between pages
  - Changed Flask-Login session protection from `'strong'` to `'basic'` for development/testing
  - Added `SESSION_PROTECTION` config setting per environment
  - Production maintains `'strong'` session protection for security

---

## [2.1.0] - 2026-01-14

### Added
- **Session Cards Slider**: Patient sessions now display as Bootstrap 5 Carousel cards
  - Each patient's sessions are presented in a swipeable/navigable card slider
  - Carousel indicators show session count and current position
  - Previous/Next navigation controls for multiple sessions
  - Responsive card design with session counter (e.g., "Sesión 1 de 3")
  - Uses native Bootstrap 5 Carousel component (no additional dependencies)

### Changed
- `templates/patients/list.html`: Replaced list-group layout with Bootstrap Carousel for sessions

---

## [2.0.0] - 2026-01-14

### Added - Major Refactoring
This release represents a complete architectural overhaul of the application.

#### Architecture
- **Factory Pattern**: Application now uses `create_app()` factory for better testability
- **Blueprints**: Routes organized into `auth`, `patients`, `sessions`, and `main` blueprints
- **Service Layer**: Business logic moved to dedicated service classes
- **Model Mixins**: Reusable `TimestampMixin`, `SoftDeleteMixin`, and `AuditMixin`

#### Templates Reorganization
- Reorganized templates into module-based subdirectories:
  - `templates/auth/` - login, register, reset_password, change_password
  - `templates/patients/` - list, form_person, delete_person
  - `templates/sessions/` - form_session, form_edit
  - `templates/errors/` - 403, 404, 500
- Added CSRF protection to all forms with `{{ form.hidden_tag() }}`
- Updated to use Flask-WTF form field rendering
- Updated navigation for Flask-Login `current_user.is_authenticated`
- Added flash message categories with Bootstrap alert styling

#### Security
- **CSRF Protection**: Flask-WTF integrated on all forms
- **Rate Limiting**: Flask-Limiter on authentication routes
- **Password Hashing**: Werkzeug secure password hashing
- **Security Headers**: Custom middleware for X-Frame-Options, etc.
- **Role-Based Access**: Admin, Therapist, Viewer roles

#### Database
- **SQLAlchemy ORM**: Replaced raw SQLite queries with SQLAlchemy 2.0+
- **Flask-Migrate**: Database migrations with Alembic
- **Soft Delete**: Recoverable data deletion with timestamps
- **Audit Logging**: Track all CRUD operations with user attribution
- **Foreign Keys**: Proper relationship constraints in AuditMixin

#### Testing
- **pytest Framework**: 104 tests passing
- **Unit Tests**: Models, services, validators
- **Integration Tests**: Authentication, patient, session routes
- **Fixtures**: Reusable test data in conftest.py

#### Dependencies
- Updated `requirements.txt` with all new dependencies
- Split requirements by environment: base, dev, test, prod

### Changed
- Base template updated with responsive navigation
- Flash messages now support categories (success, error, warning, info)
- URL routes use blueprint prefixes (e.g., `url_for('auth.login')`)
- Template path configuration moved to app factory

### Fixed
- SQLAlchemy relationship configuration with proper ForeignKey constraints
- Template folder path resolution for modular app structure
- Test for SessionForm validation with SelectField choices

### Security
- Environment variables for all secrets
- No hardcoded credentials in source code
- CSRF tokens on all POST/PUT/DELETE forms

---

## [1.0.0] - 2025-XX-XX (Legacy)

### Initial Release
- Monolithic Flask application
- SQLite database with raw SQL queries
- Basic authentication with hardcoded secrets
- Single-file application structure

---

## Migration Notes

### From 1.x to 2.0

1. **Database Migration**: Run `flask db upgrade` after updating code
2. **Environment Variables**: Copy `.env.example` to `.env` and configure
3. **Templates**: Templates moved to subdirectories - update custom templates
4. **URL References**: Update `url_for()` calls to use blueprint prefixes:
   - `url_for('login')` → `url_for('auth.login')`
   - `url_for('index')` → `url_for('patients.index')`
   - `url_for('add_session')` → `url_for('sessions.add_session')`
