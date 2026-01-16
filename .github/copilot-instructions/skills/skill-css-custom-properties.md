# Skill: CSS Custom Properties

## Overview

CSS Custom Properties (CSS Variables) enable dynamic, maintainable styling with built-in theming support. This skill covers variable naming, organization, theming patterns, and best practices for the Therapy Session Management Application.

---

## Syntax Fundamentals

### Declaration and Usage

```css
/* Declaration in :root (global scope) */
:root {
    --color-primary: #3F4A49;
    --spacing-md: 1rem;
}

/* Usage with var() function */
.card {
    background: var(--color-primary);
    padding: var(--spacing-md);
}

/* Fallback values */
.card {
    color: var(--text-color, #333);  /* Falls back to #333 if undefined */
}
```

### Scope and Inheritance

```css
/* Global scope - available everywhere */
:root {
    --color-primary: blue;
}

/* Local scope - only within .card and descendants */
.card {
    --card-padding: 1rem;
    padding: var(--card-padding);
}

/* Inheritance - child inherits parent's variables */
.card .card-title {
    /* Can access --card-padding from parent */
    margin-bottom: var(--card-padding);
}
```

---

## Variable Naming Convention

### Pattern

```
--{category}-{property}-{variant}
```

| Part | Description | Examples |
|------|-------------|----------|
| Category | Logical grouping | `color`, `space`, `font`, `radius` |
| Property | What it controls | `primary`, `body`, `heading` |
| Variant | Modification | `light`, `dark`, `hover`, `sm`, `lg` |

### Naming Examples

```css
:root {
    /* Colors */
    --color-primary: #3F4A49;
    --color-primary-light: #4d5a59;
    --color-primary-dark: #2d3635;
    --color-secondary: #DCD9D0;
    --color-success: #198754;
    --color-warning: #ffc107;
    --color-danger: #dc3545;
    
    /* Text colors */
    --color-text-primary: #3F4A49;
    --color-text-secondary: #5a6665;
    --color-text-muted: #7a8685;
    --color-text-inverse: #ffffff;
    
    /* Background colors */
    --color-bg-body: #F5F3EF;
    --color-bg-card: #ffffff;
    --color-bg-input: #ffffff;
    
    /* Spacing scale */
    --space-1: 0.25rem;    /* 4px */
    --space-2: 0.5rem;     /* 8px */
    --space-3: 0.75rem;    /* 12px */
    --space-4: 1rem;       /* 16px */
    --space-5: 1.5rem;     /* 24px */
    --space-6: 2rem;       /* 32px */
    --space-8: 3rem;       /* 48px */
    
    /* Font sizes */
    --font-size-xs: 0.875rem;   /* 14px */
    --font-size-sm: 0.9375rem;  /* 15px */
    --font-size-base: 1rem;     /* 16px */
    --font-size-lg: 1.125rem;   /* 18px */
    --font-size-xl: 1.25rem;    /* 20px */
    --font-size-2xl: 1.5rem;    /* 24px */
    --font-size-3xl: 1.875rem;  /* 30px */
    
    /* Font weights */
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    
    /* Border radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-full: 50%;
    --radius-pill: 9999px;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
    --transition-slow: 500ms ease;
    
    /* Z-index scale */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-fixed: 1030;
    --z-modal-backdrop: 1040;
    --z-modal: 1050;
    --z-popover: 1060;
    --z-tooltip: 1070;
    --z-toast: 1080;
}
```

---

## Theming System

### Theme Architecture

The application uses Bootstrap's `data-bs-theme` attribute for theme switching:

```html
<!-- Dark theme (default) -->
<html data-bs-theme="dark">

<!-- Light theme -->
<html data-bs-theme="light">
```

### Base Variables (Theme-Agnostic)

Define non-changing values in `:root`:

```css
:root {
    /* Brand colors - constant across themes */
    --brand-teal: #3F4A49;
    --brand-teal-light: #4d5a59;
    --brand-beige: #DCD9D0;
    --brand-cream: #F5F3EF;
    
    /* Typography - constant */
    --font-family-primary: 'Nunito Sans', system-ui, sans-serif;
    --font-family-mono: 'Fira Code', monospace;
    
    /* Spacing scale - constant */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
    
    /* Radius - constant */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    
    /* Transitions - constant */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
}
```

### Semantic Variables (Theme-Dependent)

Override semantic variables per theme:

