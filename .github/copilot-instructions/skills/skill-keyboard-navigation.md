# Skill: Keyboard Navigation

## Overview

This skill covers keyboard accessibility implementation for the Therapy Session Management Application. All functionality must be accessible via keyboard alone for users who cannot use a mouse.

---

## Essential Keyboard Interactions

### Standard Keys

| Key | Action |
|-----|--------|
| `Tab` | Move to next focusable element |
| `Shift + Tab` | Move to previous focusable element |
| `Enter` | Activate buttons, links, submit forms |
| `Space` | Activate buttons, toggle checkboxes |
| `Escape` | Close modals, dialogs, dropdowns |
| `Arrow Keys` | Navigate within components (menus, carousels, tabs) |
| `Home` | Go to first item in a list |
| `End` | Go to last item in a list |

### Component-Specific Keys

| Component | Keys | Behavior |
|-----------|------|----------|
| Dropdown Menu | `↓/↑` | Navigate options |
| Tabs | `←/→` | Switch tabs |
| Carousel | `←/→` | Previous/next slide |
| Modal | `Tab` | Cycle within modal |
| Modal | `Escape` | Close modal |
| Date Picker | `Arrow keys` | Navigate dates |
| Autocomplete | `↓/↑` + `Enter` | Navigate and select |

---

## Focus Management

### Focusable Elements

These elements are naturally focusable:
- `<a href="...">` (links with href)
- `<button>` (not disabled)
- `<input>`, `<select>`, `<textarea>` (not disabled)
- `<details>`, `<summary>`
- Elements with `tabindex="0"`

### Making Elements Focusable

```html
<!-- Natural focus (preferred) -->
<button type="button">Click me</button>

<!-- Add to tab order -->
<div tabindex="0" role="button">Custom button</div>

<!-- Programmatically focusable only (not in tab order) -->
<div tabindex="-1" id="focus-target">
    Will receive focus via JavaScript
</div>
```

### Focus Order Best Practices

```html
<!-- ✅ CORRECT: Natural DOM order = visual order -->
<form>
    <input name="first" placeholder="First Name">
    <input name="last" placeholder="Last Name">
    <input name="email" placeholder="Email">
    <button type="submit">Submit</button>
</form>

<!-- ❌ WRONG: Avoid positive tabindex -->
<input tabindex="3">  <!-- Creates confusing order -->
<input tabindex="1">
<input tabindex="2">
```

---

## Focus Indicators

### CSS Implementation

```css
/* Base focus style for all elements */
:focus-visible {
    outline: 2px solid var(--bs-primary);
    outline-offset: 2px;
}

/* Remove default outline (replaced with :focus-visible) */
:focus:not(:focus-visible) {
    outline: none;
}

/* High contrast focus for buttons */
.btn:focus-visible {
    outline: 2px solid currentColor;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(var(--bs-primary-rgb), 0.25);
}

/* Focus within cards */
.card:focus-within {
    box-shadow: 0 0 0 2px var(--bs-primary);
}

/* Dark mode focus adjustments */
[data-bs-theme="dark"] :focus-visible {
    outline-color: #8bb9fe;
}

/* Skip link visible on focus */
.skip-link {
    position: absolute;
    left: -9999px;
    z-index: 9999;
}

.skip-link:focus {
    left: 50%;
    transform: translateX(-50%);
    top: 10px;
    background: var(--bs-primary);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    text-decoration: none;
}
```

---

## Skip Links

### Implementation

```html
<!-- First element in <body> -->
<a href="#main-content" class="skip-link">
    Saltar al contenido principal
</a>

<!-- Target in page -->
<main id="main-content" tabindex="-1">
    <!-- Page content -->
</main>
```

```css
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--bs-primary);
    color: white;
    padding: 8px 16px;
    z-index: 10000;
    text-decoration: none;
    font-weight: 600;
    transition: top 0.2s;
}

.skip-link:focus {
    top: 0;
}
```

---

## Modal Keyboard Handling

### Focus Trapping

```javascript
/**
 * Trap keyboard focus within a modal
 * @param {HTMLElement} modal - The modal element
 */
function trapFocusInModal(modal) {
    const focusableSelector = [
        'button:not([disabled]):not([tabindex="-1"])',
        'input:not([disabled]):not([tabindex="-1"])',
        'select:not([disabled]):not([tabindex="-1"])',
        'textarea:not([disabled]):not([tabindex="-1"])',
        'a[href]:not([tabindex="-1"])',
        '[tabindex="0"]'
    ].join(', ');
    
    const focusableElements = modal.querySelectorAll(focusableSelector);
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    function handleKeydown(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                // Shift + Tab
                if (document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                }
            } else {
                // Tab
                if (document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        }
        
        // Escape to close
        if (e.key === 'Escape') {
            closeModal(modal);
        }
    }
    
    modal.addEventListener('keydown', handleKeydown);
    
    // Return cleanup function
    return () => modal.removeEventListener('keydown', handleKeydown);
}
```

