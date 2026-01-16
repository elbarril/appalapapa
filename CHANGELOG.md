# Changelog

All notable changes to the Therapy Session Management Application will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.11.0] - 2026-01-15

### Added
- **Testing & Documentation** (Phase 6 of Frontend Refactoring Plan - FINAL PHASE)
  - Frontend test infrastructure with Playwright for visual, accessibility, and interaction tests
  - Comprehensive documentation in `docs/` directory:
    - `css-components.md` - CSS architecture, design tokens, component styles
    - `js-modules.md` - JavaScript module structure and API reference
    - `template-macros.md` - Jinja2 macro documentation with usage examples
    - `frontend-style-guide.md` - Coding standards and best practices
    - `frontend-contributing.md` - Contributor guidelines for frontend changes

### Changed
- **Test Requirements**: Added Playwright, pytest-playwright, and axe-playwright-python to `requirements/test.txt`
- **Test Structure**: New `tests/frontend/` directory with:
  - `conftest.py` - Playwright fixtures for browser testing
  - `test_visual.py` - Theme switching and responsive design tests
  - `test_accessibility.py` - WCAG compliance and keyboard navigation tests
  - `test_interactions.py` - User interaction and form submission tests

### Technical
- Frontend Refactoring Plan 100% complete (all 6 phases)
- 5 new documentation files in `docs/`
- 4 new frontend test files with Playwright
- All existing tests pass (134 tests)

---

## [2.10.0] - 2026-01-15

### Added
- **Performance Optimization** (Phase 5 of Frontend Refactoring Plan)
  - Self-hosted Nunito Sans fonts (no external Google Fonts dependency)
  - Self-hosted Bootstrap Icons (no external CDN dependency)
  - Font preloading for critical font file (improved LCP)
  - Static asset caching middleware with immutable cache headers for fonts

### Changed
- **Asset Loading**: Moved from CDN to self-hosted assets:
  - `static/fonts/` - Nunito Sans (latin, latin-ext) and Bootstrap Icons fonts
  - `static/css/base/_fonts.css` - Self-hosted @font-face declarations with font-display: swap
  - `static/css/bootstrap-icons.min.css` - Local Bootstrap Icons CSS
- **Template Optimization**: Updated `base.html` for better performance:
  - Added `<link rel="preload">` for critical font (improved FCP/LCP)
  - Added `defer` attribute to Bootstrap bundle script (non-blocking JS)
  - Self-hosted Bootstrap Icons instead of CDN
- **Middleware**: Added cache headers for static assets:
  - 1-year cache for CSS/JS files
  - Immutable cache for font files
  - Security headers now registered with middleware system

### Performance Impact
- Eliminated render-blocking external font request (Google Fonts)
- Eliminated external CDN request (Bootstrap Icons)
- Font display: swap prevents invisible text during font load
- Static assets cached for 1 year with proper cache headers

### Technical
- New `static/fonts/` directory with 4 self-hosted font files
- New `static/css/base/_fonts.css` for font-face declarations
- `app/middleware/security.py` enhanced with `add_cache_headers()` function
- `app/__init__.py` updated with `register_middleware()` function
- Zero functional regressions - all tests pass

## [2.9.0] - 2026-01-15

### Added
- **Template Component System** (Phase 4 of Frontend Refactoring Plan)
  - Reusable Jinja2 macro library for forms, cards, modals, and buttons
  - Partials for navbar, footer, and flash messages
  - Shared error page template macro

### Changed
- **Template Organization**: Created modular structure with macros and partials:
  - `macros/_forms.html` - Form input macros (text, password, email, select, date, number, textarea, checkbox)
  - `macros/_cards.html` - Card macros (patient_card, session_card, auth_card, empty_state)
  - `macros/_modals.html` - Modal macros (modal, confirm_modal, edit_modal, dashboard_modals)
  - `macros/_buttons.html` - Button macros (submit_button, cancel_button, form_buttons, cta_link)
  - `partials/_navbar.html` - Navbar partial extracted from base.html
  - `partials/_footer.html` - Footer partial extracted from base.html
  - `partials/_flash_messages.html` - Flash messages partial
  - `errors/_error_page.html` - Shared error page macro
- **Refactored Templates**: Simplified all templates to use macros:
  - Auth templates (login, register, change_password, reset_password) reduced by ~60%
  - Patient templates (form_person, list) reduced by ~50%
  - Session templates (form_session, form_edit) reduced by ~60%
  - Error templates (403, 404, 500) reduced by ~70%
