# Frontend Refactoring Master Plan

## Executive Summary

This document outlines a comprehensive frontend refactoring plan for the Therapy Session Management Application. The plan is organized into **6 phases**, each with specific goals, deliverables, and skill requirements. The refactoring focuses on:

- **Accessibility (WCAG 2.1 AA Compliance)**
- **Scalability & Architecture**
- **Performance Optimization**
- **Code Readability & Maintainability**
- **Best Practices & Modern Standards**

---

## Current State Analysis

### Strengths Identified ✅

1. **Dark/Light Theme Support**: Excellent theme switching with localStorage persistence
2. **Semantic HTML**: Good use of landmark elements (`<header>`, `<main>`, `<footer>`, `<nav>`)
3. **ARIA Labels**: Most interactive elements have proper aria-labels
4. **CSS Variables**: Well-organized custom properties for theming
5. **Skip Link**: Accessibility skip link implemented
6. **Responsive Design**: Bootstrap 5 responsive grid with custom breakpoints
7. **Font Minimum 14px**: WCAG 2.1 AA compliant font sizes
8. **Focus Indicators**: `:focus-visible` styles implemented

### Issues Identified 🔴

#### Accessibility Issues
1. **Color Contrast**: Some badge colors may not meet 4.5:1 ratio (PENDIENTE badge)
2. **Focus Management**: Modal focus trapping not fully implemented
3. **Live Regions**: Toast notifications lack proper ARIA live regions
4. **Keyboard Navigation**: Carousel navigation not fully keyboard accessible
5. **Form Error Announcements**: Error messages not announced to screen readers

#### Performance Issues
1. **External Font Loading**: Google Fonts loaded with `@import` (render-blocking)
2. **Large CSS File**: Single 1120-line CSS file should be modularized
3. **JavaScript in Global Scope**: All functions exposed globally
4. **No Lazy Loading**: Images and components loaded eagerly
5. **No CSS/JS Minification**: Development assets served in production

#### Scalability Issues
1. **Monolithic JavaScript**: Single 1044-line api.js file
2. **Template Duplication**: HTML generation duplicated between templates and JS
3. **Inline Styles**: Some inline styles in templates
4. **No Component System**: UI elements not reusable
5. **Hardcoded URLs**: Some URLs hardcoded in JavaScript

#### Code Quality Issues
1. **Mixed Concerns**: UI logic mixed with API calls
2. **No TypeScript**: No type safety in JavaScript
3. **No JSDoc**: Limited documentation in JavaScript
4. **CSS Specificity Wars**: Some `!important` overrides
5. **No CSS Naming Convention**: Mixed naming patterns

---

## Phase Overview

| Phase | Name | Duration | Priority | Status |
|-------|------|----------|----------|--------|
| 1 | Accessibility Enhancement | 1 week | 🔴 Critical | ✅ COMPLETED |
| 2 | CSS Architecture Refactor | 1 week | 🟡 High | ✅ COMPLETED |
| 3 | JavaScript Modularization | 1.5 weeks | 🟡 High | ✅ COMPLETED |
| 4 | Template Component System | 1 week | 🟢 Medium | ✅ COMPLETED |
| 5 | Performance Optimization | 1 week | 🟢 Medium | ✅ COMPLETED |
| 6 | Testing & Documentation | 0.5 week | 🟢 Medium | ✅ COMPLETED |

**Progress: 6/6 Phases Complete (100%) 🎉**

---

## Phase 1: Accessibility Enhancement ✅ COMPLETED (v2.6.0)

📄 **Detailed Document**: [phase-1-accessibility.md](./phases/phase-1-accessibility.md)

**Completed**: January 2026

### Goals ✅
- ✅ Achieve WCAG 2.1 AA compliance
- ✅ Improve screen reader compatibility
- ✅ Enhance keyboard navigation
- ✅ Fix color contrast issues

### Deliverables ✅
1. ✅ Color contrast audit and fixes
2. ✅ ARIA live regions for dynamic content
3. ✅ Focus management in modals
4. ✅ Keyboard-accessible carousel (44x44px touch targets)
5. ✅ Form error announcements
6. ✅ Accessibility testing checklist

### Skills Created
- `skill-wcag-accessibility.md`
- `skill-keyboard-navigation.md`
- `skill-screen-reader-testing.md`
- `skill-responsive-design.md`

---

## Phase 2: CSS Architecture Refactor ✅ COMPLETED (v2.7.0)

📄 **Detailed Document**: [phase-2-css-architecture.md](./phases/phase-2-css-architecture.md)

**Completed**: January 15, 2026

### Goals ✅
- ✅ Modularize CSS into logical files (22 files created)
- ✅ Implement organized naming convention
- ✅ Create CSS custom property system
- ✅ Optimize for maintainability

### Deliverables ✅
1. ✅ CSS file structure: `base/`, `components/`, `layout/`, `pages/`, `themes/`, `utilities/`
2. ✅ Component-specific CSS files (navbar, cards, buttons, forms, modals, carousel, alerts, badges)
3. ✅ Theme system with `_light.css` and `_dark.css`
4. ✅ Entry point `main.css` with proper import order
5. ✅ Removed old monolithic `custom.css` (1168 lines → 22 modular files)

