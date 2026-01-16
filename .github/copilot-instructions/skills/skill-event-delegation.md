# Skill: Event Delegation

## Overview

Event delegation is a pattern that leverages event bubbling to handle events efficiently. Instead of attaching listeners to individual elements, you attach a single listener to a parent element that handles events from its descendants. This skill covers event propagation, delegation patterns, and best practices for the Therapy Session Management Application.

---

## Event Propagation

### Three Phases

```
                    ┌─────────────────────────────┐
                    │         document            │
                    └─────────────────────────────┘
                              │    ▲
         Capturing Phase (1)  │    │  Bubbling Phase (3)
                              ▼    │
                    ┌─────────────────────────────┐
                    │          <html>             │
                    └─────────────────────────────┘
                              │    ▲
                              ▼    │
                    ┌─────────────────────────────┐
                    │          <body>             │
                    └─────────────────────────────┘
                              │    ▲
                              ▼    │
                    ┌─────────────────────────────┐
                    │       <div.container>       │
                    └─────────────────────────────┘
                              │    ▲
                              ▼    │
                    ┌─────────────────────────────┐
                    │     <button> (target)       │  ← Target Phase (2)
                    └─────────────────────────────┘
```

| Phase | Description | Default Listener |
|-------|-------------|------------------|
| Capturing | Event travels DOWN from document to target | No |
| Target | Event reaches the clicked element | Yes |
| Bubbling | Event travels UP from target to document | Yes |

### Event Properties

```javascript
element.addEventListener('click', (event) => {
    // The element that triggered the event
    event.target;
    
    // The element the listener is attached to
    event.currentTarget;
    
    // Current phase (1=capturing, 2=target, 3=bubbling)
    event.eventPhase;
    
    // Stop propagation to other elements
    event.stopPropagation();
    
    // Stop propagation and other listeners on same element
    event.stopImmediatePropagation();
    
    // Prevent default browser behavior
    event.preventDefault();
});
```

---

## Why Use Event Delegation?

### Problem: Many Individual Listeners

```javascript
// ❌ BAD: One listener per button
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', handleDelete);
});

// Issues:
// 1. Memory overhead - each button has its own listener
// 2. Dynamic elements - new buttons need manual attachment
// 3. Cleanup complexity - must remove each listener
```

### Solution: Single Delegated Listener

```javascript
// ✅ GOOD: One listener on parent
document.querySelector('.patient-list').addEventListener('click', (event) => {
    const deleteBtn = event.target.closest('.delete-btn');
    if (deleteBtn) {
        handleDelete(deleteBtn);
    }
});

// Benefits:
// 1. Single listener - minimal memory
// 2. Dynamic elements - automatically handled
// 3. Easy cleanup - one listener to remove
```

### Performance Comparison

| Approach | 100 Buttons | 1000 Buttons |
|----------|-------------|--------------|
| Individual listeners | 100 listeners | 1000 listeners |
| Delegated listener | 1 listener | 1 listener |
| Memory usage | High | Very High |
| Setup time | O(n) | O(n) |
| Delegation setup | O(1) | O(1) |

---

## Core Delegation Pattern

### Basic Structure

```javascript
/**
 * Handle delegated clicks on a container
 * @param {Event} event - Click event
 */
function handleContainerClick(event) {
    // Find the relevant element (may be nested inside the target)
    const actionButton = event.target.closest('[data-action]');
    
    // Exit if click wasn't on an action element
    if (!actionButton) return;
    
    // Get action type from data attribute
    const action = actionButton.dataset.action;
    
    // Route to appropriate handler
    switch (action) {
        case 'edit':
            handleEdit(actionButton);
            break;
        case 'delete':
            handleDelete(actionButton);
            break;
        case 'toggle-payment':
            handleTogglePayment(actionButton);
            break;
    }
}

// Attach single listener to container
document.querySelector('.patient-list').addEventListener('click', handleContainerClick);
```

### Using closest() Method

```javascript
// event.target is the exact element clicked (could be icon inside button)
// closest() traverses up to find matching ancestor

// HTML:
// <button class="btn-delete" data-patient-id="123">
//     <i class="bi bi-trash"></i>  ← User clicks here
//     <span>Eliminar</span>
// </button>

element.addEventListener('click', (event) => {
    // event.target = <i class="bi bi-trash">
    
    // ❌ This would fail:
    if (event.target.classList.contains('btn-delete')) { }
    
    // ✅ This works - finds the button ancestor:
    const button = event.target.closest('.btn-delete');
    if (button) {
        const patientId = button.dataset.patientId;
    }
});
```