### Modal Open/Close Focus Restoration

```javascript
let previouslyFocusedElement = null;

/**
 * Open modal with focus management
 * @param {string} modalId - ID of modal to open
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    
    // Store currently focused element
    previouslyFocusedElement = document.activeElement;
    
    // Show modal (Bootstrap)
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
    
    // Focus first focusable element after modal opens
    modal.addEventListener('shown.bs.modal', () => {
        const firstInput = modal.querySelector('input, button, [tabindex="0"]');
        firstInput?.focus();
    }, { once: true });
}

/**
 * Close modal and restore focus
 * @param {HTMLElement} modal - Modal element
 */
function closeModal(modal) {
    const bsModal = bootstrap.Modal.getInstance(modal);
    bsModal?.hide();
    
    // Restore focus after modal closes
    modal.addEventListener('hidden.bs.modal', () => {
        previouslyFocusedElement?.focus();
        previouslyFocusedElement = null;
    }, { once: true });
}
```

---

## Carousel Keyboard Navigation

### Arrow Key Navigation

```javascript
/**
 * Add keyboard navigation to carousel
 * @param {HTMLElement} carousel - Carousel element
 */
function setupCarouselKeyboard(carousel) {
    const bsCarousel = bootstrap.Carousel.getOrCreateInstance(carousel);
    
    carousel.addEventListener('keydown', (e) => {
        switch (e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                bsCarousel.prev();
                announceSlide(carousel, 'anterior');
                break;
            case 'ArrowRight':
                e.preventDefault();
                bsCarousel.next();
                announceSlide(carousel, 'siguiente');
                break;
            case 'Home':
                e.preventDefault();
                bsCarousel.to(0);
                announceSlide(carousel, 'primera');
                break;
            case 'End':
                e.preventDefault();
                const lastIndex = carousel.querySelectorAll('.carousel-item').length - 1;
                bsCarousel.to(lastIndex);
                announceSlide(carousel, 'última');
                break;
        }
    });
}

/**
 * Announce slide change to screen readers
 */
function announceSlide(carousel, direction) {
    const activeItem = carousel.querySelector('.carousel-item.active');
    const totalItems = carousel.querySelectorAll('.carousel-item').length;
    const currentIndex = Array.from(carousel.querySelectorAll('.carousel-item'))
        .indexOf(activeItem) + 1;
    
    // Use live region to announce
    const announcement = `Sesión ${currentIndex} de ${totalItems}`;
    announceToScreenReader(announcement);
}
```

---

## Dropdown/Menu Keyboard Navigation

### Implementation Pattern

```javascript
/**
 * Add keyboard navigation to dropdown menu
 * @param {HTMLElement} dropdown - Dropdown container
 */
function setupDropdownKeyboard(dropdown) {
    const trigger = dropdown.querySelector('[data-bs-toggle="dropdown"]');
    const menu = dropdown.querySelector('.dropdown-menu');
    const items = menu.querySelectorAll('.dropdown-item:not(.disabled)');
    let currentIndex = -1;
    
    trigger.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            // Open dropdown and focus first item
            bootstrap.Dropdown.getOrCreateInstance(trigger).show();
            currentIndex = 0;
            items[0]?.focus();
        }
    });
    
    menu.addEventListener('keydown', (e) => {
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                currentIndex = Math.min(currentIndex + 1, items.length - 1);
                items[currentIndex]?.focus();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                currentIndex = Math.max(currentIndex - 1, 0);
                items[currentIndex]?.focus();
                break;
                
            case 'Home':
                e.preventDefault();
                currentIndex = 0;
                items[0]?.focus();
                break;
                
            case 'End':
                e.preventDefault();
                currentIndex = items.length - 1;
                items[currentIndex]?.focus();
                break;
                
            case 'Escape':
                e.preventDefault();
                bootstrap.Dropdown.getOrCreateInstance(trigger).hide();
                trigger.focus();
                break;
                
            case 'Tab':
                // Allow Tab to close dropdown
                bootstrap.Dropdown.getOrCreateInstance(trigger).hide();
                break;
        }
    });
}
```

---

## Button/Interactive Element Patterns

### Custom Button with Keyboard Support

```html
<!-- If you must use a div as button (use real button when possible) -->
<div role="button"
     tabindex="0"
     class="custom-button"
     aria-label="Agregar sesión"
     onclick="handleClick()"
     onkeydown="handleKeydown(event)">
    <i class="bi bi-plus" aria-hidden="true"></i>
    Agregar
</div>
```

