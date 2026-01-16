# Skill: CSS Architecture

## Overview

This skill covers CSS file organization, naming conventions, and architectural patterns for maintainable, scalable stylesheets. The goal is to transform a monolithic CSS file into a well-organized, modular system.

---

## Current State Analysis

### Project CSS Structure
```
static/css/
├── bootstrap.min.css    # Bootstrap 5 framework (vendor)
└── custom.css           # Application styles (1120 lines - monolithic)
```

### Issues with Monolithic CSS
- **Hard to maintain**: Finding specific styles requires scrolling through 1000+ lines
- **Specificity conflicts**: Rules override each other unpredictably
- **Code duplication**: Similar patterns repeated without abstraction
- **Team collaboration**: Multiple developers editing same file causes conflicts
- **Performance**: Browser parses entire file even for simple pages

---

## ITCSS Architecture (Inverted Triangle CSS)

ITCSS organizes CSS from generic to specific, reducing specificity conflicts.

### Layer Structure

```
           ▲
          /│\     Settings   - Variables, config
         / │ \    Tools      - Mixins, functions
        /  │  \   Generic    - Reset, normalize
       /   │   \  Elements   - Base HTML elements
      /    │    \ Objects    - Layout patterns
     /     │     \Components - UI components
    /      │      \Utilities - Helper classes
   ▼───────┴───────▼
   Low Specificity → High Specificity
```

### Proposed File Structure

```
static/css/
├── bootstrap.min.css         # Vendor (unchanged)
├── main.css                  # Entry point (imports all)
│
├── settings/
│   ├── _variables.css        # CSS custom properties
│   └── _breakpoints.css      # Responsive breakpoints
│
├── base/
│   ├── _reset.css            # CSS reset/normalize additions
│   ├── _typography.css       # Font styles, headings
│   └── _forms.css            # Base form element styles
│
├── layout/
│   ├── _grid.css             # Grid system extensions
│   ├── _header.css           # Header/navbar layout
│   ├── _footer.css           # Footer layout
│   └── _containers.css       # Page containers
│
├── components/
│   ├── _buttons.css          # Button variants
│   ├── _cards.css            # Card components
│   ├── _modals.css           # Modal styles
│   ├── _carousel.css         # Carousel styles
│   ├── _badges.css           # Badge/tag styles
│   ├── _alerts.css           # Alert/flash messages
│   ├── _toasts.css           # Toast notifications
│   └── _forms-components.css # Form components (inputs, selects)
│
├── pages/
│   ├── _dashboard.css        # Dashboard-specific styles
│   ├── _auth.css             # Login/register pages
│   └── _errors.css           # Error page styles
│
├── themes/
│   ├── _light.css            # Light theme overrides
│   └── _dark.css             # Dark theme overrides
│
└── utilities/
    ├── _spacing.css          # Margin/padding utilities
    ├── _display.css          # Display utilities
    └── _accessibility.css    # A11y utilities (sr-only, etc.)
```

---

## CSS Custom Properties System

### Variable Naming Convention

```css
/* Pattern: --{category}-{property}-{variant} */

:root {
    /* Colors */
    --color-primary: #3F4A49;
    --color-primary-light: #4d5a59;
    --color-primary-dark: #2d3635;
    
    /* Semantic colors */
    --color-text-primary: var(--color-primary);
    --color-text-secondary: #5a6665;
    --color-text-muted: #7a8685;
    
    /* Component-specific */
    --card-bg: var(--color-white);
    --card-border: var(--color-beige);
    --card-shadow: var(--shadow-md);
    
    /* Spacing scale */
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-5: 1.5rem;    /* 24px */
    --space-6: 2rem;      /* 32px */
    --space-8: 3rem;      /* 48px */
    
    /* Typography scale */
    --text-xs: 0.75rem;   /* 12px */
    --text-sm: 0.875rem;  /* 14px */
    --text-base: 1rem;    /* 16px */
    --text-lg: 1.125rem;  /* 18px */
    --text-xl: 1.25rem;   /* 20px */
    --text-2xl: 1.5rem;   /* 24px */
    --text-3xl: 1.875rem; /* 30px */
}
```

### Theme Switching Pattern

```css
/* Base theme (dark - default) */
:root {
    --bg-body: #1a1d1f;
    --text-body: #e5e5e5;
    --bg-card: #212529;
}

/* Light theme override */
[data-bs-theme="light"] {
    --bg-body: #F5F3EF;
    --text-body: #3F4A49;
    --bg-card: #FFFFFF;
}

/* Component uses semantic variables */
.card {
    background: var(--bg-card);
    color: var(--text-body);
}
```

---

## Specificity Management

### Specificity Rules

| Selector Type | Specificity | Example |
|---------------|-------------|---------|
| Element | 0-0-1 | `div`, `p` |
| Class | 0-1-0 | `.card`, `.btn` |
| ID | 1-0-0 | `#header` |
| Inline | 1-0-0-0 | `style=""` |

### Best Practices

```css
/* ✅ DO: Use single class selectors */
.card-header { }
.card-header-title { }

/* ❌ DON'T: Chain multiple classes unnecessarily */
.card .card-header .card-header-title { }

/* ✅ DO: Use BEM for component variants */
.btn--primary { }
.btn--large { }

/* ❌ DON'T: Use IDs for styling */
#submit-button { }

/* ✅ DO: Use data attributes for state */
.btn[data-loading="true"] { }

/* ❌ DON'T: Use !important (except utilities) */
.card { background: white !important; }
```

### When `!important` is Acceptable

```css
/* ✅ Utility classes - designed to override */
.u-hidden { display: none !important; }
.u-sr-only { position: absolute !important; }

/* ✅ Overriding vendor styles with no other option */
.bootstrap-override { color: inherit !important; }
```