---

## Project Implementation

### HTML Structure with Data Attributes

```html
<!-- Patient card with action buttons -->
<article class="patient-card" data-patient-id="123">
    <header class="patient-card__header">
        <h3 class="patient-card__name">Juan Pérez</h3>
        <div class="patient-card__actions">
            <button 
                class="btn btn--icon" 
                data-action="edit-patient"
                data-patient-id="123"
                aria-label="Editar paciente">
                <i class="bi bi-pencil"></i>
            </button>
            <button 
                class="btn btn--icon btn--danger" 
                data-action="delete-patient"
                data-patient-id="123"
                aria-label="Eliminar paciente">
                <i class="bi bi-trash"></i>
            </button>
        </div>
    </header>
    
    <!-- Session cards -->
    <div class="patient-card__sessions">
        <article class="session-card" data-session-id="456">
            <span class="session-card__date">Lunes 15/01/2026</span>
            <span class="session-card__price">$150.00</span>
            <div class="session-card__actions">
                <button 
                    class="btn btn--sm" 
                    data-action="toggle-payment"
                    data-session-id="456">
                    Marcar Pagado
                </button>
                <button 
                    class="btn btn--sm btn--icon" 
                    data-action="edit-session"
                    data-session-id="456">
                    <i class="bi bi-pencil"></i>
                </button>
                <button 
                    class="btn btn--sm btn--icon btn--danger" 
                    data-action="delete-session"
                    data-session-id="456">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </article>
    </div>
</article>
```

### Centralized Event Handler

```javascript
/**
 * Action handlers registry
 * @type {Object.<string, function(HTMLElement): void>}
 */
const actionHandlers = {
    'edit-patient': handleEditPatient,
    'delete-patient': handleDeletePatient,
    'toggle-payment': handleTogglePayment,
    'edit-session': handleEditSession,
    'delete-session': handleDeleteSession,
    'add-session': handleAddSession,
    'apply-filter': handleApplyFilter,
};

/**
 * Initialize event delegation on the main container
 */
function initEventDelegation() {
    const mainContent = document.querySelector('main');
    
    if (mainContent) {
        mainContent.addEventListener('click', handleDelegatedClick);
        mainContent.addEventListener('submit', handleDelegatedSubmit);
        mainContent.addEventListener('change', handleDelegatedChange);
    }
}

/**
 * Handle all delegated click events
 * @param {MouseEvent} event
 */
function handleDelegatedClick(event) {
    const actionElement = event.target.closest('[data-action]');
    
    if (!actionElement) return;
    
    const action = actionElement.dataset.action;
    const handler = actionHandlers[action];
    
    if (handler) {
        event.preventDefault();
        handler(actionElement);
    } else {
        console.warn(`No handler for action: ${action}`);
    }
}

/**
 * Handle all delegated form submissions
 * @param {SubmitEvent} event
 */
function handleDelegatedSubmit(event) {
    const form = event.target.closest('form[data-form]');
    
    if (!form) return;
    
    event.preventDefault();
    
    const formType = form.dataset.form;
    
    switch (formType) {
        case 'edit-patient':
            submitPatientForm(form);
            break;
        case 'edit-session':
            submitSessionForm(form);
            break;
        case 'filter':
            submitFilterForm(form);
            break;
    }
}

/**
 * Handle all delegated change events
 * @param {Event} event
 */
function handleDelegatedChange(event) {
    const select = event.target.closest('select[data-filter]');
    
    if (select) {
        applyFilter(select.value);
    }
}
```

### Individual Action Handlers

```javascript
/**
 * Handle edit patient action
 * @param {HTMLElement} button - The clicked button
 */
async function handleEditPatient(button) {
    const patientId = parseInt(button.dataset.patientId, 10);
    
    try {
        // Fetch patient data
        const patient = await getPatient(patientId);
        
        // Open edit modal with data
        openEditPatientModal(patient);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Handle delete patient action
 * @param {HTMLElement} button - The clicked button
 */
function handleDeletePatient(button) {
    const patientId = parseInt(button.dataset.patientId, 10);
    const patientName = button.closest('.patient-card').querySelector('.patient-card__name').textContent;
    
    // Open confirmation modal
    openConfirmModal({
        title: 'Eliminar Paciente',
        message: `¿Está seguro de eliminar a ${patientName}?`,
        confirmLabel: 'Eliminar',
        confirmClass: 'btn--danger',
        onConfirm: async () => {
            try {
                await deletePatient(patientId);
                removePatientFromUI(patientId);
                showToast('Paciente eliminado', 'success');
            } catch (error) {
                showToast(error.message, 'error');
            }
        }
    });
}

/**
 * Handle toggle payment action
 * @param {HTMLElement} button - The clicked button
 */
async function handleTogglePayment(button) {
    const sessionId = parseInt(button.dataset.sessionId, 10);
    
    // Disable button during request
    button.disabled = true;
    
    try {
        const session = await toggleSessionPayment(sessionId);
        updateSessionUI(session);
        showToast(
            session.pending ? 'Marcado como pendiente' : 'Marcado como pagado',
            'success'
        );
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        button.disabled = false;
    }
}
```