```javascript
function handleKeydown(event) {
    // Activate on Enter or Space
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        handleClick();
    }
}
```

### Toggle Button Pattern

```html
<button type="button"
        class="btn toggle-payment-btn"
        aria-pressed="false"
        onclick="togglePayment(this)">
    Pendiente
</button>
```

```javascript
function togglePayment(button) {
    const isPressed = button.getAttribute('aria-pressed') === 'true';
    button.setAttribute('aria-pressed', !isPressed);
    button.textContent = isPressed ? 'Pendiente' : 'Pagado';
    button.classList.toggle('btn-warning', isPressed);
    button.classList.toggle('btn-success', !isPressed);
}
```

---

## Testing Keyboard Navigation

### Manual Testing Checklist

1. **Tab Navigation**
   - [ ] All interactive elements receive focus in logical order
   - [ ] Focus is visible on all elements
   - [ ] No elements trap focus unexpectedly
   - [ ] Hidden elements don't receive focus

2. **Activation**
   - [ ] All buttons activate with Enter and Space
   - [ ] All links activate with Enter
   - [ ] Form submissions work with Enter

3. **Modals**
   - [ ] Focus moves into modal on open
   - [ ] Focus is trapped within modal
   - [ ] Escape closes modal
   - [ ] Focus returns to trigger after close

4. **Carousels**
   - [ ] Arrow keys navigate slides
   - [ ] Focus remains on carousel during navigation
   - [ ] Slide changes are announced

5. **Dropdowns**
   - [ ] Opens with Enter/Space/Arrow Down
   - [ ] Arrow keys navigate items
   - [ ] Escape closes and returns focus
   - [ ] Selection works with Enter

### Automated Testing

```javascript
// Test all interactive elements are keyboard accessible
function testKeyboardAccessibility() {
    const interactive = document.querySelectorAll(
        'button, a[href], input, select, textarea, [tabindex="0"]'
    );
    
    interactive.forEach(el => {
        // Check it can receive focus
        el.focus();
        if (document.activeElement !== el) {
            console.error('Cannot focus:', el);
        }
        
        // Check it has visible focus indicator
        const outline = getComputedStyle(el).outline;
        const boxShadow = getComputedStyle(el).boxShadow;
        if (outline === 'none' && boxShadow === 'none') {
            console.warn('No visible focus indicator:', el);
        }
    });
}
```

---

## Common Issues and Fixes

### Issue: Hidden Elements Receiving Focus

```javascript
// Fix: Remove from tab order when hidden
function hideElement(element) {
    element.hidden = true;
    element.setAttribute('tabindex', '-1');
    element.setAttribute('aria-hidden', 'true');
}

function showElement(element) {
    element.hidden = false;
    element.removeAttribute('tabindex');
    element.removeAttribute('aria-hidden');
}
```

### Issue: Focus Lost After DOM Update

```javascript
// Fix: Restore focus after dynamic content update
function updateContent(container, newContent) {
    const previouslyFocused = document.activeElement;
    const focusedId = previouslyFocused?.id;
    
    container.innerHTML = newContent;
    
    // Try to restore focus
    if (focusedId) {
        const newElement = document.getElementById(focusedId);
        newElement?.focus();
    } else {
        // Focus container or first focusable element
        const firstFocusable = container.querySelector(
            'button, a[href], input, [tabindex="0"]'
        );
        firstFocusable?.focus() || container.focus();
    }
}
```

### Issue: Carousel Navigation Not Keyboard Accessible

```javascript
// Fix: Add roving tabindex pattern
function setupRovingTabindex(carousel) {
    const indicators = carousel.querySelectorAll('.carousel-indicators button');
    
    indicators.forEach((indicator, index) => {
        indicator.setAttribute('tabindex', index === 0 ? '0' : '-1');
        
        indicator.addEventListener('keydown', (e) => {
            let newIndex;
            
            if (e.key === 'ArrowRight') {
                newIndex = (index + 1) % indicators.length;
            } else if (e.key === 'ArrowLeft') {
                newIndex = (index - 1 + indicators.length) % indicators.length;
            } else {
                return;
            }
            
            e.preventDefault();
            indicators.forEach((ind, i) => {
                ind.setAttribute('tabindex', i === newIndex ? '0' : '-1');
            });
            indicators[newIndex].focus();
            indicators[newIndex].click();
        });
    });
}
```

---

## Resources

- [WebAIM Keyboard Accessibility](https://webaim.org/techniques/keyboard/)
- [MDN Keyboard Navigation](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Keyboard-navigable_JavaScript_widgets)
- [ARIA Keyboard Patterns](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)

---

*Last Updated: January 15, 2026*
