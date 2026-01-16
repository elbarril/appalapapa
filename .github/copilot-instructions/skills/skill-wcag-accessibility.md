# Skill: WCAG 2.1 AA Accessibility

## Overview

This skill covers Web Content Accessibility Guidelines (WCAG) 2.1 Level AA compliance for the Therapy Session Management Application. All frontend changes must meet these standards.

---

## Core Principles (POUR)

### 1. Perceivable
Users must be able to perceive all information and UI components.

**Requirements:**
- Text alternatives for non-text content
- Captions/alternatives for multimedia
- Content adaptable to different presentations
- Distinguishable content (color, contrast, audio control)

### 2. Operable
Users must be able to operate all interface components.

**Requirements:**
- Keyboard accessible
- Enough time to read/use content
- No seizure-inducing content
- Navigable structure
- Input modalities beyond keyboard

### 3. Understandable
Users must understand information and UI operation.

**Requirements:**
- Readable text
- Predictable behavior
- Input assistance (error prevention/correction)

### 4. Robust
Content must be robust enough for assistive technologies.

**Requirements:**
- Compatible with current/future user agents
- Valid, parseable markup

---

## Color Contrast Requirements

### Text Contrast Ratios

| Element Type | Minimum Ratio | Tool |
|--------------|---------------|------|
| Normal text (< 18px) | 4.5:1 | WebAIM Contrast Checker |
| Large text (≥ 18px or 14px bold) | 3:1 | WebAIM Contrast Checker |
| UI components & graphics | 3:1 | WebAIM Contrast Checker |
| Focus indicators | 3:1 | WebAIM Contrast Checker |

### Current Theme Colors (Verify These)

```css
/* Dark Mode - Verify contrast against #212529 background */
--bs-body-bg: #212529;
--bs-body-color: #dee2e6;  /* Must be 4.5:1 */

/* Light Mode - Verify contrast against #ffffff background */
--bs-body-bg: #ffffff;
--bs-body-color: #212529;  /* Must be 4.5:1 */

/* Badge Colors - Check against card backgrounds */
.badge.bg-warning { /* Yellow on dark - CHECK THIS */ }
.badge.bg-success { /* Green on dark - CHECK THIS */ }
```

### Contrast Checking Process

1. **Use Chrome DevTools**:
   ```
   mcp_chrome-devtoo_evaluate_script
   function: () => {
     // Get computed styles for text elements
     const elements = document.querySelectorAll('p, span, h1, h2, h3, .badge');
     return Array.from(elements).map(el => ({
       text: el.textContent.substring(0, 20),
       color: getComputedStyle(el).color,
       background: getComputedStyle(el).backgroundColor
     }));
   }
   ```

2. **Use axe-core for automated testing**:
   ```javascript
   // In browser console
   axe.run().then(results => console.log(results.violations));
   ```

---

## Focus Management

### Visible Focus Indicators

All interactive elements MUST have visible focus states.

```css
/* ✅ CORRECT - High visibility focus */
:focus-visible {
    outline: 2px solid var(--bs-primary);
    outline-offset: 2px;
}

/* ✅ For dark backgrounds */
.btn:focus-visible {
    outline: 2px solid #fff;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.25);
}

/* ❌ NEVER remove focus outlines */
:focus {
    outline: none;  /* FORBIDDEN */
}
```

### Focus Order

Focus order must follow logical reading order (top-to-bottom, left-to-right for LTR languages).

```html
<!-- ✅ Logical tab order -->
<form>
    <input name="email" tabindex="0">    <!-- 1st -->
    <input name="password" tabindex="0"> <!-- 2nd -->
    <button type="submit" tabindex="0">  <!-- 3rd -->
</form>

<!-- ❌ Avoid positive tabindex -->
<input tabindex="3">  <!-- Forces unnatural order -->
```

### Focus Trapping in Modals

When a modal opens, focus must be trapped within it.

```javascript
/**
 * Trap focus within a modal element
 * @param {HTMLElement} modalElement - The modal container
 */
function trapFocus(modalElement) {
    const focusableSelectors = [
        'button:not([disabled])',
        'input:not([disabled])',
        'select:not([disabled])',
        'textarea:not([disabled])',
        'a[href]',
        '[tabindex]:not([tabindex="-1"])'
    ].join(', ');
    
    const focusableElements = modalElement.querySelectorAll(focusableSelectors);
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    // Focus first element when modal opens
    firstElement?.focus();
    
    // Handle Tab key
    modalElement.addEventListener('keydown', (e) => {
        if (e.key !== 'Tab') return;
        
        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement?.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement?.focus();
        }
    });
}
```

---

