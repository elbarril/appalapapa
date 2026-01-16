# Skill: BEM Methodology

## Overview

BEM (Block Element Modifier) is a naming convention for CSS classes that creates clear, strict relationships between HTML and CSS. It improves code readability, reusability, and maintainability.

---

## BEM Naming Structure

### Pattern

```
.block__element--modifier
```

| Part | Description | Example |
|------|-------------|---------|
| **Block** | Standalone component | `.card`, `.nav`, `.btn` |
| **Element** | Part of a block (uses `__`) | `.card__header`, `.nav__item` |
| **Modifier** | Variant or state (uses `--`) | `.card--featured`, `.btn--primary` |

---

## Blocks

A block is a standalone, reusable component.

### Naming Rules
- Use lowercase letters
- Use hyphens for multi-word names
- Name describes purpose, not appearance

```css
/* ✅ DO: Descriptive, purpose-based names */
.card { }
.nav-menu { }
.search-form { }
.patient-list { }

/* ❌ DON'T: Appearance-based names */
.big-blue-box { }
.left-sidebar { }
```

### Block Examples for This Project

```css
/* Patient management */
.patient-card { }
.patient-list { }
.patient-form { }

/* Session management */
.session-card { }
.session-carousel { }
.session-form { }

/* Common components */
.nav-header { }
.modal-dialog { }
.toast-notification { }
.filter-bar { }
```

---

## Elements

An element is a part of a block that has no standalone meaning.

### Naming Rules
- Always prefixed with block name
- Separated by double underscore (`__`)
- Cannot exist outside its block

```css
/* ✅ DO: Elements belong to blocks */
.card__header { }
.card__body { }
.card__footer { }
.card__title { }
.card__actions { }

/* ❌ DON'T: Nest elements (no .block__element__subelement) */
.card__header__title { }  /* Wrong! */

/* ✅ DO: Flatten nested elements */
.card__header { }
.card__header-title { }   /* Use hyphen for sub-parts */
```

### Element Examples for This Project

```css
/* Patient card elements */
.patient-card { }
.patient-card__header { }
.patient-card__name { }
.patient-card__notes { }
.patient-card__sessions { }
.patient-card__actions { }

/* Session card elements */
.session-card { }
.session-card__date { }
.session-card__price { }
.session-card__status { }
.session-card__buttons { }

/* Navigation elements */
.nav-header { }
.nav-header__brand { }
.nav-header__menu { }
.nav-header__item { }
.nav-header__link { }
.nav-header__toggle { }

/* Form elements */
.session-form { }
.session-form__group { }
.session-form__label { }
.session-form__input { }
.session-form__error { }
.session-form__submit { }
```

---

## Modifiers

A modifier changes appearance, behavior, or state of a block/element.

### Naming Rules
- Separated by double hyphen (`--`)
- Can apply to blocks or elements
- Describes what it changes, not how

```css
/* Block modifiers */
.card--featured { }
.card--compact { }
.card--pending { }
.card--paid { }

/* Element modifiers */
.card__title--large { }
.card__status--warning { }
.nav-header__link--active { }
```

### Modifier Types

#### Boolean Modifiers (presence = true)

```css
/* The modifier is either present or not */
.btn--disabled { }
.card--loading { }
.modal--open { }
.nav-header__item--active { }
```

#### Key-Value Modifiers

```css
/* Modifier has a specific value */
.btn--size-large { }
.btn--size-small { }
.card--theme-dark { }
.card--theme-light { }
.alert--type-success { }
.alert--type-error { }
```

### Modifier Examples for This Project

```css
/* Payment status modifiers */
.session-card--pending { }
.session-card--paid { }
.badge--pending { }
.badge--paid { }

/* Size modifiers */
.btn--full-width { }
.card--compact { }
.modal--large { }

/* State modifiers */
.btn--loading { }
.btn--disabled { }
.form__input--invalid { }
.form__input--valid { }
.nav-header__link--active { }

/* Theme modifiers */
.card--theme-dark { }
.toast--type-success { }
.toast--type-error { }
.toast--type-warning { }
```

---

## BEM with HTML

### Complete Example