- `base.html` now uses includes for navbar, footer, and flash messages

### Technical
- 8 new macro/partial files for reusable UI components
- Consistent accessibility patterns across all forms (ARIA attributes, error handling)
- Standardized HTML patterns eliminate duplication between templates
- Zero functional regressions - all 134 tests pass

## [2.8.0] - 2026-01-15

### Added
- **JavaScript Modularization** (Phase 3 of Frontend Refactoring Plan)
  - ES6 module architecture with `main.js` entry point
  - Comprehensive JSDoc documentation for all functions
  - Global error handlers for uncaught errors and promise rejections

### Changed
- **JavaScript File Organization**: Replaced monolithic `api.js` (1238 lines) with modular structure:
  - `modules/api/` - API client, patients, sessions, dashboard modules (4 files)
  - `modules/ui/` - Toast, modal, carousel, accessibility utilities (4 files)
  - `modules/components/` - Patient card, session card, filter buttons, dashboard renderer (4 files)
  - `modules/utils/` - Formatters, validators, helpers (3 files)
- Template `list.html` now uses `<script type="module">` for ES6 module support

### Removed
- Deleted legacy `api.js` file (functionality fully migrated to modules)

### Technical
- 15 new JavaScript modules organized by concern for better maintainability
- Type definitions via JSDoc for improved IDE support
- Separation of concerns: API calls, UI updates, and event handling in separate modules
- Backward compatibility maintained with `window` exports for onclick handlers
- Zero functional regressions - all 134 tests pass

## [2.7.0] - 2026-01-15

### Added
- **CSS Architecture Refactoring** (Phase 2 of Frontend Refactoring Plan)
  - Modular CSS structure with organized file hierarchy
  - New `main.css` entry point importing all CSS modules

### Changed
- **CSS File Organization**: Replaced monolithic `custom.css` with modular structure:
  - `base/` - Variables, reset, typography (3 files)
  - `components/` - Navbar, cards, buttons, forms, modals, carousel, alerts, badges (8 files)
  - `layout/` - Header, footer, containers (3 files)
  - `pages/` - Auth, dashboard, errors (3 files)
  - `themes/` - Light and dark theme variables (2 files)
  - `utilities/` - Animations, accessibility, helpers (3 files)
- Template base.html now links to `main.css` instead of `custom.css`

### Technical
- 22 new CSS files organized by concern for better maintainability
- CSS custom properties centralized in `_variables.css`
- Theme-specific overrides isolated in `themes/_light.css` and `themes/_dark.css`
- Improved code organization following CSS architecture best practices
- Zero visual regressions - all styling preserved in both dark and light themes

## [2.6.0] - 2026-01-15