## ARIA Patterns

### Live Regions for Dynamic Content

Use ARIA live regions to announce dynamic changes to screen readers.

```html
<!-- Toast notifications - MUST have live region -->
<div id="toast-container" 
     role="status" 
     aria-live="polite" 
     aria-atomic="true">
    <!-- Toasts inserted here will be announced -->
</div>

<!-- For urgent errors -->
<div role="alert" aria-live="assertive">
    Error: Session could not be saved.
</div>
```

### Form Validation Announcements

```html
<!-- ✅ Accessible form error -->
<div class="mb-3">
    <label for="email" class="form-label">Email</label>
    <input type="email" 
           id="email" 
           class="form-control is-invalid"
           aria-describedby="email-error"
           aria-invalid="true">
    <div id="email-error" class="invalid-feedback" role="alert">
        Por favor ingrese un email válido.
    </div>
</div>
```

### Button States

```html
<!-- Loading state -->
<button type="submit" 
        aria-busy="true" 
        aria-label="Guardando...">
    <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
    <span>Guardando...</span>
</button>

<!-- Toggle button -->
<button type="button"
        aria-pressed="false"
        aria-label="Marcar como pagado">
    Pendiente
</button>
```

---

## Semantic HTML Requirements

### Heading Hierarchy

```html
<!-- ✅ CORRECT - Logical hierarchy -->
<h1>Panel de Pacientes</h1>
    <h2>Juan García</h2>
        <h3>Sesiones</h3>
    <h2>María López</h2>
        <h3>Sesiones</h3>

<!-- ❌ WRONG - Skipping levels -->
<h1>Panel</h1>
    <h3>Paciente</h3>  <!-- Missing h2! -->
```

### Landmark Regions

```html
<body>
    <a href="#main-content" class="skip-link">Saltar al contenido</a>
    
    <header role="banner">
        <nav role="navigation" aria-label="Navegación principal">
            <!-- Navigation links -->
        </nav>
    </header>
    
    <main id="main-content" role="main">
        <!-- Page content -->
    </main>
    
    <footer role="contentinfo">
        <!-- Footer content -->
    </footer>
</body>
```

---

## Testing Checklist

### Automated Testing
- [ ] Run axe-core browser extension
- [ ] Run Lighthouse accessibility audit
- [ ] Check color contrast with WebAIM tool
- [ ] Validate HTML with W3C validator

### Manual Testing
- [ ] Navigate entire page with keyboard only (Tab, Shift+Tab, Enter, Escape)
- [ ] Test with screen reader (NVDA on Windows, VoiceOver on Mac)
- [ ] Verify focus is visible on all interactive elements
- [ ] Test at 200% zoom level
- [ ] Test with high contrast mode
- [ ] Verify all images have alt text
- [ ] Test form submission with errors

### Screen Reader Announcements to Verify
- [ ] Page title announced on navigation
- [ ] Form labels read correctly
- [ ] Error messages announced
- [ ] Toast notifications announced
- [ ] Modal open/close announced
- [ ] Dynamic content changes announced

---

## Common Fixes

### Issue: Badge Color Contrast
```css
/* Before - Poor contrast */
.badge.bg-warning {
    background-color: #ffc107;
    color: #000;  /* May not be enough */
}

/* After - Improved contrast */
.badge.bg-warning {
    background-color: #ffc107;
    color: #1a1a1a;
    font-weight: 600;  /* Bolder text helps */
}
```

### Issue: Icon-Only Buttons
```html
<!-- ❌ Missing accessible name -->
<button class="btn"><i class="bi bi-trash"></i></button>

<!-- ✅ With accessible name -->
<button class="btn" aria-label="Eliminar sesión">
    <i class="bi bi-trash" aria-hidden="true"></i>
</button>

<!-- ✅ Alternative: visually hidden text -->
<button class="btn">
    <i class="bi bi-trash" aria-hidden="true"></i>
    <span class="visually-hidden">Eliminar sesión</span>
</button>
```

### Issue: Carousel Accessibility
```html
<!-- Accessible carousel controls -->
<div class="carousel" 
     role="region" 
     aria-label="Sesiones de Juan García"
     aria-roledescription="carrusel">
    
    <button class="carousel-control-prev" 
            aria-label="Sesión anterior"
            aria-controls="carousel-123">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    </button>
    
    <div class="carousel-indicators" role="tablist">
        <button role="tab" 
                aria-selected="true" 
                aria-label="Sesión 1 de 5">
        </button>
    </div>
</div>
```

---

## Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [axe DevTools Extension](https://www.deque.com/axe/devtools/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

---

*Last Updated: January 15, 2026*