```css
/* Light theme */
[data-bs-theme="light"] {
    /* Backgrounds */
    --bg-body: var(--brand-cream);
    --bg-surface: #ffffff;
    --bg-elevated: #ffffff;
    --bg-muted: var(--brand-beige);
    
    /* Text */
    --text-primary: var(--brand-teal);
    --text-secondary: #5a6665;
    --text-muted: #7a8685;
    --text-inverse: #ffffff;
    
    /* Borders */
    --border-default: var(--brand-beige);
    --border-muted: #e5e5e5;
    
    /* Interactive */
    --interactive-primary: var(--brand-teal);
    --interactive-primary-hover: var(--brand-teal-light);
    
    /* Component-specific */
    --card-bg: #ffffff;
    --card-border: var(--brand-beige);
    --card-header-bg: var(--brand-beige);
    --input-bg: #ffffff;
    --input-border: var(--brand-beige);
    --nav-bg: var(--brand-teal);
    --nav-text: #ffffff;
    
    /* Shadows - softer for light theme */
    --shadow-color: rgba(0, 0, 0, 0.08);
}

/* Dark theme */
[data-bs-theme="dark"] {
    /* Backgrounds */
    --bg-body: #1a1d1f;
    --bg-surface: #212529;
    --bg-elevated: #2a2e32;
    --bg-muted: #2d3235;
    
    /* Text */
    --text-primary: #e5e5e5;
    --text-secondary: #adb5bd;
    --text-muted: #868e96;
    --text-inverse: #1a1d1f;
    
    /* Borders */
    --border-default: #3d4447;
    --border-muted: #2d3235;
    
    /* Interactive */
    --interactive-primary: #5a9a97;
    --interactive-primary-hover: #6fb3b0;
    
    /* Component-specific */
    --card-bg: #212529;
    --card-border: #3d4447;
    --card-header-bg: #2a2e32;
    --input-bg: #2d3235;
    --input-border: #3d4447;
    --nav-bg: #212529;
    --nav-text: #e5e5e5;
    
    /* Shadows - stronger for dark theme */
    --shadow-color: rgba(0, 0, 0, 0.3);
}
```

### Using Semantic Variables in Components

```css
/* Components use semantic variables, not raw colors */
.card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    color: var(--text-primary);
}

.card__header {
    background: var(--card-header-bg);
    border-bottom: 1px solid var(--card-border);
}

.btn--primary {
    background: var(--interactive-primary);
    color: var(--text-inverse);
}

.btn--primary:hover {
    background: var(--interactive-primary-hover);
}

/* Shadows adapt to theme */
.card {
    box-shadow: 0 4px 6px var(--shadow-color);
}
```

---

## Component-Level Variables

### Scoped Variables for Components

```css
/* Button component with local variables */
.btn {
    /* Local variables - can be overridden by modifiers */
    --btn-padding-x: var(--space-4);
    --btn-padding-y: var(--space-2);
    --btn-font-size: var(--font-size-base);
    --btn-border-radius: var(--radius-md);
    --btn-bg: transparent;
    --btn-color: var(--text-primary);
    --btn-border-color: var(--border-default);
    
    /* Use local variables */
    padding: var(--btn-padding-y) var(--btn-padding-x);
    font-size: var(--btn-font-size);
    border-radius: var(--btn-border-radius);
    background: var(--btn-bg);
    color: var(--btn-color);
    border: 1px solid var(--btn-border-color);
}

/* Modifiers override local variables */
.btn--primary {
    --btn-bg: var(--interactive-primary);
    --btn-color: var(--text-inverse);
    --btn-border-color: var(--interactive-primary);
}

.btn--small {
    --btn-padding-x: var(--space-2);
    --btn-padding-y: var(--space-1);
    --btn-font-size: var(--font-size-sm);
}

.btn--large {
    --btn-padding-x: var(--space-6);
    --btn-padding-y: var(--space-3);
    --btn-font-size: var(--font-size-lg);
}
```

### Card Component Example

```css
.card {
    /* Local variables */
    --card-padding: var(--space-4);
    --card-radius: var(--radius-lg);
    --card-shadow: var(--shadow-md);
    
    padding: var(--card-padding);
    border-radius: var(--card-radius);
    box-shadow: var(--card-shadow);
    background: var(--card-bg);
    border: 1px solid var(--card-border);
}

.card--compact {
    --card-padding: var(--space-3);
}

.card--elevated {
    --card-shadow: var(--shadow-lg);
}

.card--flat {
    --card-shadow: none;
    --card-radius: 0;
}
```

---

## JavaScript Integration

### Reading CSS Variables

```javascript
// Get computed value
const root = document.documentElement;
const primaryColor = getComputedStyle(root).getPropertyValue('--color-primary').trim();

// Get from specific element
const card = document.querySelector('.card');
const cardPadding = getComputedStyle(card).getPropertyValue('--card-padding').trim();
```

### Setting CSS Variables

```javascript
// Set on :root (global)
document.documentElement.style.setProperty('--color-primary', '#ff0000');

// Set on specific element
const card = document.querySelector('.card');
card.style.setProperty('--card-padding', '2rem');
```

### Theme Switching

```javascript
/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

/**
 * Initialize theme from localStorage or system preference
 */
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
        document.documentElement.setAttribute('data-bs-theme', 'light');
    }
    // Default is dark (set in HTML)
}

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        document.documentElement.setAttribute('data-bs-theme', e.matches ? 'dark' : 'light');
    }
});
```

### Dynamic Theming