### File Structure Created
```
static/css/
├── main.css              # Entry point
├── base/                 # Variables, reset, typography
├── components/           # UI components (8 files)
├── layout/               # Header, footer, containers
├── pages/                # Page-specific styles
├── themes/               # Light/dark theme variables
└── utilities/            # Helpers, animations, a11y
```

---

## Phase 3: JavaScript Modularization ✅ COMPLETED (v2.8.0)

📄 **Detailed Document**: [phase-3-javascript-modularization.md](./phases/phase-3-javascript-modularization.md)

**Completed**: January 15, 2026

### Goals ✅
- ✅ Split api.js into modules
- ✅ Implement ES6 module pattern
- ✅ Add JSDoc documentation
- ✅ Create reusable UI utilities
- ✅ Implement error boundary pattern

### Deliverables ✅
1. ✅ Modular JavaScript architecture with `main.js` entry point
2. ✅ API module separation (client, patients, sessions, dashboard)
3. ✅ UI utilities modules (toast, modal, carousel, accessibility)
4. ✅ Component modules (patientCard, sessionCard, filterButtons, dashboardRenderer)
5. ✅ Utility modules (formatters, validators, helpers)
6. ✅ JSDoc documentation for all functions
7. ✅ Removed legacy `api.js` (1238 lines → 15 modular files)

### File Structure Created
```
static/js/
├── main.js                 # Entry point
└── modules/
    ├── api/                # API client and endpoints (4 files)
    ├── ui/                 # Toast, modal, carousel, accessibility (4 files)
    ├── components/         # UI components (4 files)
    └── utils/              # Formatters, validators, helpers (3 files)
```

### Skills Used
- `skill-javascript-modules.md`
- `skill-jsdoc-documentation.md`
- `skill-event-delegation.md`
- `skill-error-handling.md`

---

## Phase 4: Template Component System ✅ COMPLETED (v2.9.0)

📄 **Detailed Document**: [phase-4-template-components.md](./phases/phase-4-template-components.md)

**Completed**: January 2026

### Goals ✅
- ✅ Create reusable Jinja2 macros
- ✅ Standardize HTML patterns
- ✅ Remove template/JS duplication
- ✅ Implement template inheritance properly

### Deliverables ✅
1. ✅ Component macro library (`templates/macros/`)
2. ✅ Form component macros (`_forms.html` - 9 macros)
3. ✅ Card component macros (`_cards.html` - 6 macros)
4. ✅ Modal component macros (`_modals.html` - 8 macros)
5. ✅ Button component macros (`_buttons.html` - 6 macros)
6. ✅ Template partials (`_navbar.html`, `_footer.html`, `_flash_messages.html`)
7. ✅ Error page macro (`errors/_error_page.html`)
8. ✅ Refactored all templates to use macros (~60% code reduction)

### File Structure Created
```
templates/
├── macros/
│   ├── _forms.html       # text_input, password_input, email_input, etc.
│   ├── _cards.html       # patient_card, auth_card, sessions_carousel, etc.
│   ├── _modals.html      # modal, confirm_modal, edit_modal, dashboard_modals
│   └── _buttons.html     # submit_button, cancel_button, icon_button, etc.
├── partials/
│   ├── _navbar.html      # Navigation bar component
│   ├── _footer.html      # Footer component
│   └── _flash_messages.html  # Flash message alerts
└── errors/
    └── _error_page.html  # Shared error page macro
```

### Key Improvements
- **Auth templates**: Reduced from ~70 lines to ~25 lines each
- **Dashboard (list.html)**: Reduced from ~340 lines to ~95 lines
- **Error templates**: Reduced from ~15 lines to ~12 lines each
- **All macros include ARIA accessibility attributes**
- **Consistent Bootstrap 5 patterns across all components**

### Skills Used
- `skill-jinja2-macros.md`
- `skill-template-patterns.md`
- `skill-html-semantics.md`
- `skill-component-design.md`

---

## Phase 5: Performance Optimization ✅ COMPLETED (v2.10.0)

📄 **Detailed Document**: [phase-5-performance.md](./phases/phase-5-performance.md)

**Completed**: January 15, 2026

### Goals ✅
- ✅ Optimize asset loading (self-hosted fonts and icons)
- ✅ Implement font preloading for better LCP
- ✅ Reduce render-blocking resources
- ✅ Add static asset caching

### Deliverables ✅
1. ✅ Self-hosted Nunito Sans fonts (Latin + Latin-ext for Spanish)
2. ✅ Self-hosted Bootstrap Icons (CSS + WOFF2/WOFF fonts)
3. ✅ Font preloading with `<link rel="preload">`
4. ✅ Deferred JavaScript loading (`defer` attribute)
5. ✅ Cache headers middleware for static assets

