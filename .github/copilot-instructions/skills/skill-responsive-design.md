# Skill: Responsive Design

## Overview

This skill covers mobile-first responsive design, breakpoint systems, fluid typography, and responsive patterns for the Therapy Session Management Application. The goal is to create interfaces that work seamlessly across all device sizes.

---

## Mobile-First Approach

### Philosophy

Write CSS for mobile screens first, then add complexity for larger screens:

```css
/* ✅ Mobile-first: Base styles for mobile, enhance for larger */
.card {
    padding: 1rem;          /* Mobile default */
    flex-direction: column; /* Stack on mobile */
}

@media (min-width: 768px) {
    .card {
        padding: 1.5rem;        /* More padding on tablet+ */
        flex-direction: row;    /* Side-by-side on tablet+ */
    }
}

/* ❌ Desktop-first: Harder to maintain */
.card {
    padding: 1.5rem;
    flex-direction: row;
}

@media (max-width: 767px) {
    .card {
        padding: 1rem;
        flex-direction: column;
    }
}
```

### Benefits of Mobile-First

| Benefit | Description |
|---------|-------------|
| Performance | Mobile devices load only needed styles |
| Progressive Enhancement | Start simple, add features |
| Content Priority | Forces focus on essential content |
| Maintainability | Fewer overrides needed |

---

## Breakpoint System

### Bootstrap 5 Breakpoints

| Breakpoint | Class Prefix | Dimension | Devices |
|------------|--------------|-----------|---------|
| X-Small | - | < 576px | Portrait phones |
| Small | `sm` | ≥ 576px | Landscape phones |
| Medium | `md` | ≥ 768px | Tablets |
| Large | `lg` | ≥ 992px | Laptops |
| X-Large | `xl` | ≥ 1200px | Desktops |
| XX-Large | `xxl` | ≥ 1400px | Large desktops |

### CSS Custom Properties for Breakpoints

```css
:root {
    /* Breakpoint values (for reference, can't use in media queries) */
    --breakpoint-sm: 576px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 992px;
    --breakpoint-xl: 1200px;
    --breakpoint-xxl: 1400px;
}

/* Media queries must use literal values */
@media (min-width: 576px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 992px) { /* lg */ }
@media (min-width: 1200px) { /* xl */ }
@media (min-width: 1400px) { /* xxl */ }
```

### Breakpoint Mixins Pattern (for Reference)

```css
/* Named media queries for clarity */

/* Mobile only (xs) */
@media (max-width: 575.98px) { }

/* Small and up */
@media (min-width: 576px) { }

/* Medium and up */
@media (min-width: 768px) { }

/* Large and up */
@media (min-width: 992px) { }

/* Between breakpoints */
@media (min-width: 576px) and (max-width: 767.98px) { }
```

---

## Responsive Typography

### Fluid Typography with clamp()

```css
:root {
    /* Fluid font sizes that scale between viewport widths */
    
    /* Pattern: clamp(min, preferred, max) */
    /* preferred: calculated for smooth scaling */
    
    --font-size-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
    /* 16px → 18px between 320px and 1200px viewport */
    
    --font-size-lg: clamp(1.125rem, 1rem + 0.5vw, 1.375rem);
    /* 18px → 22px */
    
    --font-size-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.75rem);
    /* 20px → 28px */
    
    --font-size-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2.25rem);
    /* 24px → 36px */
    
    --font-size-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 3rem);
    /* 30px → 48px */
}

/* Usage */
h1 { font-size: var(--font-size-3xl); }
h2 { font-size: var(--font-size-2xl); }
h3 { font-size: var(--font-size-xl); }
body { font-size: var(--font-size-base); }
```

### Fixed Typography Scale (Alternative)

```css
:root {
    /* Base sizes */
    --font-size-xs: 0.875rem;   /* 14px - WCAG minimum */
    --font-size-sm: 0.9375rem;  /* 15px */
    --font-size-base: 1rem;     /* 16px */
    --font-size-md: 1.0625rem;  /* 17px */
    --font-size-lg: 1.125rem;   /* 18px */
    --font-size-xl: 1.25rem;    /* 20px */
    --font-size-2xl: 1.5rem;    /* 24px */
    --font-size-3xl: 1.75rem;   /* 28px */
    --font-size-4xl: 2rem;      /* 32px */
}

/* Adjust base for larger screens */
@media (min-width: 768px) {
    :root {
        --font-size-base: 1.0625rem;  /* 17px on tablet+ */
    }
}

@media (min-width: 1200px) {
    :root {
        --font-size-base: 1.125rem;   /* 18px on desktop+ */
    }
}
```

### Line Height Considerations

```css
:root {
    /* Tighter line height for headings */
    --line-height-tight: 1.2;
    --line-height-snug: 1.375;
    
    /* Normal for body text */
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.625;
    
    /* Looser for small text / captions */
    --line-height-loose: 1.75;
}

h1, h2, h3 { line-height: var(--line-height-tight); }
p, li { line-height: var(--line-height-normal); }
.caption { line-height: var(--line-height-loose); }
```

