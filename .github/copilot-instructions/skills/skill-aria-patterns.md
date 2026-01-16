# Skill: ARIA Patterns & Best Practices

## Overview

This skill covers ARIA (Accessible Rich Internet Applications) implementation patterns for the Therapy Session Management Application. ARIA provides attributes that define ways to make web content more accessible to people with disabilities.

---

## Golden Rules of ARIA

### Rule 1: Don't Use ARIA If You Don't Need It

Native HTML elements have built-in accessibility. Use them first.

```html
<!-- ❌ Unnecessary ARIA -->
<div role="button" tabindex="0" aria-pressed="false">Click me</div>

<!-- ✅ Use native element -->
<button type="button">Click me</button>
```

### Rule 2: Don't Change Native Semantics

Don't override native element semantics unless absolutely necessary.

```html
<!-- ❌ Confusing semantics -->
<h2 role="tab">Tab heading</h2>

<!-- ✅ Correct approach -->
<div role="tab"><h2>Tab heading</h2></div>
```

### Rule 3: All Interactive ARIA Controls Must Be Keyboard Accessible

If you use `role="button"`, it must work with Enter and Space keys.

```javascript
// If using div as button (not recommended, but if necessary)
element.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        element.click();
    }
});
```

### Rule 4: Don't Hide Focusable Elements

Never use `role="presentation"` or `aria-hidden="true"` on focusable elements.

```html
<!-- ❌ WRONG - Hidden but focusable -->
<button aria-hidden="true">Hidden Button</button>

<!-- ✅ If truly hidden, also disable focus -->
<button aria-hidden="true" tabindex="-1" disabled>Hidden Button</button>
```

### Rule 5: All Interactive Elements Need Accessible Names

Every button, link, input must have a name that screen readers can announce.

```html
<!-- ❌ No accessible name -->
<button><i class="bi bi-plus"></i></button>

<!-- ✅ With aria-label -->
<button aria-label="Agregar sesión">
    <i class="bi bi-plus" aria-hidden="true"></i>
</button>
```

---

## ARIA Roles

### Landmark Roles

Use landmarks to help screen reader users navigate quickly.

```html
<header role="banner">           <!-- Page header (use once) -->
<nav role="navigation">          <!-- Navigation regions -->
<main role="main">               <!-- Main content (use once) -->
<aside role="complementary">     <!-- Supporting content -->
<footer role="contentinfo">      <!-- Page footer (use once) -->
<form role="form">               <!-- Form regions -->
<section role="region">          <!-- Generic regions (need aria-label) -->
<search role="search">           <!-- Search functionality -->
```

**Application in this project:**
```html
<body>
    <header role="banner">
        <nav role="navigation" aria-label="Navegación principal">
            <!-- Navbar content -->
        </nav>
    </header>
    
    <main role="main" id="main-content">
        <section role="region" aria-labelledby="patients-heading">
            <h1 id="patients-heading">Panel de Pacientes</h1>
            <!-- Patient list -->
        </section>
    </main>
    
    <footer role="contentinfo">
        <!-- Footer -->
    </footer>
</body>
```

### Widget Roles

Common interactive widget roles used in this application:

| Role | Use Case | Example |
|------|----------|---------|
| `button` | Clickable actions | Delete, Edit buttons |
| `dialog` | Modal dialogs | Edit patient modal |
| `alertdialog` | Important dialogs requiring response | Delete confirmation |
| `alert` | Important, time-sensitive messages | Error notifications |
| `status` | Status messages | Success toasts |
| `tablist/tab/tabpanel` | Tab interfaces | If tabs are added |
| `menu/menuitem` | Dropdown menus | Action menus |
| `progressbar` | Loading indicators | Form submission |

---

## ARIA States and Properties

### Common States

```html
<!-- Disabled state -->
<button aria-disabled="true" class="btn disabled">
    Deshabilitado
</button>

<!-- Expanded state (for dropdowns, accordions) -->
<button aria-expanded="false" aria-controls="dropdown-menu">
    Opciones
</button>
<div id="dropdown-menu" hidden>
    <!-- Menu items -->
</div>

<!-- Selected state -->
<button role="tab" aria-selected="true">Tab 1</button>
<button role="tab" aria-selected="false">Tab 2</button>

<!-- Pressed state (toggle buttons) -->
<button aria-pressed="false" class="toggle-payment-btn">
    Pendiente
</button>

<!-- Busy state (loading) -->
<button aria-busy="true">
    <span class="spinner-border spinner-border-sm"></span>
    Cargando...
</button>

<!-- Invalid state (form validation) -->
<input type="email" aria-invalid="true" aria-describedby="email-error">
<span id="email-error">Email inválido</span>
```