```html
<!-- Block: patient-card -->
<article class="patient-card patient-card--has-sessions">
    
    <!-- Element: header -->
    <header class="patient-card__header">
        <h3 class="patient-card__name">Juan Pérez</h3>
        <button class="patient-card__action patient-card__action--edit">
            <i class="bi bi-pencil"></i>
        </button>
    </header>
    
    <!-- Element: body -->
    <div class="patient-card__body">
        <p class="patient-card__notes">Notas del paciente...</p>
    </div>
    
    <!-- Element: sessions (nested block) -->
    <div class="patient-card__sessions">
        <!-- session-card is a separate block -->
        <article class="session-card session-card--pending">
            <span class="session-card__date">Lunes 15/01/2026</span>
            <span class="session-card__price">$150.00</span>
            <span class="session-card__status badge badge--pending">PENDIENTE</span>
        </article>
    </div>
    
    <!-- Element: footer -->
    <footer class="patient-card__footer">
        <button class="btn btn--primary btn--full-width">
            Nueva Sesión
        </button>
    </footer>
    
</article>
```

### CSS for Above Example

```css
/* Block */
.patient-card {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

/* Block modifier */
.patient-card--has-sessions {
    border-left: 3px solid var(--color-primary);
}

/* Elements */
.patient-card__header {
    display: flex;
    justify-content: space-between;
    padding: var(--space-4);
    border-bottom: 1px solid var(--card-border);
}

.patient-card__name {
    margin: 0;
    font-size: var(--text-lg);
    font-weight: var(--font-weight-semibold);
}

.patient-card__action {
    background: transparent;
    border: none;
    cursor: pointer;
}

/* Element modifier */
.patient-card__action--edit {
    color: var(--color-primary);
}

.patient-card__action--delete {
    color: var(--color-danger);
}

.patient-card__body {
    padding: var(--space-4);
}

.patient-card__notes {
    color: var(--text-secondary);
    font-size: var(--text-sm);
}

.patient-card__sessions {
    padding: var(--space-4);
    background: var(--bg-tertiary);
}

.patient-card__footer {
    padding: var(--space-4);
    border-top: 1px solid var(--card-border);
}
```

---

## Handling Component Nesting

### Nested Blocks (Not Nested Elements)

When a component contains another component, treat them as separate blocks:

```html
<!-- ✅ DO: Separate blocks -->
<article class="patient-card">
    <div class="patient-card__sessions">
        <!-- session-card is its own block -->
        <article class="session-card">
            <span class="session-card__date">...</span>
        </article>
    </div>
</article>
```

```css
/* Each block is independent */
.patient-card { }
.patient-card__sessions { }

.session-card { }
.session-card__date { }
```

```html
<!-- ❌ DON'T: Deep element nesting -->
<article class="patient-card">
    <div class="patient-card__sessions">
        <article class="patient-card__sessions__card">  <!-- Wrong! -->
            <span class="patient-card__sessions__card__date">...</span>
        </article>
    </div>
</article>
```

---

## BEM with JavaScript

### Using Data Attributes for JS Hooks

Separate styling classes from JavaScript hooks:

```html
<!-- ✅ DO: Use data attributes for JS -->
<button class="btn btn--primary" data-action="toggle-payment" data-session-id="123">
    Marcar Pagado
</button>
```

```javascript
// JavaScript uses data attributes
document.querySelector('[data-action="toggle-payment"]');
document.querySelectorAll('[data-session-id]');
```

```html
<!-- ❌ DON'T: Use BEM classes for JS hooks -->
<button class="btn btn--primary js-toggle-payment">
    Marcar Pagado
</button>
```

### State Classes with BEM

```html
<!-- State applied via JavaScript -->
<button class="btn btn--loading" disabled>
    <span class="btn__spinner"></span>
    Guardando...
</button>

<div class="modal modal--open">
    ...
</div>

<input class="form__input form__input--invalid" />
```

```javascript
// Adding state modifiers
element.classList.add('btn--loading');
element.classList.remove('btn--loading');

// Checking state
if (element.classList.contains('modal--open')) { }
```

---

## BEM with Bootstrap

### Extending Bootstrap Components

```html
<!-- Bootstrap base + BEM customization -->
<div class="card patient-card patient-card--pending">
    <div class="card-header patient-card__header">
        <h5 class="card-title patient-card__title">Juan Pérez</h5>
    </div>
    <div class="card-body patient-card__body">
        ...
    </div>
</div>
```

