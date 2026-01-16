# CSS Component Documentation

This document describes the CSS architecture, design tokens, and component styles for the Therapy Session Management Application.

## Architecture Overview

The CSS is organized into a modular structure with `main.css` as the entry point:

```
static/css/
├── main.css              # Entry point - imports all modules
├── base/                 # Design tokens and foundation
│   ├── _variables.css    # CSS custom properties
│   ├── _fonts.css        # Self-hosted font definitions
│   ├── _reset.css        # CSS reset/normalize
│   └── _typography.css   # Typography styles
├── components/           # UI components
│   ├── _alerts.css       # Alert/notification styles
│   ├── _badges.css       # Status badges
│   ├── _buttons.css      # Button styles
│   ├── _cards.css        # Card components
│   ├── _carousel.css     # Session carousel
│   ├── _forms.css        # Form elements
│   ├── _modals.css       # Modal dialogs
│   └── _navbar.css       # Navigation bar
├── layout/               # Page structure
│   ├── _header.css       # Header styles
│   ├── _footer.css       # Footer styles
│   └── _containers.css   # Container layouts
├── pages/                # Page-specific styles
│   ├── _auth.css         # Login/register pages
│   ├── _dashboard.css    # Patient dashboard
│   └── _errors.css       # Error pages
├── themes/               # Theme definitions
│   ├── _light.css        # Light theme overrides
│   └── _dark.css         # Dark theme overrides
└── utilities/            # Helper classes
    ├── _accessibility.css # A11y utilities
    ├── _animations.css   # Animation definitions
    └── _helpers.css      # Utility classes
```

---

## Design Tokens

All design tokens are defined in `static/css/base/_variables.css`.

### Color Palette

| Variable | Value | Usage |
|----------|-------|-------|
| `--mlc-teal` | `#3F4A49` | Primary brand color |
| `--mlc-teal-light` | `#4d5a59` | Hover states |
| `--mlc-teal-dark` | `#2d3635` | Active states |
| `--mlc-beige` | `#DCD9D0` | Secondary backgrounds |
| `--mlc-beige-light` | `#EAE8E3` | Light backgrounds |
| `--mlc-cream` | `#F5F3EF` | Page backgrounds |
| `--mlc-white` | `#FFFFFF` | Pure white |

### Semantic Colors

| Variable | Value | Usage |
|----------|-------|-------|
| `--color-success` | `var(--mlc-teal)` | Success states, paid badges |
| `--color-warning` | `#c9a057` | Warning states, pending badges |
| `--color-danger` | `#8b5a5a` | Error states, delete actions |
| `--color-info` | `#5a9a97` | Information states |

### Typography Scale

| Variable | Size | Pixels | Usage |
|----------|------|--------|-------|
| `--font-size-xs` | `0.875rem` | 14px | Minimum accessible size |
| `--font-size-sm` | `0.9375rem` | 15px | Secondary text |
| `--font-size-base` | `1rem` | 16px | Body text |
| `--font-size-md` | `1.0625rem` | 17px | Emphasized body |
| `--font-size-lg` | `1.125rem` | 18px | Large text |
| `--font-size-xl` | `1.25rem` | 20px | Subheadings |
| `--font-size-2xl` | `1.5rem` | 24px | Section headings |
| `--font-size-3xl` | `1.75rem` | 28px | Page headings |
| `--font-size-4xl` | `2rem` | 32px | Large headings |
| `--font-size-5xl` | `2.5rem` | 40px | Hero headings |

> **WCAG 2.1 AA Compliance**: Minimum font size is 14px (`--font-size-xs`).

### Font Weights

| Variable | Value | Usage |
|----------|-------|-------|
| `--font-weight-normal` | `400` | Body text |
| `--font-weight-medium` | `500` | Emphasized text |
| `--font-weight-semibold` | `600` | Labels, buttons |
| `--font-weight-bold` | `700` | Headings |

### Spacing Scale

| Variable | Size | Pixels | Usage |
|----------|------|--------|-------|
| `--spacing-xs` | `0.25rem` | 4px | Tight spacing |
| `--spacing-sm` | `0.5rem` | 8px | Small gaps |
| `--spacing-md` | `1rem` | 16px | Standard spacing |
| `--spacing-lg` | `1.5rem` | 24px | Section padding |
| `--spacing-xl` | `2rem` | 32px | Large gaps |
| `--spacing-xxl` | `3rem` | 48px | Section margins |

### Border Radius

| Variable | Size | Usage |
|----------|------|-------|
| `--radius-sm` | `0.25rem` | Small elements |
| `--radius-md` | `0.5rem` | Buttons, inputs |
| `--radius-lg` | `0.75rem` | Cards |
| `--radius-xl` | `1rem` | Large cards |
| `--radius-pill` | `50rem` | Pills, badges |

### Shadows

| Variable | Value | Usage |
|----------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Cards, dropdowns |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |

### Transitions

| Variable | Value | Usage |
|----------|-------|-------|
| `--transition-fast` | `150ms ease` | Hover states |
| `--transition-normal` | `300ms ease` | Standard animations |

---

## Components

### Patient Card

Patient cards display patient information with a sessions carousel.

```html
<div class="card patient-card" data-patient-id="1">
    <div class="card-header">
        <h5 class="patient-card__name mb-0">Patient Name</h5>
        <div class="patient-card__actions">
            <button class="btn btn-sm" data-patient-action="edit">Edit</button>
            <button class="btn btn-sm" data-patient-action="delete">Delete</button>
        </div>
    </div>
    <div class="card-body">
        <!-- Sessions carousel -->
    </div>
</div>
```

### Session Card

Session cards appear inside the carousel, showing session details.

```html
<div class="card session-card" data-session-id="1">
    <div class="card-header">
        <small class="session-date">Lunes 15/01/2026</small>
        <span class="badge text-bg-warning session-status">PENDIENTE</span>
    </div>
    <div class="card-body">
        <p class="session-price">$100.00</p>
    </div>
    <div class="card-footer">
        <!-- Action buttons -->
    </div>
</div>
```

### Status Badges

| Class | Usage |
|-------|-------|
| `.badge.text-bg-success` | Paid sessions |
| `.badge.text-bg-warning` | Pending sessions |

---

## Theme System

Themes are controlled by the `data-bs-theme` attribute on `<html>`.

### Dark Theme (Default)

```html
<html lang="es" data-bs-theme="dark">
```

Dark theme variables are defined in `themes/_dark.css`.

### Light Theme

```html
<html lang="es" data-bs-theme="light">
```

Light theme overrides are in `themes/_light.css`.

### Theme-Safe CSS

Always use CSS variables for colors:

```css
/* ✅ Correct - theme-aware */
.component {
    background-color: var(--card-bg);
    color: var(--text-primary);
}

/* ❌ Incorrect - hardcoded colors */
.component {
    background-color: #ffffff;
    color: #333333;
}
```

---

## Accessibility

### Touch Targets

All interactive elements have minimum 44x44px touch targets (WCAG 2.5.5).

### Color Contrast

All text meets 4.5:1 contrast ratio (WCAG 1.4.3).

### Focus Indicators

All focusable elements have visible `:focus-visible` styles.

---

## Adding New Styles

1. Identify the appropriate file based on component type
2. Use CSS variables from `_variables.css`
3. Follow BEM naming: `.block__element--modifier`
4. Test in both dark and light themes
5. Verify responsive behavior

---

*Last Updated: January 15, 2026*