---

## Responsive Spacing

### Fluid Spacing Scale

```css
:root {
    /* Responsive spacing that scales with viewport */
    --space-1: clamp(0.25rem, 0.2rem + 0.25vw, 0.375rem);
    --space-2: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
    --space-3: clamp(0.75rem, 0.6rem + 0.75vw, 1.125rem);
    --space-4: clamp(1rem, 0.8rem + 1vw, 1.5rem);
    --space-5: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem);
    --space-6: clamp(2rem, 1.6rem + 2vw, 3rem);
    --space-8: clamp(3rem, 2.4rem + 3vw, 4.5rem);
}
```

### Container Padding

```css
:root {
    --container-padding: var(--space-4);
}

@media (min-width: 768px) {
    :root {
        --container-padding: var(--space-5);
    }
}

@media (min-width: 1200px) {
    :root {
        --container-padding: var(--space-6);
    }
}

.container {
    padding-left: var(--container-padding);
    padding-right: var(--container-padding);
}
```

---

## Responsive Layout Patterns

### Stack to Horizontal

```css
/* Mobile: stacked, Desktop: side-by-side */
.patient-card__actions {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

@media (min-width: 576px) {
    .patient-card__actions {
        flex-direction: row;
    }
}
```

### Responsive Grid

```css
/* Auto-fit grid that adapts to available space */
.patient-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: var(--space-4);
}

/* Or with explicit breakpoints */
.patient-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-4);
}

@media (min-width: 768px) {
    .patient-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1200px) {
    .patient-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

### Sidebar Layout

```css
/* Mobile: single column, Desktop: sidebar + main */
.dashboard-layout {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-4);
}

@media (min-width: 992px) {
    .dashboard-layout {
        grid-template-columns: 280px 1fr;
    }
}

/* Sticky sidebar on desktop */
@media (min-width: 992px) {
    .dashboard-layout__sidebar {
        position: sticky;
        top: var(--space-4);
        height: fit-content;
    }
}
```

### Responsive Cards

```css
.session-card {
    display: flex;
    flex-direction: column;
    padding: var(--space-3);
}