### File Structure Created
```
static/fonts/
├── nunito-sans-latin.woff2       # Primary Latin characters
├── nunito-sans-latin-ext.woff2   # Extended Latin (Spanish accents)
├── bootstrap-icons.woff2         # Bootstrap Icons font
└── bootstrap-icons.woff          # Bootstrap Icons fallback

static/css/
├── base/_fonts.css               # Self-hosted @font-face declarations
└── bootstrap-icons.min.css       # Local Bootstrap Icons CSS
```

### Performance Improvements
- Eliminated render-blocking Google Fonts request
- Eliminated external CDN request for Bootstrap Icons
- Font display: swap prevents invisible text during load
- Static assets cached for 1 year with immutable headers
- Deferred JavaScript reduces Total Blocking Time

### Skills Used
- `skill-web-performance.md`
- `skill-asset-optimization.md`
- `skill-core-web-vitals.md`

---

## Phase 6: Testing & Documentation ✅ COMPLETED (v2.11.0)

📄 **Detailed Document**: [phase-6-testing-documentation.md](./phases/phase-6-testing-documentation.md)

**Completed**: January 15, 2026

### Goals ✅
- ✅ Create frontend testing strategy
- ✅ Document all components
- ✅ Create style guide
- ✅ Establish coding standards

### Deliverables ✅
1. ✅ Frontend testing setup with Playwright
2. ✅ CSS, JS, and Template documentation
3. ✅ Style guide with examples
4. ✅ Contributing guidelines for frontend

### File Structure Created
```
docs/
├── css-components.md       # CSS architecture and design tokens
├── js-modules.md           # JavaScript module API reference
├── template-macros.md      # Jinja2 macro documentation
├── frontend-style-guide.md # Coding standards
└── frontend-contributing.md # Contributor guidelines

tests/frontend/
├── conftest.py             # Playwright fixtures
├── test_visual.py          # Visual regression tests
├── test_accessibility.py   # WCAG compliance tests
└── test_interactions.py    # User interaction tests
```

### Skills Used
- `skill-frontend-testing.md`
- `skill-documentation.md`
- `skill-style-guide.md`

---

## UX/UI Issues from Chrome DevTools Review

### Visual Inconsistencies Found

| Issue | Location | Priority | Phase |
|-------|----------|----------|-------|
| Badge color contrast (PENDIENTE) | Dashboard cards | High | 1 |
| Button group spacing on mobile | Session cards | Medium | 2 |
| Filter button active state subtle | Dashboard | Medium | 2 |
| Toast notification z-index | Global | Low | 3 |
| Carousel indicators small touch target | Dashboard | Medium | 1 |
| Modal backdrop transition | All modals | Low | 2 |
| Form validation visual feedback | Auth forms | Medium | 1 |

### Responsive Design Issues

| Issue | Breakpoint | Priority |
|-------|------------|----------|
| Navbar collapse alignment | < 992px | Medium |
| Patient card text truncation | < 400px | Low |
| Filter buttons stacking | < 400px | Low |
| Session button text overflow | < 576px | Medium |

### Theme-Specific Issues

| Issue | Theme | Priority |
|-------|-------|----------|
| Alert message contrast | Light | Medium |
| Card header distinction | Dark | Low |
| Form input placeholder visibility | Dark | Medium |

---

## Success Metrics

### Accessibility
- [ ] Lighthouse Accessibility Score ≥ 95
- [ ] axe-core automated tests pass
- [ ] Manual keyboard navigation test pass
- [ ] Screen reader testing with NVDA/VoiceOver

### Performance
- [ ] Lighthouse Performance Score ≥ 90
- [ ] First Contentful Paint < 1.5s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Total Blocking Time < 200ms

### Code Quality
- [ ] CSS file size reduced by 20%
- [ ] JavaScript modules < 300 lines each
- [ ] No `!important` except utilities
- [ ] 100% JSDoc coverage

---

## Risk Mitigation

### Phase Dependencies
- Phase 2 depends on Phase 1 (accessibility fixes may change CSS)
- Phase 3 should wait for Phase 2 (JS may reference CSS classes)
- Phase 4 can run parallel to Phase 3
- Phase 5 requires Phase 2-4 completion
- Phase 6 is the final validation

### Rollback Strategy
- Git branch per phase
- Feature flags for new components
- Gradual rollout with A/B testing capability
- Backup of current working state

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Begin Phase 1** immediately (accessibility is critical)
3. **Create phase branch**: `git checkout -b refactor/phase-1-accessibility`
4. **Follow phase document** for detailed implementation steps
5. **Verify each change** with Chrome DevTools before proceeding

---

## Related Documents

- [Phase 1: Accessibility Enhancement](./phases/phase-1-accessibility.md)
- [Phase 2: CSS Architecture Refactor](./phases/phase-2-css-architecture.md)
- [Phase 3: JavaScript Modularization](./phases/phase-3-javascript-modularization.md)
- [Phase 4: Template Component System](./phases/phase-4-template-components.md)
- [Phase 5: Performance Optimization](./phases/phase-5-performance.md)
- [Phase 6: Testing & Documentation](./phases/phase-6-testing-documentation.md)

---

*Last Updated: January 15, 2026*
*Version: 1.0*