### Relationship Properties

```html
<!-- aria-labelledby: Label from another element -->
<section aria-labelledby="section-title">
    <h2 id="section-title">Sesiones de Terapia</h2>
</section>

<!-- aria-describedby: Additional description -->
<input type="password" 
       aria-describedby="password-help password-error">
<small id="password-help">Mínimo 8 caracteres</small>
<span id="password-error" class="text-danger"></span>

<!-- aria-controls: Element controls another -->
<button aria-controls="session-list" aria-expanded="true">
    Mostrar sesiones
</button>
<ul id="session-list">...</ul>

<!-- aria-owns: Establishes parent-child relationship -->
<div role="listbox" aria-owns="option-1 option-2 option-3">
    <!-- Options may be elsewhere in DOM -->
</div>
```

---

## Live Regions

Live regions announce dynamic content changes to screen readers.

### Types of Live Regions

```html
<!-- Polite: Waits for user to stop interacting -->
<div aria-live="polite">
    Se guardó correctamente.
</div>

<!-- Assertive: Interrupts immediately (use sparingly) -->
<div aria-live="assertive" role="alert">
    Error: No se pudo guardar.
</div>

<!-- Off: No announcements -->
<div aria-live="off">
    <!-- Silent updates -->
</div>
```

### Implementation for Toast Notifications

```html
<!-- Toast container with live region -->
<div id="toast-container" 
     class="toast-container position-fixed bottom-0 end-0 p-3"
     role="status"
     aria-live="polite"
     aria-atomic="true">
    <!-- Toasts inserted here will be announced -->
</div>
```

```javascript
/**
 * Show accessible toast notification
 * @param {string} message - Message to display
 * @param {string} type - 'success' | 'error' | 'warning' | 'info'
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    
    // For errors, use assertive
    if (type === 'error') {
        container.setAttribute('aria-live', 'assertive');
        container.setAttribute('role', 'alert');
    } else {
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('role', 'status');
    }
    
    const toast = document.createElement('div');
    toast.className = `toast show bg-${type === 'error' ? 'danger' : type}`;
    toast.innerHTML = `
        <div class="toast-body">
            ${message}
            <button type="button" 
                    class="btn-close" 
                    aria-label="Cerrar notificación"
                    onclick="this.closest('.toast').remove()">
            </button>
        </div>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => toast.remove(), 5000);
}
```

### aria-atomic

Controls whether entire region or just changes are announced.

```html
<!-- Announce entire region on any change -->
<div aria-live="polite" aria-atomic="true">
    Items en carrito: <span id="cart-count">5</span>
</div>

<!-- Announce only the changed part -->
<ul aria-live="polite" aria-atomic="false">
    <li>Item 1</li>
    <li>Item 2</li>
    <!-- Only new items announced -->
</ul>
```

---

## Modal/Dialog Pattern

### Accessible Modal Structure

```html
<div id="editModal" 
     class="modal" 
     role="dialog"
     aria-modal="true"
     aria-labelledby="editModalTitle"
     aria-describedby="editModalDescription">
    
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editModalTitle">
                    Editar Paciente
                </h5>
                <button type="button" 
                        class="btn-close" 
                        data-bs-dismiss="modal"
                        aria-label="Cerrar modal">
                </button>
            </div>
            
            <div class="modal-body" id="editModalDescription">
                <!-- Form content -->
            </div>
            
            <div class="modal-footer">
                <button type="button" 
                        class="btn btn-secondary" 
                        data-bs-dismiss="modal">
                    Cancelar
                </button>
                <button type="submit" class="btn btn-primary">
                    Guardar
                </button>
            </div>
        </div>
    </div>
</div>
```

### Modal Focus Management

```javascript
/**
 * Handle modal accessibility
 * @param {HTMLElement} modal - Modal element
 */