### Added
- **WCAG 2.1 AA Accessibility Enhancements** (Phase 1 of Frontend Refactoring Plan)
  - **Color Contrast Fixes**: PENDIENTE badge now uses lighter gold (#d4a85a/#e0b86c) with dark text for 7.2:1+ contrast ratio
  - **Touch Target Improvements**: Carousel indicators now have 44x44px touch targets (WCAG minimum)
  - **ARIA Live Regions**: Toast notifications announce messages to screen readers with proper roles
  - **Screen Reader Announcements**: Filter changes and carousel navigation announced dynamically
  - **Modal Focus Management**: Focus trapped within modals, returns to trigger element on close
  - **Keyboard Navigation**: Carousels support Arrow Left/Right, Home/End key navigation
  - **Form Accessibility**: Login and register forms include aria-invalid, aria-describedby, role="alert" for errors
  - **Filter Button States**: aria-pressed attributes for toggle button accessibility

### Changed
- Carousel elements now have role="region", aria-roledescription="carrusel", and aria-label
- Filter buttons include aria-pressed state for screen readers
- Form inputs show visual required field indicators (asterisks)
- Toast close buttons have descriptive aria-label

### Technical
- Added `announceToScreenReader()` helper function for ARIA live region updates
- Added `trapFocusInModal()`, `getFocusableElements()` focus management utilities
- Added `enableCarouselKeyboardNav()` for keyboard accessibility
- Carousel slide changes announce position to screen readers

## [2.5.0] - 2026-01-15

### Added
- **Dashboard API Endpoint**: New `/api/v1/dashboard` endpoint for fetching filtered patient/session data
  - Supports `show` query parameter: `all`, `pending`, `paid`
  - Returns grouped sessions with patient info, filter metadata, and `allow_delete` flag
  - Full test coverage with 4 new integration tests

### Changed
- **JavaScript-based List Filtering**: Filter buttons now use AJAX instead of page reloads
  - Clicking TODOS/PENDIENTES/PAGADOS filters dynamically refresh the list
  - URL updates via `history.pushState()` for bookmarkable filters
  - No page reload required - instant filter switching
  - Filter state preserved in browser history

### Technical
- All 134 backend tests pass (including 4 new dashboard API tests)
- Backend route preserved for initial render and non-JS fallback
- Removed unused `toTitleCase()` function that incorrectly handled accented characters

## [2.4.0] - 2026-01-14

### Added
- **Custom Design System**: New `static/css/custom.css` with 580+ lines of styling
  - CSS custom properties for consistent theming across dark/light modes
  - Nunito Sans typography from Google Fonts (weights 400, 500, 600, 700)
  - MLC-inspired color palette: Teal #3F4A49, Beige #DCD9D0, Cream #F5F3EF
  - Card components, button styles, and form elements
  - Fade-in animations with staggered delays
  - Accessibility improvements (focus indicators, skip links)

### Changed
- **Complete UI Rebrand**: Inspired by Millennial Life Counseling website design
  - Teal (#3F4A49) navbar and footer with cream/white content areas
  - Centered auth cards with icon headers (login, register, reset password)
  - Dashboard with new header design and improved empty state
  - Form pages with minimalist card-based layouts
  - Error pages (403, 404, 500) with simple icon + message design

- **Improved Dark Mode Support**: Better theme consistency
  - Dark mode uses #1a1d1f backgrounds with teal #5a9a97 accents
  - Theme-adaptive CSS classes for seamless switching
  - Sun/moon toggle icons with smooth transitions

- **Enhanced Accessibility**:
  - Skip link "Saltar al contenido principal" for keyboard users
  - Improved ARIA labels on all interactive elements
  - Proper heading hierarchy (h1 → h2 → h3)
  - Visible focus indicators on buttons and links

- **Responsive Design Improvements**:
  - Mobile-first layouts for all pages
  - Proper button sizing for touch targets (44x44px minimum)
  - Hamburger menu on mobile with full navigation

### Technical
- All 130 backend tests continue to pass
- No breaking changes to routes, APIs, or database

## [2.3.0] - 2026-01-14

### Added
- **JavaScript API Client**: New `static/js/api.js` module for AJAX-based CRUD operations
  - Patient operations: `getPatient()`, `updatePatient()`, `deletePatient()`
  - Session operations: `getSession()`, `updateSession()`, `deleteSession()`, `toggleSessionPayment()`
  - UI helpers: `showToast()`, `formatDisplayDate()`, `formatPrice()`
  - Modal management functions for edit/delete operations
  - Toast notifications for real-time user feedback

- **REST API Enhancements**: Extended API v1 with new endpoints
  - `GET /api/v1/sessions/{id}` - Get single session details
  - `PUT /api/v1/patients/{id}` - Update patient via API
  - `PUT /api/v1/sessions/{id}` - Update session via API

- **API Integration Tests**: Comprehensive test coverage for all API endpoints
  - New `tests/integration/test_api.py` with 30+ test cases
  - Tests for patients API (list, get, create, update, delete)
  - Tests for sessions API (list, get, create, update, delete, toggle)
  - Tests for stats API and authentication requirements

### Changed
- **Dashboard Actions Without Page Refresh**: All patient and session actions now use JavaScript API
  - Edit patient: Opens modal, saves via API, updates UI instantly
  - Delete patient: Confirmation modal, deletes via API, removes card from UI
  - Edit session: Opens modal with session data, saves via API, updates carousel
  - Delete session: Confirmation modal, deletes via API, updates carousel
  - Toggle payment: Instant status toggle via API with visual feedback
  - Toast notifications replace flash messages for AJAX operations

- **Template Structure**: Updated `templates/patients/list.html`
  - Action buttons now use `onclick` handlers instead of `href` links
  - Added Bootstrap modals for edit/delete operations (patients and sessions)
  - Includes `api.js` script via `extra_js` block
  - Data attributes (`data-patient-id`, `data-session-id`) for JS targeting

### Documentation
- **Testing Requirements**: Added mandatory testing documentation
  - Test file organization mapping (which tests for which component)
  - Requirements to add tests for new features/modifications
  - Run `pytest` before marking any task complete
  
- **JavaScript API Documentation**: Added to project instructions
  - Available functions and their usage
  - Modal functions for UI interactions
  - How to include in templates

---

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
