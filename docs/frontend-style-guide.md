# Frontend Style Guide

This document establishes the coding standards and best practices for frontend development in the Therapy Session Management Application.

---

## Naming Conventions

### CSS Classes

We use **BEM (Block Element Modifier)** methodology:

```css
/* Block - Standalone component */
.patient-card { }

/* Element - Part of a block (double underscore) */
.patient-card__header { }
.patient-card__name { }
.patient-card__actions { }

/* Modifier - Variation (double hyphen) */
.patient-card--highlighted { }
.patient-card__name--truncated { }
```

### JavaScript

| Type | Convention | Example |
|------|------------|---------|
| Files | kebab-case | `patient-card.js` |
| Functions | camelCase | `getPatient()` |
| Classes | PascalCase | `ApiError` |
| Constants | SCREAMING_SNAKE | `API_BASE` |
| Private functions | underscore prefix | `_parseResponse()` |

### HTML Data Attributes

Use `data-*` attributes for JavaScript hooks:

```html
<button data-patient-action="edit" data-patient-id="1">
    Edit
</button>
```

---

## CSS Guidelines

### File Organization

1. Variables and tokens
2. Base/Reset styles
3. Typography
4. Layout
5. Components (alphabetical)
6. Page-specific styles
7. Themes
8. Utilities

### Use CSS Variables

```css
/* ✅ Correct - use variables */
.component {
    color: var(--text-primary);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
}

/* ❌ Incorrect - hardcoded values */
.component {
    color: #333333;
    padding: 16px;
    border-radius: 8px;
}
```

### Avoid `!important`

Never use `!important` except in utility classes:

```css
/* ✅ Only in utilities */
.u-hidden { display: none !important; }

/* ❌ Never in components */
.card { margin: 0 !important; }
```

### Theme-Safe Colors

Always use theme-aware variables:

```css
/* ✅ Theme-aware */
.card {
    background-color: var(--card-bg);
    border-color: var(--border-color);
}

/* ❌ Hardcoded colors break themes */
.card {
    background-color: #ffffff;
}
```

---

## JavaScript Guidelines

### Module Structure

```javascript
/**
 * Module Name
 * @module category/name
 * @description Brief description
 */

// 1. Imports
import { dependency } from './dependency.js';

// 2. Constants
const CONSTANT_VALUE = 'value';

// 3. Private functions
function _privateHelper() { }

// 4. Public functions (exported)
export function publicFunction() { }

// 5. Initialization
export function init() { }
```

### JSDoc Documentation

All public functions must have JSDoc:

```javascript
/**
 * Format a date for display in Spanish locale
 * @param {string} dateStr - Date in YYYY-MM-DD format
 * @returns {string} Formatted date (e.g., "Lunes 15/01/2024")
 * @example
 * formatDisplayDate('2024-01-15'); // "Lunes 15/01/2024"
 */
export function formatDisplayDate(dateStr) {
    // implementation
}
```

### Error Handling

Always handle errors gracefully:

```javascript
async function handleAction() {
    try {
        const result = await apiCall();
        showToast('Éxito', 'success');
    } catch (error) {
        console.error('Action failed:', error);
        showToast(error.message || 'Error inesperado', 'error');
    }
}
```

### Event Delegation

Prefer event delegation over individual handlers:

```javascript
// ✅ Event delegation
document.addEventListener('click', (e) => {
    if (e.target.matches('[data-action="delete"]')) {
        handleDelete(e.target.dataset.id);
    }
});

// ❌ Individual handlers (less efficient)
buttons.forEach(btn => {
    btn.addEventListener('click', handleDelete);
});
```

---

## Template Guidelines

### Use Macros

Always use macros for reusable components:

```jinja2
{# ✅ Use macros #}
{% from 'macros/_forms.html' import text_input %}
{{ text_input(form.name, icon='person', required=true) }}

{# ❌ Don't duplicate HTML #}
<div class="mb-3">
    <label>...</label>
    <input>...</input>
</div>
```

### Accessibility in Templates

Include ARIA attributes:

```jinja2
{# ✅ Accessible #}
<button aria-label="Editar paciente {{ patient.name }}">
    <i class="bi bi-pencil" aria-hidden="true"></i>
</button>

{# ❌ Missing accessibility #}
<button>
    <i class="bi bi-pencil"></i>
</button>
```

### Spanish UI Text

All user-facing text should be in Spanish:

```jinja2
{# ✅ Spanish UI #}
{{ submit_button('Guardar Cambios') }}

{# ❌ English UI #}
{{ submit_button('Save Changes') }}
```

---

## Accessibility Requirements

### Minimum Standards

- **WCAG 2.1 AA** compliance
- Color contrast ≥ **4.5:1** for text
- Minimum font size **14px** (`--font-size-xs`)
- Touch targets ≥ **44x44px**
- Keyboard navigable
- Screen reader compatible

### Required ARIA Attributes

| Element | Required |
|---------|----------|
| Images | `alt` attribute |
| Icons (decorative) | `aria-hidden="true"` |
| Interactive elements (no text) | `aria-label` |
| Form inputs | Associated `<label>` |
| Error messages | `role="alert"` |
| Live updates | `aria-live` region |

### Focus Indicators

All focusable elements must have visible `:focus-visible` styles.

---

## Theme Support

### Required Testing

Test all UI changes in both themes:
1. **Dark mode** (default)
2. **Light mode**

### Theme Toggle

Theme is controlled via `data-bs-theme` on `<html>`:

```html
<html lang="es" data-bs-theme="dark">
<html lang="es" data-bs-theme="light">
```

---

## Responsive Design

### Breakpoints

| Name | Width | Usage |
|------|-------|-------|
| Mobile | < 576px | Phone portrait |
| Tablet | 576px - 991px | Tablets, phone landscape |
| Desktop | ≥ 992px | Laptops, desktops |

### Testing Requirements

Test at these viewports:
- **375px** (iPhone SE)
- **768px** (iPad)
- **1200px** (Desktop)

---

## Performance Guidelines

### Asset Budgets

| Asset Type | Budget |
|------------|--------|
| Total CSS | < 50KB |
| Total JS | < 100KB |
| Font files | < 100KB |
| Per-page load | < 500KB |

### Loading Strategy

- Critical CSS: inline in `<head>`
- Non-critical CSS: deferred
- JavaScript: `defer` attribute
- Images: lazy loaded
- Fonts: `font-display: swap`

---

## Code Review Checklist

Before submitting code:

### Visual
- [ ] Verified in dark mode
- [ ] Verified in light mode
- [ ] Tested at mobile viewport (375px)
- [ ] Tested at desktop viewport (1200px)

### Accessibility
- [ ] Keyboard navigation works
- [ ] ARIA labels present
- [ ] Color contrast passes
- [ ] Focus indicators visible

### Code Quality
- [ ] BEM naming convention
- [ ] No hardcoded colors
- [ ] No `!important` (except utilities)
- [ ] JSDoc on all functions
- [ ] No console.log in production

### Testing
- [ ] No console errors
- [ ] All tests pass
- [ ] Manual testing completed

---

*Last Updated: January 15, 2026*