function setupModalAccessibility(modal) {
    const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    // Store previously focused element
    let previouslyFocused;
    
    modal.addEventListener('show.bs.modal', () => {
        previouslyFocused = document.activeElement;
    });
    
    modal.addEventListener('shown.bs.modal', () => {
        firstFocusable?.focus();
    });
    
    modal.addEventListener('hidden.bs.modal', () => {
        previouslyFocused?.focus();
    });
    
    // Trap focus within modal
    modal.addEventListener('keydown', (e) => {
        if (e.key !== 'Tab') return;
        
        if (e.shiftKey) {
            if (document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            }
        } else {
            if (document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
}
```

---

## Form Accessibility Patterns

### Form with Validation

```html
<form novalidate aria-describedby="form-instructions">
    <p id="form-instructions" class="text-body-secondary">
        Los campos marcados con * son obligatorios.
    </p>
    
    <div class="mb-3">
        <label for="name" class="form-label">
            Nombre <span aria-hidden="true">*</span>
            <span class="visually-hidden">(obligatorio)</span>
        </label>
        <input type="text" 
               id="name" 
               class="form-control"
               required
               aria-required="true"
               aria-invalid="false"
               aria-describedby="name-error">
        <div id="name-error" class="invalid-feedback" role="alert">
            <!-- Error message inserted by JS -->
        </div>
    </div>
    
    <button type="submit">Guardar</button>
</form>
```

### Dynamic Error Handling

```javascript
/**
 * Show form validation error accessibly
 * @param {HTMLInputElement} input - Input element
 * @param {string} message - Error message
 */
function showFieldError(input, message) {
    const errorId = `${input.id}-error`;
    const errorElement = document.getElementById(errorId);
    
    // Update input state
    input.classList.add('is-invalid');
    input.setAttribute('aria-invalid', 'true');
    
    // Show error message
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    // Focus the invalid field
    input.focus();
}

/**
 * Clear form validation error
 * @param {HTMLInputElement} input - Input element
 */
function clearFieldError(input) {
    const errorId = `${input.id}-error`;
    const errorElement = document.getElementById(errorId);
    
    input.classList.remove('is-invalid');
    input.setAttribute('aria-invalid', 'false');
    
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}
```

---

## Carousel/Slider Pattern

### Accessible Carousel Structure

```html
<div class="carousel slide" 
     id="sessions-carousel-123"
     role="group"
     aria-roledescription="carrusel"
     aria-label="Sesiones de Juan García">
    
    <!-- Carousel indicators as tabs -->
    <div class="carousel-indicators" role="tablist">
        <button type="button" 
                role="tab"
                data-bs-target="#sessions-carousel-123" 
                data-bs-slide-to="0" 
                class="active"
                aria-selected="true"
                aria-label="Sesión 1 de 3: 15 de enero">
        </button>
        <button type="button"
                role="tab" 
                data-bs-target="#sessions-carousel-123" 
                data-bs-slide-to="1"
                aria-selected="false"
                aria-label="Sesión 2 de 3: 8 de enero">
        </button>
    </div>
    
    <!-- Carousel items -->
    <div class="carousel-inner" role="tabpanel">
        <div class="carousel-item active" aria-hidden="false">
            <!-- Session card -->
        </div>
        <div class="carousel-item" aria-hidden="true">
            <!-- Session card -->
        </div>
    </div>
    
    <!-- Navigation controls -->
    <button class="carousel-control-prev" 
            type="button"
            data-bs-target="#sessions-carousel-123" 
            data-bs-slide="prev"
            aria-label="Sesión anterior">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    </button>
    
    <button class="carousel-control-next" 
            type="button"
            data-bs-target="#sessions-carousel-123" 
            data-bs-slide="next"
            aria-label="Siguiente sesión">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
    </button>
</div>
```

---

## Testing ARIA Implementation

### Using Chrome DevTools

```javascript
// Get all elements with ARIA attributes
mcp_chrome-devtoo_evaluate_script
function: () => {
    const ariaElements = document.querySelectorAll('[aria-label], [aria-labelledby], [role]');
    return Array.from(ariaElements).map(el => ({
        tag: el.tagName,
        role: el.getAttribute('role'),
        ariaLabel: el.getAttribute('aria-label'),
        ariaLabelledby: el.getAttribute('aria-labelledby')
    }));
}
```

### Checklist

- [ ] All buttons have accessible names
- [ ] All form inputs have labels
- [ ] Modals have `role="dialog"` and `aria-modal="true"`
- [ ] Dynamic content has appropriate live regions
- [ ] Focus is managed correctly in modals
- [ ] Error states are announced
- [ ] Loading states are announced
- [ ] Carousel navigation is accessible

---

## Resources

- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [MDN ARIA Reference](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)
- [WebAIM ARIA Introduction](https://webaim.org/techniques/aria/)

---

*Last Updated: January 15, 2026*