---

## Advanced Patterns

### Event Delegation with Keyboard Support

```javascript
/**
 * Handle both click and keyboard activation
 * @param {Event} event
 */
function handleActivation(event) {
    // Handle click
    if (event.type === 'click') {
        handleAction(event);
        return;
    }
    
    // Handle Enter or Space for keyboard users
    if (event.type === 'keydown') {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            handleAction(event);
        }
    }
}

// Attach both listeners
container.addEventListener('click', handleActivation);
container.addEventListener('keydown', handleActivation);
```

### Delegation with Capturing Phase

```javascript
// Listen during capturing phase (before target receives event)
// Useful for intercepting events before they reach target

document.addEventListener('focus', (event) => {
    const input = event.target.closest('input, textarea');
    if (input) {
        input.classList.add('input--focused');
    }
}, true);  // true = capturing phase

document.addEventListener('blur', (event) => {
    const input = event.target.closest('input, textarea');
    if (input) {
        input.classList.remove('input--focused');
    }
}, true);  // focus/blur don't bubble, must use capturing
```

### Delegation with Custom Events

```javascript
/**
 * Dispatch custom event for cross-component communication
 * @param {string} eventName
 * @param {object} detail
 */
function emitEvent(eventName, detail) {
    document.dispatchEvent(new CustomEvent(eventName, {
        bubbles: true,
        detail
    }));
}

// When a session is updated
async function handleTogglePayment(button) {
    const session = await toggleSessionPayment(sessionId);
    
    // Emit event for other components to react
    emitEvent('session:updated', {
        sessionId: session.id,
        action: 'toggle-payment',
        session
    });
}

// Listen for session updates anywhere
document.addEventListener('session:updated', (event) => {
    const { sessionId, action, session } = event.detail;
    
    // Update dashboard totals
    updateDashboardTotals();
    
    // Update filter counts
    updateFilterCounts();
});
```

### Delegation with Debouncing

```javascript
/**
 * Create a debounced event handler
 * @param {Function} handler
 * @param {number} delay
 * @returns {Function}
 */
function debounce(handler, delay = 300) {
    let timeoutId;
    return function(event) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => handler.call(this, event), delay);
    };
}

// Debounced search input handler
const handleSearchInput = debounce((event) => {
    const searchTerm = event.target.value;
    filterPatients(searchTerm);
}, 300);

document.addEventListener('input', (event) => {
    if (event.target.matches('[data-search]')) {
        handleSearchInput(event);
    }
});
```

---

## Non-Bubbling Events

### Events That Don't Bubble

| Event | Description | Solution |
|-------|-------------|----------|
| `focus` | Element receives focus | Use `focusin` (bubbles) |
| `blur` | Element loses focus | Use `focusout` (bubbles) |
| `mouseenter` | Mouse enters element | Use `mouseover` (bubbles) |
| `mouseleave` | Mouse leaves element | Use `mouseout` (bubbles) |
| `load` | Resource loaded | Use capturing phase |
| `scroll` | Element scrolled | Attach to specific element |

### Using Bubbling Alternatives

```javascript
// ❌ focus doesn't bubble
container.addEventListener('focus', handler);  // Won't catch child focus

// ✅ focusin bubbles
container.addEventListener('focusin', (event) => {
    const input = event.target.closest('input');
    if (input) {
        showInputHelp(input);
    }
});

// ✅ focusout bubbles
container.addEventListener('focusout', (event) => {
    const input = event.target.closest('input');
    if (input) {
        validateInput(input);
    }
});
```

---

## Cleanup and Memory Management

### Removing Delegated Listeners

```javascript
// Store reference for cleanup
const clickHandler = (event) => {
    // Handle click
};

// Attach
container.addEventListener('click', clickHandler);

// Cleanup (on page unload or component destroy)
container.removeEventListener('click', clickHandler);
```