```css
/* BEM classes extend Bootstrap */
.patient-card {
    /* Custom styles on top of Bootstrap .card */
}

.patient-card--pending {
    border-left-color: var(--color-warning);
}

.patient-card__header {
    /* Custom header styles */
}
```

---

## Common BEM Patterns

### Button Component

```css
/* Block */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-2) var(--space-4);
    border: 1px solid transparent;
    border-radius: var(--radius-md);
    font-weight: var(--font-weight-medium);
    cursor: pointer;
    transition: var(--transition-fast);
}

/* Elements */
.btn__icon {
    margin-right: var(--space-2);
}

.btn__text { }

.btn__spinner {
    display: none;
}

/* Modifiers - Variants */
.btn--primary {
    background: var(--color-primary);
    color: white;
}

.btn--secondary {
    background: transparent;
    border-color: var(--color-primary);
    color: var(--color-primary);
}

.btn--danger {
    background: var(--color-danger);
    color: white;
}

/* Modifiers - Sizes */
.btn--small {
    padding: var(--space-1) var(--space-2);
    font-size: var(--text-sm);
}

.btn--large {
    padding: var(--space-3) var(--space-6);
    font-size: var(--text-lg);
}

.btn--full-width {
    width: 100%;
}

/* Modifiers - States */
.btn--loading .btn__spinner {
    display: inline-block;
}

.btn--loading .btn__text {
    opacity: 0.7;
}

.btn--disabled,
.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

### Form Component

```css
/* Block */
.form { }

/* Elements */
.form__group {
    margin-bottom: var(--space-4);
}

.form__label {
    display: block;
    margin-bottom: var(--space-2);
    font-weight: var(--font-weight-medium);
}

.form__input {
    width: 100%;
    padding: var(--space-2) var(--space-3);
    border: 1px solid var(--input-border);
    border-radius: var(--radius-md);
}

.form__help {
    margin-top: var(--space-1);
    font-size: var(--text-sm);
    color: var(--text-muted);
}

.form__error {
    margin-top: var(--space-1);
    font-size: var(--text-sm);
    color: var(--color-danger);
}

.form__actions {
    display: flex;
    gap: var(--space-3);
    margin-top: var(--space-5);
}

/* Element modifiers */
.form__input--invalid {
    border-color: var(--color-danger);
}

.form__input--valid {
    border-color: var(--color-success);
}
```

---

## Migration from Current CSS

### Current Pattern → BEM Pattern

| Current Class | BEM Equivalent |
|---------------|----------------|
| `.card-header` | `.patient-card__header` |
| `.session-actions` | `.session-card__actions` |
| `.btn-edit-person` | `.btn--edit` or `[data-action="edit"]` |
| `.pending-badge` | `.badge--pending` |
| `.paid-session` | `.session-card--paid` |
| `.carousel-item.active` | `.carousel__item--active` |

### Gradual Migration Strategy

1. **New components**: Use BEM from start
2. **Modified components**: Convert to BEM when editing
3. **Stable components**: Convert during dedicated refactor phase
4. **Keep both**: During transition, both naming conventions may coexist

---

## BEM Checklist

### Naming
- [ ] Block names are nouns (`.card`, `.form`, `.nav`)
- [ ] Element names describe what it is (`.card__title`, not `.card__bold-text`)
- [ ] Modifier names describe the change (`.btn--large`, not `.btn--123`)
- [ ] No more than 2 words per part (`session-card`, not `therapy-session-patient-card`)

### Structure
- [ ] Elements always include block name (`.card__header`, not `.__header`)
- [ ] No nested elements (`.card__header-title`, not `.card__header__title`)
- [ ] Modifiers include block/element name (`.card--featured`, not `.--featured`)

### Best Practices
- [ ] One block per file in modular CSS
- [ ] Blocks are independent and reusable
- [ ] JavaScript uses data attributes, not BEM classes
- [ ] States are modifiers (`.btn--loading`, `.modal--open`)

---

## Related Skills

- [skill-css-architecture.md](./skill-css-architecture.md) - File organization
- [skill-css-custom-properties.md](./skill-css-custom-properties.md) - CSS variables
- [skill-component-design.md](./skill-component-design.md) - Component patterns

---

*Last Updated: January 15, 2026*