```javascript
/**
 * Apply a custom color scheme
 */
function applyColorScheme(colors) {
    const root = document.documentElement;
    
    Object.entries(colors).forEach(([name, value]) => {
        root.style.setProperty(`--color-${name}`, value);
    });
}

// Usage
applyColorScheme({
    'primary': '#5a9a97',
    'primary-light': '#6fb3b0',
    'primary-dark': '#4a8a87'
});
```

---

## Bootstrap Integration

### Overriding Bootstrap Variables

```css
/* Override Bootstrap's CSS variables */
[data-bs-theme="light"] {
    /* Bootstrap color system */
    --bs-primary: var(--brand-teal);
    --bs-primary-rgb: 63, 74, 73;
    
    /* Bootstrap component colors */
    --bs-body-bg: var(--bg-body);
    --bs-body-color: var(--text-primary);
    --bs-card-bg: var(--card-bg);
    --bs-border-color: var(--border-default);
    
    /* Bootstrap link colors */
    --bs-link-color: var(--interactive-primary);
    --bs-link-hover-color: var(--interactive-primary-hover);
}
```

### Mapping Custom to Bootstrap Variables

```css
:root {
    /* Our semantic variables */
    --color-primary: #3F4A49;
    
    /* Map to Bootstrap */
    --bs-primary: var(--color-primary);
}
```

---

## Common Patterns

### Responsive Variables

```css
:root {
    /* Base spacing */
    --container-padding: var(--space-4);
    --section-spacing: var(--space-6);
    --card-gap: var(--space-4);
}

/* Adjust for larger screens */
@media (min-width: 768px) {
    :root {
        --container-padding: var(--space-5);
        --section-spacing: var(--space-8);
        --card-gap: var(--space-5);
    }
}

@media (min-width: 1200px) {
    :root {
        --container-padding: var(--space-6);
    }
}
```

### State Variables

```css
/* Interactive states */
.btn {
    --btn-opacity: 1;
    opacity: var(--btn-opacity);
    transition: opacity var(--transition-fast);
}

.btn:hover {
    --btn-opacity: 0.9;
}

.btn:disabled {
    --btn-opacity: 0.5;
}

/* Loading state */
.card {
    --card-loading-opacity: 0;
}

.card--loading {
    --card-loading-opacity: 1;
}

.card__loader {
    opacity: var(--card-loading-opacity);
}
```

### Computed Values

```css
:root {
    /* Base unit */
    --base-size: 1rem;
    
    /* Computed from base */
    --size-sm: calc(var(--base-size) * 0.875);
    --size-lg: calc(var(--base-size) * 1.25);
    --size-2x: calc(var(--base-size) * 2);
}

/* Spacing based on base */
.card {
    padding: calc(var(--space-4) * 1.5);
    margin-bottom: calc(var(--space-4) * 2);
}
```

---

## Project Variable Reference

### Current Variables in custom.css

```css
:root {
    /* Brand palette */
    --mlc-teal: #3F4A49;
    --mlc-teal-light: #4d5a59;
    --mlc-teal-dark: #2d3635;
    --mlc-beige: #DCD9D0;
    --mlc-beige-light: #EAE8E3;
    --mlc-cream: #F5F3EF;
    --mlc-white: #FFFFFF;
    
    /* Typography */
    --font-primary: 'Nunito Sans', 'Segoe UI', system-ui, sans-serif;
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    
    /* Font sizes (WCAG 2.1 AA minimum: 14px) */
    --font-size-xs: 0.875rem;     /* 14px */
    --font-size-sm: 0.9375rem;    /* 15px */
    --font-size-base: 1rem;       /* 16px */
    --font-size-lg: 1.125rem;     /* 18px */
    --font-size-xl: 1.25rem;      /* 20px */
    --font-size-2xl: 1.5rem;      /* 24px */
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-xxl: 3rem;
    
    /* Border radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-pill: 50rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
}
```

---

## Checklist for CSS Custom Properties

### Organization
- [ ] Global constants in `:root`
- [ ] Theme-specific values in `[data-bs-theme]` selectors
- [ ] Component-scoped variables where appropriate
- [ ] Consistent naming convention followed

### Theming
- [ ] All color values use variables
- [ ] Light and dark theme variables defined
- [ ] Bootstrap variables overridden correctly
- [ ] Theme switching works smoothly

### Usage
- [ ] Fallback values provided where needed
- [ ] No hardcoded colors in component CSS
- [ ] Computed values use `calc()` correctly
- [ ] JavaScript can read/write variables

### Documentation
- [ ] Variable naming convention documented
- [ ] All variables listed in reference
- [ ] Theme variables clearly organized

---

## Related Skills

- [skill-css-architecture.md](./skill-css-architecture.md) - File organization
- [skill-bem-methodology.md](./skill-bem-methodology.md) - Naming convention
- [skill-responsive-design.md](./skill-responsive-design.md) - Responsive variables

---

*Last Updated: January 15, 2026*