---

## CSS Organization Within Files

### File Header Template

```css
/**
 * Component: Card
 * Description: Card component for displaying patient/session info
 * Dependencies: _variables.css
 * 
 * Markup:
 * <article class="card">
 *   <header class="card__header">...</header>
 *   <div class="card__body">...</div>
 *   <footer class="card__footer">...</footer>
 * </article>
 */
```

### Section Organization

```css
/* ==========================================================================
   CARD COMPONENT
   ========================================================================== */

/**
 * Base card styles
 */
.card { }

/**
 * Card header
 */
.card__header { }

/**
 * Card body
 */
.card__body { }

/**
 * Card footer
 */
.card__footer { }

/* Card Variants
   ========================================================================== */

/**
 * Patient card variant
 */
.card--patient { }

/**
 * Session card variant
 */
.card--session { }

/* Card States
   ========================================================================== */

.card--pending { }
.card--paid { }
.card--loading { }
```

---

## Import Strategy

### Main Entry Point (main.css)

```css
/**
 * Main CSS Entry Point
 * Import order follows ITCSS methodology
 */

/* Settings - Variables and configuration */
@import 'settings/_variables.css';
@import 'settings/_breakpoints.css';

/* Base - Reset and element defaults */
@import 'base/_reset.css';
@import 'base/_typography.css';
@import 'base/_forms.css';

/* Layout - Page structure */
@import 'layout/_grid.css';
@import 'layout/_header.css';
@import 'layout/_footer.css';
@import 'layout/_containers.css';

/* Components - UI components */
@import 'components/_buttons.css';
@import 'components/_cards.css';
@import 'components/_modals.css';
@import 'components/_carousel.css';
@import 'components/_badges.css';
@import 'components/_alerts.css';
@import 'components/_toasts.css';
@import 'components/_forms-components.css';

/* Pages - Page-specific styles */
@import 'pages/_dashboard.css';
@import 'pages/_auth.css';
@import 'pages/_errors.css';

/* Themes - Theme overrides */
@import 'themes/_light.css';
@import 'themes/_dark.css';

/* Utilities - Helper classes (highest specificity) */
@import 'utilities/_spacing.css';
@import 'utilities/_display.css';
@import 'utilities/_accessibility.css';
```

---

## Migration Strategy

### Phase 1: Extract Variables
1. Create `settings/_variables.css`
2. Move all `:root` variables from `custom.css`
3. Test theme switching works

### Phase 2: Extract Components
1. Identify distinct component sections in `custom.css`
2. Create individual component files
3. Move styles maintaining order
4. Update imports

### Phase 3: Extract Layouts
1. Identify layout patterns (header, footer, grid)
2. Create layout files
3. Move styles

### Phase 4: Extract Themes
1. Create `themes/_light.css` and `themes/_dark.css`
2. Move theme-specific overrides
3. Ensure clean theme switching

### Phase 5: Cleanup
1. Remove empty sections from `custom.css`
2. Add file headers and documentation
3. Validate no broken styles

---

## Linting and Formatting

### Recommended Tools

```bash
# Stylelint - CSS linter
npm install --save-dev stylelint stylelint-config-standard

# Prettier - Code formatter
npm install --save-dev prettier
```

### Stylelint Configuration (.stylelintrc.json)

```json
{
  "extends": "stylelint-config-standard",
  "rules": {
    "selector-class-pattern": "^[a-z][a-z0-9]*(-[a-z0-9]+)*(__[a-z0-9]+(-[a-z0-9]+)*)?(--[a-z0-9]+(-[a-z0-9]+)*)?$",
    "declaration-no-important": true,
    "max-nesting-depth": 3,
    "selector-max-id": 0,
    "selector-max-specificity": "0,3,0"
  }
}
```

---

## Project-Specific Guidelines

### Current custom.css Sections

The existing `custom.css` has these logical sections that map to new files:

| Current Section | New File |
|-----------------|----------|
| CSS Custom Properties | `settings/_variables.css` |
| Light Theme Overrides | `themes/_light.css` |
| Dark Theme Overrides | `themes/_dark.css` |
| Base Typography | `base/_typography.css` |
| Navbar styles | `layout/_header.css` |
| Card styles | `components/_cards.css` |
| Button styles | `components/_buttons.css` |
| Form styles | `components/_forms-components.css` |
| Modal styles | `components/_modals.css` |
| Carousel styles | `components/_carousel.css` |
| Badge styles | `components/_badges.css` |
| Alert styles | `components/_alerts.css` |
| Toast styles | `components/_toasts.css` |
| Dashboard-specific | `pages/_dashboard.css` |
| Auth pages | `pages/_auth.css` |
| Accessibility | `utilities/_accessibility.css` |

---

## Checklist for CSS Architecture

### File Organization
- [ ] Variables extracted to `settings/_variables.css`
- [ ] Components have individual files
- [ ] Themes separated into own files
- [ ] Main entry point imports all files in correct order

### Specificity
- [ ] No ID selectors for styling
- [ ] No `!important` except utilities
- [ ] Maximum 3 levels of nesting
- [ ] Single-class selectors preferred

### Documentation
- [ ] File headers with description
- [ ] Section comments for grouping
- [ ] Markup examples in component files

### Maintainability
- [ ] Consistent naming convention (BEM)
- [ ] Semantic variable names
- [ ] No magic numbers (use variables)
- [ ] No duplicate code

---

## Related Skills

- [skill-bem-methodology.md](./skill-bem-methodology.md) - BEM naming convention
- [skill-css-custom-properties.md](./skill-css-custom-properties.md) - CSS variables deep dive
- [skill-responsive-design.md](./skill-responsive-design.md) - Responsive patterns

---

*Last Updated: January 15, 2026*