### Using AbortController

```javascript
// Modern cleanup pattern
const controller = new AbortController();

// Attach with signal
container.addEventListener('click', handleClick, { signal: controller.signal });
container.addEventListener('keydown', handleKeydown, { signal: controller.signal });

// Cleanup all at once
function cleanup() {
    controller.abort();  // Removes all listeners attached with this signal
}
```

### Cleanup on Dynamic Content

```javascript
// When removing elements, ensure no orphaned references

function removePatientCard(patientId) {
    const card = document.querySelector(`[data-patient-id="${patientId}"]`);
    
    if (card) {
        // With delegation, no need to remove individual listeners
        // Just remove the element
        card.remove();
    }
}
```

---

## Common Patterns

### Action Button Pattern

```html
<!-- HTML -->
<button 
    class="btn"
    data-action="save"
    data-entity="patient"
    data-id="123">
    Guardar
</button>
```

```javascript
// JavaScript
document.addEventListener('click', (event) => {
    const btn = event.target.closest('[data-action]');
    if (!btn) return;
    
    const { action, entity, id } = btn.dataset;
    
    // Dispatch to handler
    const handlerKey = `${action}-${entity}`;  // "save-patient"
    const handler = handlers[handlerKey];
    
    if (handler) {
        handler(id, btn);
    }
});
```

### Toggle Pattern

```html
<!-- HTML -->
<button 
    class="toggle"
    data-action="toggle"
    data-target="#menu"
    aria-expanded="false">
    Menu
</button>
<nav id="menu" hidden>...</nav>
```

```javascript
// JavaScript
document.addEventListener('click', (event) => {
    const toggle = event.target.closest('[data-action="toggle"]');
    if (!toggle) return;
    
    const targetId = toggle.dataset.target;
    const target = document.querySelector(targetId);
    
    if (target) {
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', !isExpanded);
        target.hidden = isExpanded;
    }
});
```

### Confirmation Pattern

```javascript
// Confirm before destructive actions
document.addEventListener('click', async (event) => {
    const deleteBtn = event.target.closest('[data-action="delete"]');
    if (!deleteBtn) return;
    
    // Check for confirmation requirement
    if (deleteBtn.dataset.confirm) {
        const confirmed = await showConfirmDialog(deleteBtn.dataset.confirm);
        if (!confirmed) return;
    }
    
    // Proceed with delete
    performDelete(deleteBtn);
});
```

---

## Testing Event Delegation

### Unit Testing Handlers

```javascript
// Test handler functions directly
describe('handleTogglePayment', () => {
    test('disables button during request', async () => {
        const button = document.createElement('button');
        button.dataset.sessionId = '123';
        
        // Mock API
        toggleSessionPayment.mockResolvedValue({ id: 123, pending: false });
        
        const promise = handleTogglePayment(button);
        
        expect(button.disabled).toBe(true);
        
        await promise;
        
        expect(button.disabled).toBe(false);
    });
});
```

### Integration Testing

```javascript
// Test the delegation setup
describe('Event Delegation', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <main>
                <button data-action="edit-patient" data-patient-id="1">Edit</button>
            </main>
        `;
        initEventDelegation();
    });
    
    test('clicking edit button calls handler', () => {
        const handler = jest.fn();
        actionHandlers['edit-patient'] = handler;
        
        document.querySelector('[data-action="edit-patient"]').click();
        
        expect(handler).toHaveBeenCalled();
    });
});
```

---

## Checklist for Event Delegation

### Setup
- [ ] Single listener on stable parent element
- [ ] Using `closest()` to find action elements
- [ ] Data attributes for action identification
- [ ] Handler registry for maintainability

### Accessibility
- [ ] Keyboard support (Enter/Space)
- [ ] Focus management after actions
- [ ] ARIA attributes updated

### Performance
- [ ] No listeners on individual items
- [ ] Debouncing for frequent events
- [ ] Early return if target not matched

### Cleanup
- [ ] Listeners removed on teardown
- [ ] No memory leaks from closures
- [ ] AbortController for multiple listeners

### Testing
- [ ] Handlers testable in isolation
- [ ] Integration tests for delegation
- [ ] Edge cases covered (nested elements)

---

## Related Skills

- [skill-javascript-modules.md](./skill-javascript-modules.md) - Organizing handlers
- [skill-keyboard-navigation.md](./skill-keyboard-navigation.md) - Keyboard accessibility
- [skill-error-handling.md](./skill-error-handling.md) - Error handling in handlers

---

*Last Updated: January 15, 2026*