/* Horizontal layout on larger screens */
@media (min-width: 576px) {
    .session-card {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
    
    .session-card__info {
        flex: 1;
    }
    
    .session-card__actions {
        flex-shrink: 0;
    }
}
```

---

## Responsive Components

### Navigation

```css
.nav-header {
    display: flex;
    align-items: center;
    padding: var(--space-3) var(--space-4);
}

/* Mobile: hamburger menu */
.nav-header__toggle {
    display: block;
}

.nav-header__menu {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: var(--nav-bg);
}

.nav-header__menu--open {
    display: block;
}

/* Desktop: horizontal menu */
@media (min-width: 992px) {
    .nav-header__toggle {
        display: none;
    }
    
    .nav-header__menu {
        display: flex;
        position: static;
        background: transparent;
    }
}
```

### Buttons

```css
/* Mobile: full width stacked buttons */
.btn-group--responsive {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.btn-group--responsive .btn {
    width: 100%;
}

/* Desktop: inline buttons */
@media (min-width: 576px) {
    .btn-group--responsive {
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .btn-group--responsive .btn {
        width: auto;
    }
}
```

### Tables

```css
/* Mobile: card-style stacked layout */
.table-responsive {
    display: block;
}

.table-responsive thead {
    display: none;
}

.table-responsive tr {
    display: block;
    padding: var(--space-3);
    border-bottom: 1px solid var(--border-default);
}

.table-responsive td {
    display: flex;
    justify-content: space-between;
    padding: var(--space-1) 0;
}

.table-responsive td::before {
    content: attr(data-label);
    font-weight: var(--font-weight-semibold);
}

/* Desktop: traditional table */
@media (min-width: 768px) {
    .table-responsive thead {
        display: table-header-group;
    }
    
    .table-responsive tr {
        display: table-row;
        padding: 0;
    }
    
    .table-responsive td {
        display: table-cell;
        padding: var(--space-3);
    }
    
    .table-responsive td::before {
        display: none;
    }
}
```

### Modals

```css
.modal {
    --modal-width: 100%;
    --modal-max-height: 100vh;
    --modal-margin: 0;
    --modal-border-radius: 0;
}

.modal__dialog {
    width: var(--modal-width);
    max-height: var(--modal-max-height);
    margin: var(--modal-margin);
    border-radius: var(--modal-border-radius);
}

/* Tablet and up: centered modal */
@media (min-width: 576px) {
    .modal {
        --modal-width: 500px;
        --modal-max-height: calc(100vh - 3.5rem);
        --modal-margin: 1.75rem auto;
        --modal-border-radius: var(--radius-lg);
    }
}

/* Large modal variant */
@media (min-width: 992px) {
    .modal--large {
        --modal-width: 800px;
    }
}
```

---

## Responsive Images

### Fluid Images

```css
/* Images never exceed container */
img {
    max-width: 100%;
    height: auto;
}

/* Background images */
.hero {
    background-image: url('hero-mobile.jpg');
    background-size: cover;
    background-position: center;
}

@media (min-width: 768px) {
    .hero {
        background-image: url('hero-tablet.jpg');
    }
}

@media (min-width: 1200px) {
    .hero {
        background-image: url('hero-desktop.jpg');
    }
}
```

### Picture Element with Art Direction

```html
<picture>
    <source media="(min-width: 1200px)" srcset="hero-desktop.jpg">
    <source media="(min-width: 768px)" srcset="hero-tablet.jpg">
    <img src="hero-mobile.jpg" alt="Hero image">
</picture>
```

---

## Touch-Friendly Design

### Touch Target Sizes

```css
/* Minimum touch target: 44x44px (WCAG 2.1) */
.btn,
.nav-link,
.form-control,
[type="checkbox"] + label,
[type="radio"] + label {
    min-height: 44px;
    min-width: 44px;
}

/* Adequate spacing between touch targets */
.btn-group .btn {
    margin: 2px;
}

.nav-list .nav-item {
    margin-bottom: var(--space-1);
}
```

### Hover vs Touch

```css
/* Hover states only for devices that support it */
@media (hover: hover) {
    .btn:hover {
        background: var(--interactive-primary-hover);
    }
    
    .card:hover {
        box-shadow: var(--shadow-lg);
    }
}

/* Active state for touch devices */
.btn:active {
    transform: scale(0.98);
}
```

---

## Testing Responsive Design

### Device Simulation Checklist

| Viewport | Width | Test Points |
|----------|-------|-------------|
| iPhone SE | 375px | Smallest common phone |
| iPhone 14 | 390px | Standard phone |
| iPad Mini | 768px | Tablet breakpoint |
| iPad Pro | 1024px | Large tablet |
| Laptop | 1280px | Standard laptop |
| Desktop | 1920px | Full HD monitor |

### Chrome DevTools Testing

```javascript
// Test with MCP Chrome DevTools
mcp_chrome-devtoo_resize_page({ width: 375, height: 667 });  // Mobile
mcp_chrome-devtoo_resize_page({ width: 768, height: 1024 }); // Tablet
mcp_chrome-devtoo_resize_page({ width: 1200, height: 800 }); // Desktop
```

### Testing Checklist

- [ ] Content readable at all sizes
- [ ] No horizontal scrolling
- [ ] Touch targets ≥ 44px
- [ ] Text not truncated unexpectedly
- [ ] Images scale properly
- [ ] Navigation accessible on mobile
- [ ] Forms usable on all devices
- [ ] Modals fit viewport
- [ ] Carousels work with touch/swipe

---

## Project-Specific Patterns

### Patient Card Grid (Dashboard)

```css
.patient-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-4);
}

@media (min-width: 576px) {
    .patient-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 992px) {
    .patient-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (min-width: 1400px) {
    .patient-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

### Session Carousel

```css
.session-carousel {
    position: relative;
    overflow: hidden;
}

/* Navigation arrows */
.session-carousel__nav {
    display: none;
}

@media (min-width: 768px) {
    .session-carousel__nav {
        display: flex;
    }
}

/* Indicators */
.session-carousel__indicators {
    display: flex;
    justify-content: center;
    gap: var(--space-2);
    padding: var(--space-2);
}
```

### Filter Bar

```css
.filter-bar {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.filter-bar__buttons {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
}

.filter-bar .btn {
    flex: 1 1 auto;
    min-width: 80px;
}

@media (min-width: 576px) {
    .filter-bar {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    
    .filter-bar .btn {
        flex: 0 0 auto;
    }
}
```

---

## Responsive Design Checklist

### Mobile-First
- [ ] Base styles work on 320px viewport
- [ ] Media queries use `min-width` (not `max-width`)
- [ ] Progressive enhancement for larger screens

### Breakpoints
- [ ] Consistent breakpoint usage
- [ ] No arbitrary pixel values
- [ ] Tested at each breakpoint

### Typography
- [ ] Font sizes use relative units (rem)
- [ ] Line height appropriate for reading
- [ ] Minimum 14px for body text (WCAG)

### Layout
- [ ] Flexible grids (flexbox/grid)
- [ ] No fixed widths (except max-width)
- [ ] Proper use of container widths

### Touch
- [ ] Touch targets ≥ 44px
- [ ] Adequate spacing between targets
- [ ] Hover states have touch alternatives

### Testing
- [ ] Tested on real devices (not just emulator)
- [ ] Portrait and landscape orientations
- [ ] Different screen densities (retina)

---

## Related Skills

- [skill-css-architecture.md](./skill-css-architecture.md) - File organization
- [skill-css-custom-properties.md](./skill-css-custom-properties.md) - Responsive variables
- [skill-wcag-accessibility.md](./skill-wcag-accessibility.md) - Touch targets, text sizing

---

*Last Updated: January 15, 2026*
