# Skill: Component Design Patterns

> **Scope:** Reusable UI component patterns, component API design, and composition strategies for Flask/Jinja2 applications.

---

## 1. Component Design Principles

### What Makes a Good Component

| Principle | Description | Example |
|-----------|-------------|---------|
| **Single Responsibility** | One clear purpose | Card displays one entity |
| **Composable** | Works with other components | Card accepts any content |
| **Configurable** | Behavior controlled via props | `show_actions=true` |
| **Self-Contained** | Minimal external dependencies | Includes own styles |
| **Accessible** | WCAG compliant by default | ARIA labels built-in |
| **Documented** | Clear usage instructions | Parameter comments |

### Component Categories

```
components/
├── primitives/          # Basic building blocks
│   ├── button.html      # Buttons, links
│   ├── icon.html        # Icon wrapper
│   ├── badge.html       # Status badges
│   └── spinner.html     # Loading indicator
├── forms/               # Form-related
│   ├── field.html       # Form field wrapper
│   ├── input.html       # Input variations
│   ├── select.html      # Dropdowns
│   └── checkbox.html    # Checkboxes/radios
├── feedback/            # User feedback
│   ├── alert.html       # Alert messages
│   ├── toast.html       # Toast notifications
│   └── modal.html       # Modal dialogs
├── layout/              # Structural
│   ├── card.html        # Card container
│   ├── section.html     # Page section
│   └── grid.html        # Grid layouts
└── composite/           # Complex combinations
    ├── patient_card.html
    ├── session_card.html
    └── data_table.html
```

---

## 2. Component API Design

### Parameter Conventions

```html
{#
    Component: Button
    
    Parameters:
        text (str, required): Button label text
        type (str): 'button' | 'submit' | 'reset'. Default: 'button'
        variant (str): 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'link'. Default: 'primary'
        size (str): 'sm' | 'md' | 'lg'. Default: 'md'
        icon (str): Bootstrap icon name (without 'bi-' prefix). Default: none
        icon_position (str): 'start' | 'end'. Default: 'start'
        disabled (bool): Disable the button. Default: false
        loading (bool): Show loading spinner. Default: false
        full_width (bool): Make button full width. Default: false
        attrs (dict): Additional HTML attributes. Default: {}
        
    Usage:
        {% from 'components/button.html' import button %}
        {{ button(text='Guardar', variant='primary', icon='check') }}
        {{ button(text='Eliminar', variant='danger', icon='trash', disabled=true) }}
#}

{% macro button(
    text,
    type='button',
    variant='primary',
    size='md',
    icon=none,
    icon_position='start',
    disabled=false,
    loading=false,
    full_width=false,
    attrs={}
) %}
{% set size_class = {'sm': 'btn-sm', 'md': '', 'lg': 'btn-lg'}[size] %}
{% set width_class = 'w-100' if full_width else '' %}

<button type="{{ type }}"
        class="btn btn-{{ variant }} {{ size_class }} {{ width_class }}"
        {% if disabled or loading %}disabled aria-disabled="true"{% endif %}
        {% for key, value in attrs.items() %}{{ key }}="{{ value }}"{% endfor %}>
    
    {% if loading %}
    <span class="spinner-border spinner-border-sm me-1" 
          role="status" 
          aria-hidden="true"></span>
    {% elif icon and icon_position == 'start' %}
    <i class="bi bi-{{ icon }} me-1" aria-hidden="true"></i>
    {% endif %}
    
    <span>{{ text }}</span>
    
    {% if icon and icon_position == 'end' and not loading %}
    <i class="bi bi-{{ icon }} ms-1" aria-hidden="true"></i>
    {% endif %}
</button>
{% endmacro %}
```

### Naming Conventions

| Type | Convention | Examples |
|------|------------|----------|
| **Boolean props** | `is_`, `has_`, `show_`, `enable_` | `is_active`, `show_icon`, `enable_edit` |
| **Handler props** | `on_` prefix (JS callbacks) | `on_click`, `on_submit` |
| **Content slots** | Descriptive nouns | `header`, `footer`, `actions` |
| **Style variants** | Standard names | `variant`, `size`, `color` |
| **ID references** | `_id` suffix | `label_id`, `error_id` |

### Required vs. Optional Parameters

```html
{# 
    Required parameters: No default value
    Optional parameters: Has default value
#}

{% macro form_field(
    name,                    {# Required: field name #}
    label,                   {# Required: field label #}
    type='text',            {# Optional: input type #}
    value='',               {# Optional: current value #}
    placeholder='',         {# Optional: placeholder text #}
    required=false,         {# Optional: is required #}
    error=none,             {# Optional: error message #}
    help_text=none,         {# Optional: help text #}
    attrs={}                {# Optional: extra attributes #}
) %}
{# ... implementation ... #}
{% endmacro %}
```

---

## 3. Primitive Components

### Icon Component

```html
{# components/primitives/icon.html #}

{#
    Renders a Bootstrap icon with proper accessibility.
    
    Parameters:
        name (str, required): Icon name without 'bi-' prefix
        label (str): Accessible label. If provided, icon is not decorative
        size (str): 'sm' | 'md' | 'lg' | 'xl'. Default: 'md'
        class (str): Additional CSS classes
#}

{% macro icon(name, label=none, size='md', class='') %}
{% set size_class = {
    'sm': 'fs-6',
    'md': 'fs-5', 
    'lg': 'fs-4',
    'xl': 'fs-3'
}[size] %}

{% if label %}
<i class="bi bi-{{ name }} {{ size_class }} {{ class }}" 
   role="img" 
   aria-label="{{ label }}"></i>
{% else %}
<i class="bi bi-{{ name }} {{ size_class }} {{ class }}" 
   aria-hidden="true"></i>
{% endif %}
{% endmacro %}
```

### Badge Component

```html
{# components/primitives/badge.html #}

{#
    Status badge with semantic colors.
    
    Parameters:
        text (str, required): Badge text
        variant (str): 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info'
        pill (bool): Rounded pill style. Default: false
        icon (str): Optional icon name
#}

{% macro badge(text, variant='secondary', pill=false, icon=none) %}
<span class="badge bg-{{ variant }} {{ 'rounded-pill' if pill }}">
    {% if icon %}
    <i class="bi bi-{{ icon }} me-1" aria-hidden="true"></i>
    {% endif %}
    {{ text }}
</span>
{% endmacro %}

{# Semantic shortcuts #}
{% macro badge_success(text, icon='check-circle') %}
    {{ badge(text, variant='success', icon=icon) }}
{% endmacro %}

{% macro badge_pending(text, icon='clock') %}
    {{ badge(text, variant='warning', icon=icon) }}
{% endmacro %}

{% macro badge_error(text, icon='exclamation-circle') %}
    {{ badge(text, variant='danger', icon=icon) }}
{% endmacro %}
```

### Spinner Component

```html
{# components/primitives/spinner.html #}

{#
    Loading spinner with accessible label.
    
    Parameters:
        size (str): 'sm' | 'md' | 'lg'. Default: 'md'
        label (str): Screen reader text. Default: 'Cargando...'
        variant (str): Color variant. Default: 'primary'
        type (str): 'border' | 'grow'. Default: 'border'
#}

{% macro spinner(size='md', label='Cargando...', variant='primary', type='border') %}
{% set size_class = {'sm': 'spinner-' ~ type ~ '-sm', 'md': '', 'lg': ''}[size] %}

<div class="spinner-{{ type }} text-{{ variant }} {{ size_class }}" 
     role="status"
     {% if size == 'lg' %}style="width: 3rem; height: 3rem;"{% endif %}>
    <span class="visually-hidden">{{ label }}</span>
</div>
{% endmacro %}

{# Full-page loading overlay #}
{% macro loading_overlay(label='Cargando...') %}
<div class="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-body bg-opacity-75"
     style="z-index: 1050;"
     role="status"
     aria-live="polite">
    <div class="text-center">
        {{ spinner(size='lg', label=label) }}
        <p class="mt-2 text-body-secondary">{{ label }}</p>
    </div>
</div>
{% endmacro %}
```

---

## 4. Form Components

### Form Field Wrapper

```html
{# components/forms/field.html #}

{#
    Wraps form inputs with label, help text, and error handling.
    
    Parameters:
        name (str, required): Field name for ID generation
        label (str, required): Field label text
        required (bool): Show required indicator. Default: false
        error (str): Error message to display
        help_text (str): Help text below field
        class (str): Additional wrapper classes
        
    Usage with caller():
        {% call field('email', 'Correo electrónico', required=true) %}
            <input type="email" id="email" name="email" class="form-control">
        {% endcall %}
#}

{% macro field(name, label, required=false, error=none, help_text=none, class='') %}
{% set field_id = name %}
{% set error_id = name ~ '-error' if error else none %}
{% set help_id = name ~ '-help' if help_text else none %}
{% set described_by = [error_id, help_id] | select | join(' ') %}

<div class="mb-3 {{ class }}">
    <label for="{{ field_id }}" class="form-label">
        {{ label }}
        {% if required %}
        <span class="text-danger" aria-hidden="true">*</span>
        <span class="visually-hidden">(requerido)</span>
        {% endif %}
    </label>
    
    {# Render the input via caller #}
    {{ caller() }}
    
    {% if error %}
    <div id="{{ error_id }}" class="invalid-feedback d-block" role="alert">
        <i class="bi bi-exclamation-circle me-1" aria-hidden="true"></i>
        {{ error }}
    </div>
    {% endif %}
    
    {% if help_text %}
    <div id="{{ help_id }}" class="form-text">
        {{ help_text }}
    </div>
    {% endif %}
</div>
{% endmacro %}
```

### Text Input Component

```html
{# components/forms/input.html #}

{#
    Text input with full accessibility support.
    
    Parameters:
        name (str, required): Input name and ID
        label (str, required): Label text
        type (str): Input type. Default: 'text'
        value (str): Current value. Default: ''
        placeholder (str): Placeholder text
        required (bool): Is required. Default: false
        disabled (bool): Is disabled. Default: false
        readonly (bool): Is readonly. Default: false
        error (str): Error message
        help_text (str): Help text
        autocomplete (str): Autocomplete attribute
        pattern (str): Validation pattern
        minlength (int): Minimum length
        maxlength (int): Maximum length
        attrs (dict): Additional attributes
#}

{% macro input(
    name,
    label,
    type='text',
    value='',
    placeholder='',
    required=false,
    disabled=false,
    readonly=false,
    error=none,
    help_text=none,
    autocomplete=none,
    pattern=none,
    minlength=none,
    maxlength=none,
    attrs={}
) %}
{% set has_error = error is not none %}
{% set error_id = name ~ '-error' if has_error else none %}
{% set help_id = name ~ '-help' if help_text else none %}
{% set aria_described = [error_id, help_id] | select | join(' ') or none %}

<div class="mb-3">
    <label for="{{ name }}" class="form-label">
        {{ label }}
        {% if required %}
        <span class="text-danger" aria-hidden="true">*</span>
        {% endif %}
    </label>
    
    <input type="{{ type }}"
           id="{{ name }}"
           name="{{ name }}"
           value="{{ value }}"
           class="form-control {{ 'is-invalid' if has_error }}"
           {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
           {% if required %}required aria-required="true"{% endif %}
           {% if disabled %}disabled{% endif %}
           {% if readonly %}readonly{% endif %}
           {% if has_error %}aria-invalid="true"{% endif %}
           {% if aria_described %}aria-describedby="{{ aria_described }}"{% endif %}
           {% if autocomplete %}autocomplete="{{ autocomplete }}"{% endif %}
           {% if pattern %}pattern="{{ pattern }}"{% endif %}
           {% if minlength %}minlength="{{ minlength }}"{% endif %}
           {% if maxlength %}maxlength="{{ maxlength }}"{% endif %}
           {% for key, val in attrs.items() %}{{ key }}="{{ val }}"{% endfor %}>
    
    {% if has_error %}
    <div id="{{ error_id }}" class="invalid-feedback" role="alert">
        {{ error }}
    </div>
    {% endif %}
    
    {% if help_text %}
    <div id="{{ help_id }}" class="form-text">{{ help_text }}</div>
    {% endif %}
</div>
{% endmacro %}
```

### Select Component

```html
{# components/forms/select.html #}

{#
    Select dropdown with options.
    
    Parameters:
        name (str, required): Select name and ID
        label (str, required): Label text
        options (list, required): List of {'value': str, 'label': str, 'disabled': bool}
        selected (str): Currently selected value
        placeholder (str): Placeholder option text
        required (bool): Is required. Default: false
        disabled (bool): Is disabled. Default: false
        error (str): Error message
        multiple (bool): Allow multiple selection. Default: false
        size (int): Visible options for multiple. Default: none
#}

{% macro select(
    name,
    label,
    options,
    selected=none,
    placeholder=none,
    required=false,
    disabled=false,
    error=none,
    multiple=false,
    size=none
) %}
{% set has_error = error is not none %}

<div class="mb-3">
    <label for="{{ name }}" class="form-label">
        {{ label }}
        {% if required %}
        <span class="text-danger" aria-hidden="true">*</span>
        {% endif %}
    </label>
    
    <select id="{{ name }}"
            name="{{ name }}"
            class="form-select {{ 'is-invalid' if has_error }}"
            {% if required %}required aria-required="true"{% endif %}
            {% if disabled %}disabled{% endif %}
            {% if multiple %}multiple{% endif %}
            {% if size %}size="{{ size }}"{% endif %}
            {% if has_error %}aria-invalid="true" aria-describedby="{{ name }}-error"{% endif %}>
        
        {% if placeholder %}
        <option value="" {% if not selected %}selected{% endif %} disabled>
            {{ placeholder }}
        </option>
        {% endif %}
        
        {% for option in options %}
        <option value="{{ option.value }}"
                {% if option.value == selected %}selected{% endif %}
                {% if option.disabled | default(false) %}disabled{% endif %}>
            {{ option.label }}
        </option>
        {% endfor %}
    </select>
    
    {% if has_error %}
    <div id="{{ name }}-error" class="invalid-feedback" role="alert">
        {{ error }}
    </div>
    {% endif %}
</div>
{% endmacro %}
```

---

## 5. Feedback Components

### Alert Component

```html
{# components/feedback/alert.html #}

{#
    Alert message with optional dismissibility.
    
    Parameters:
        message (str, required): Alert message
        variant (str): 'success' | 'danger' | 'warning' | 'info'. Default: 'info'
        dismissible (bool): Show close button. Default: true
        icon (str): Override default icon. Default: auto based on variant
        heading (str): Optional alert heading
        id (str): Optional element ID
#}

{% macro alert(
    message,
    variant='info',
    dismissible=true,
    icon=none,
    heading=none,
    id=none
) %}
{% set icons = {
    'success': 'check-circle-fill',
    'danger': 'exclamation-triangle-fill',
    'warning': 'exclamation-triangle-fill',
    'info': 'info-circle-fill'
} %}
{% set icon_name = icon or icons[variant] %}
{% set role = 'alert' if variant in ['danger', 'warning'] else 'status' %}

<div class="alert alert-{{ variant }} {{ 'd-flex' if not heading }} {{ 'alert-dismissible fade show' if dismissible }}"
     role="{{ role }}"
     {% if id %}id="{{ id }}"{% endif %}>
    
    {% if heading %}
    <h4 class="alert-heading">
        <i class="bi bi-{{ icon_name }} me-2" aria-hidden="true"></i>
        {{ heading }}
    </h4>
    <p class="mb-0">{{ message }}</p>
    {% else %}
    <i class="bi bi-{{ icon_name }} flex-shrink-0 me-2" aria-hidden="true"></i>
    <div>{{ message }}</div>
    {% endif %}
    
    {% if dismissible %}
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="alert" 
            aria-label="Cerrar"></button>
    {% endif %}
</div>
{% endmacro %}

{# Semantic shortcuts #}
{% macro alert_success(message, dismissible=true) %}
    {{ alert(message, variant='success', dismissible=dismissible) }}
{% endmacro %}

{% macro alert_error(message, dismissible=true) %}
    {{ alert(message, variant='danger', dismissible=dismissible) }}
{% endmacro %}

{% macro alert_warning(message, dismissible=true) %}
    {{ alert(message, variant='warning', dismissible=dismissible) }}
{% endmacro %}

{% macro alert_info(message, dismissible=true) %}
    {{ alert(message, variant='info', dismissible=dismissible) }}
{% endmacro %}
```

### Modal Component

```html
{# components/feedback/modal.html #}

{#
    Modal dialog component.
    
    Parameters:
        id (str, required): Modal ID for JavaScript targeting
        title (str, required): Modal title
        size (str): 'sm' | 'md' | 'lg' | 'xl'. Default: 'md'
        centered (bool): Vertically center modal. Default: true
        static_backdrop (bool): Prevent closing on backdrop click. Default: false
        scrollable (bool): Scrollable body for long content. Default: false
        footer (bool): Show footer section. Default: true
        close_label (str): Close button label. Default: 'Cerrar'
        
    Slots (via caller and set):
        body: Modal body content (via caller)
        footer: Custom footer content (via set before call)
#}

{% macro modal(
    id,
    title,
    size='md',
    centered=true,
    static_backdrop=false,
    scrollable=false,
    footer=true,
    close_label='Cerrar'
) %}
{% set size_class = '' if size == 'md' else 'modal-' ~ size %}
{% set dialog_classes = [
    'modal-dialog',
    size_class,
    'modal-dialog-centered' if centered,
    'modal-dialog-scrollable' if scrollable
] | select | join(' ') %}

<div class="modal fade" 
     id="{{ id }}" 
     tabindex="-1" 
     aria-labelledby="{{ id }}-title" 
     aria-hidden="true"
     {% if static_backdrop %}data-bs-backdrop="static" data-bs-keyboard="false"{% endif %}>
    <div class="{{ dialog_classes }}">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title h5" id="{{ id }}-title">{{ title }}</h2>
                <button type="button" 
                        class="btn-close" 
                        data-bs-dismiss="modal" 
                        aria-label="Cerrar"></button>
            </div>
            
            <div class="modal-body">
                {{ caller() }}
            </div>
            
            {% if footer %}
            <div class="modal-footer">
                {% if modal_footer is defined %}
                    {{ modal_footer }}
                {% else %}
                <button type="button" 
                        class="btn btn-secondary" 
                        data-bs-dismiss="modal">
                    {{ close_label }}
                </button>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endmacro %}
```

### Confirmation Modal

```html
{# components/feedback/confirm_modal.html #}

{#
    Pre-configured confirmation modal.
    
    Parameters:
        id (str, required): Modal ID
        title (str): Modal title. Default: 'Confirmar acción'
        message (str, required): Confirmation message
        confirm_text (str): Confirm button text. Default: 'Confirmar'
        cancel_text (str): Cancel button text. Default: 'Cancelar'
        variant (str): Confirm button variant. Default: 'danger'
        icon (str): Icon name. Default: 'exclamation-triangle'
        on_confirm (str): JavaScript function to call on confirm
#}

{% macro confirm_modal(
    id,
    message,
    title='Confirmar acción',
    confirm_text='Confirmar',
    cancel_text='Cancelar',
    variant='danger',
    icon='exclamation-triangle',
    on_confirm=none
) %}
<div class="modal fade" 
     id="{{ id }}" 
     tabindex="-1" 
     aria-labelledby="{{ id }}-title" 
     aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title h5" id="{{ id }}-title">
                    <i class="bi bi-{{ icon }} text-{{ variant }} me-2" aria-hidden="true"></i>
                    {{ title }}
                </h2>
                <button type="button" 
                        class="btn-close" 
                        data-bs-dismiss="modal" 
                        aria-label="Cerrar"></button>
            </div>
            
            <div class="modal-body">
                <p id="{{ id }}-message">{{ message }}</p>
            </div>
            
            <div class="modal-footer">
                <button type="button" 
                        class="btn btn-secondary" 
                        data-bs-dismiss="modal">
                    {{ cancel_text }}
                </button>
                <button type="button" 
                        class="btn btn-{{ variant }}"
                        id="{{ id }}-confirm"
                        {% if on_confirm %}onclick="{{ on_confirm }}"{% endif %}>
                    <i class="bi bi-{{ icon }} me-1" aria-hidden="true"></i>
                    {{ confirm_text }}
                </button>
            </div>
        </div>
    </div>
</div>
{% endmacro %}
```

---

## 6. Layout Components

### Card Component

```html
{# components/layout/card.html #}

{#
    Flexible card component with optional sections.
    
    Parameters:
        title (str): Card title in header
        title_tag (str): Heading tag for title. Default: 'h3'
        subtitle (str): Optional subtitle
        show_header (bool): Show header section. Default: true if title provided
        show_footer (bool): Show footer section. Default: false
        variant (str): Border color variant. Default: none
        class (str): Additional card classes
        id (str): Card element ID
        data (dict): Data attributes
        
    Slots:
        header_actions: Content for header right side (set before call)
        body: Main content (via caller)
        footer: Footer content (set before call)
#}

{% macro card(
    title=none,
    title_tag='h3',
    subtitle=none,
    show_header=none,
    show_footer=false,
    variant=none,
    class='',
    id=none,
    data={}
) %}
{% set show_header = show_header if show_header is not none else (title is not none) %}
{% set border_class = 'border-' ~ variant if variant else '' %}

<div class="card {{ border_class }} {{ class }}"
     {% if id %}id="{{ id }}"{% endif %}
     {% for key, value in data.items() %}data-{{ key }}="{{ value }}"{% endfor %}>
    
    {% if show_header %}
    <div class="card-header d-flex justify-content-between align-items-center">
        <div>
            {% if title %}
            <{{ title_tag }} class="card-title h5 mb-0">{{ title }}</{{ title_tag }}>
            {% endif %}
            {% if subtitle %}
            <small class="text-body-secondary">{{ subtitle }}</small>
            {% endif %}
        </div>
        {% if card_header_actions is defined %}
        <div class="card-header-actions">
            {{ card_header_actions }}
        </div>
        {% endif %}
    </div>
    {% endif %}
    
    <div class="card-body">
        {{ caller() }}
    </div>
    
    {% if show_footer and card_footer is defined %}
    <div class="card-footer">
        {{ card_footer }}
    </div>
    {% endif %}
</div>
{% endmacro %}
```

### Empty State Component

```html
{# components/layout/empty_state.html #}

{#
    Empty state placeholder for lists/grids with no data.
    
    Parameters:
        message (str, required): Primary message
        description (str): Optional secondary description
        icon (str): Icon name. Default: 'inbox'
        action_url (str): Optional action button URL
        action_text (str): Optional action button text
        action_icon (str): Action button icon. Default: 'plus-lg'
#}

{% macro empty_state(
    message,
    description=none,
    icon='inbox',
    action_url=none,
    action_text=none,
    action_icon='plus-lg'
) %}
<div class="text-center py-5" role="status">
    <i class="bi bi-{{ icon }} display-1 text-body-secondary mb-3" aria-hidden="true"></i>
    
    <h3 class="h5 text-body-secondary">{{ message }}</h3>
    
    {% if description %}
    <p class="text-body-secondary mb-4">{{ description }}</p>
    {% endif %}
    
    {% if action_url and action_text %}
    <a href="{{ action_url }}" class="btn btn-primary">
        <i class="bi bi-{{ action_icon }} me-1" aria-hidden="true"></i>
        {{ action_text }}
    </a>
    {% endif %}
</div>
{% endmacro %}
```

### Section Component

```html
{# components/layout/section.html #}

{#
    Page section with consistent spacing and optional heading.
    
    Parameters:
        title (str): Section heading
        title_tag (str): Heading tag. Default: 'h2'
        title_id (str): ID for heading (for aria-labelledby)
        description (str): Optional description below title
        class (str): Additional section classes
        compact (bool): Reduced padding. Default: false
        
    Slots:
        actions: Header actions (set before call)
        content: Section content (via caller)
#}

{% macro section(
    title=none,
    title_tag='h2',
    title_id=none,
    description=none,
    class='',
    compact=false
) %}
{% set padding_class = 'py-3' if compact else 'py-4' %}
{% set generated_id = title_id or (title | lower | replace(' ', '-') if title else none) %}

<section class="{{ padding_class }} {{ class }}"
         {% if generated_id %}aria-labelledby="{{ generated_id }}"{% endif %}>
    
    {% if title or section_actions is defined %}
    <header class="d-flex justify-content-between align-items-start mb-3">
        <div>
            {% if title %}
            <{{ title_tag }} {% if generated_id %}id="{{ generated_id }}"{% endif %} class="mb-1">
                {{ title }}
            </{{ title_tag }}>
            {% endif %}
            
            {% if description %}
            <p class="text-body-secondary mb-0">{{ description }}</p>
            {% endif %}
        </div>
        
        {% if section_actions is defined %}
        <div class="section-actions">
            {{ section_actions }}
        </div>
        {% endif %}
    </header>
    {% endif %}
    
    {{ caller() }}
</section>
{% endmacro %}
```

---

## 7. Composite Components

### Patient Card

```html
{# components/composite/patient_card.html #}

{#
    Complete patient card with sessions preview and actions.
    
    Parameters:
        patient (Person, required): Patient model object
        show_actions (bool): Show edit/delete buttons. Default: true
        show_sessions (bool): Show sessions carousel. Default: true
        max_sessions (int): Maximum sessions to show. Default: 5
        compact (bool): Compact card mode. Default: false
#}

{% from 'components/primitives/badge.html' import badge, badge_pending %}
{% from 'components/primitives/button.html' import button %}

{% macro patient_card(
    patient,
    show_actions=true,
    show_sessions=true,
    max_sessions=5,
    compact=false
) %}
{% set pending_count = patient.sessions | selectattr('pending') | list | length %}
{% set pending_total = patient.pending_total | default(0) %}

<article class="card h-100" 
         id="patient-{{ patient.id }}"
         data-patient-id="{{ patient.id }}"
         aria-labelledby="patient-{{ patient.id }}-name">
    
    {# Card Header #}
    <div class="card-header d-flex justify-content-between align-items-center">
        <h3 id="patient-{{ patient.id }}-name" class="card-title h5 mb-0">
            {{ patient.name }}
        </h3>
        {% if pending_count > 0 %}
        {{ badge_pending(pending_count ~ ' pendiente' ~ ('s' if pending_count > 1 else '')) }}
        {% endif %}
    </div>
    
    {# Card Body #}
    <div class="card-body {{ 'py-2' if compact }}">
        {% if patient.notes and not compact %}
        <p class="card-text text-body-secondary small">{{ patient.notes | truncate(100) }}</p>
        {% endif %}
        
        {# Sessions Carousel #}
        {% if show_sessions and patient.sessions %}
        <div id="carousel-{{ patient.id }}" 
             class="carousel slide"
             data-bs-ride="false"
             aria-label="Sesiones de {{ patient.name }}">
            <div class="carousel-inner">
                {% for session in patient.sessions[:max_sessions] %}
                <div class="carousel-item {{ 'active' if loop.first }}">
                    {% include 'sessions/_card_mini.html' %}
                </div>
                {% endfor %}
            </div>
            
            {% if patient.sessions | length > 1 %}
            <div class="carousel-indicators position-relative mt-2">
                {% for session in patient.sessions[:max_sessions] %}
                <button type="button" 
                        data-bs-target="#carousel-{{ patient.id }}"
                        data-bs-slide-to="{{ loop.index0 }}"
                        class="{{ 'active' if loop.first }}"
                        aria-label="Sesión {{ loop.index }}"
                        {% if loop.first %}aria-current="true"{% endif %}></button>
                {% endfor %}
            </div>
            {% endif %}
        </div>
        {% elif show_sessions %}
        <p class="text-body-secondary text-center py-3 mb-0">
            <i class="bi bi-calendar-x me-1" aria-hidden="true"></i>
            Sin sesiones registradas
        </p>
        {% endif %}
    </div>
    
    {# Card Footer with Actions #}
    {% if show_actions %}
    <div class="card-footer">
        <div class="btn-group w-100" role="group" aria-label="Acciones del paciente">
            <button type="button" 
                    class="btn btn-outline-secondary flex-fill"
                    onclick="openEditPatientModal({{ patient.id }}, '{{ patient.name | e }}')"
                    aria-label="Editar {{ patient.name }}">
                <i class="bi bi-pencil" aria-hidden="true"></i>
                <span class="d-none d-sm-inline ms-1">Editar</span>
            </button>
            <a href="{{ url_for('sessions.add_session', person_id=patient.id) }}"
               class="btn btn-outline-primary flex-fill"
               aria-label="Nueva sesión para {{ patient.name }}">
                <i class="bi bi-plus-lg" aria-hidden="true"></i>
                <span class="d-none d-sm-inline ms-1">Sesión</span>
            </a>
            <button type="button" 
                    class="btn btn-outline-danger flex-fill"
                    onclick="openDeletePatientModal({{ patient.id }}, '{{ patient.name | e }}')"
                    aria-label="Eliminar {{ patient.name }}">
                <i class="bi bi-trash" aria-hidden="true"></i>
                <span class="d-none d-sm-inline ms-1">Eliminar</span>
            </button>
        </div>
    </div>
    {% endif %}
</article>
{% endmacro %}
```

### Data Table

```html
{# components/composite/data_table.html #}

{#
    Accessible data table with sorting and empty state.
    
    Parameters:
        columns (list, required): List of {'key': str, 'label': str, 'sortable': bool, 'class': str}
        rows (list, required): List of row data dicts
        id (str): Table ID. Default: 'data-table'
        caption (str): Table caption
        striped (bool): Striped rows. Default: true
        hover (bool): Hover effect. Default: true
        responsive (bool): Responsive wrapper. Default: true
        empty_message (str): Message when no data
        row_id_key (str): Key for row ID attribute. Default: 'id'
#}

{% macro data_table(
    columns,
    rows,
    id='data-table',
    caption=none,
    striped=true,
    hover=true,
    responsive=true,
    empty_message='No hay datos disponibles',
    row_id_key='id'
) %}
{% set table_classes = [
    'table',
    'table-striped' if striped,
    'table-hover' if hover
] | select | join(' ') %}

{% if responsive %}<div class="table-responsive">{% endif %}

<table id="{{ id }}" class="{{ table_classes }}">
    {% if caption %}
    <caption>{{ caption }}</caption>
    {% endif %}
    
    <thead>
        <tr>
            {% for col in columns %}
            <th scope="col" class="{{ col.class | default('') }}">
                {% if col.sortable | default(false) %}
                <button type="button" 
                        class="btn btn-link p-0 text-decoration-none"
                        onclick="sortTable('{{ col.key }}')"
                        aria-label="Ordenar por {{ col.label }}">
                    {{ col.label }}
                    <i class="bi bi-arrow-down-up ms-1" aria-hidden="true"></i>
                </button>
                {% else %}
                {{ col.label }}
                {% endif %}
            </th>
            {% endfor %}
        </tr>
    </thead>
    
    <tbody>
        {% for row in rows %}
        <tr {% if row[row_id_key] %}id="row-{{ row[row_id_key] }}" data-id="{{ row[row_id_key] }}"{% endif %}>
            {% for col in columns %}
            <td class="{{ col.class | default('') }}">
                {{ row[col.key] }}
            </td>
            {% endfor %}
        </tr>
        {% else %}
        <tr>
            <td colspan="{{ columns | length }}" class="text-center py-4 text-body-secondary">
                <i class="bi bi-inbox me-1" aria-hidden="true"></i>
                {{ empty_message }}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

{% if responsive %}</div>{% endif %}
{% endmacro %}
```

---

## 8. Component Composition Patterns

### Slot Pattern with set/caller

```html
{# Define component with slots #}
{% macro card_with_slots(title) %}
<div class="card">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">{{ caller() }}</div>
    {% if card_footer is defined %}
    <div class="card-footer">{{ card_footer }}</div>
    {% endif %}
</div>
{% endmacro %}

{# Usage with slots #}
{% set card_footer %}
<button class="btn btn-primary">Guardar</button>
{% endset %}

{% call card_with_slots('Mi Tarjeta') %}
    <p>Contenido del body</p>
{% endcall %}
```

### Wrapper Pattern

```html
{# Wrapper component that enhances children #}
{% macro clickable_card(url, class='') %}
<a href="{{ url }}" class="text-decoration-none {{ class }}">
    <div class="card h-100 card-hover">
        {{ caller() }}
    </div>
</a>
{% endmacro %}

{# Usage #}
{% call clickable_card(url_for('patients.view', id=patient.id)) %}
    <div class="card-body">
        <h3>{{ patient.name }}</h3>
    </div>
{% endcall %}
```

### Render Props Pattern

```html
{# Component that accepts a rendering macro #}
{% macro list_component(items, render_item) %}
<ul class="list-group">
    {% for item in items %}
    <li class="list-group-item">
        {{ render_item(item) }}
    </li>
    {% endfor %}
</ul>
{% endmacro %}

{# Define custom item renderer #}
{% macro render_patient(patient) %}
<div class="d-flex justify-content-between">
    <span>{{ patient.name }}</span>
    <span class="badge bg-primary">{{ patient.sessions | length }}</span>
</div>
{% endmacro %}

{# Usage #}
{{ list_component(patients, render_patient) }}
```

---

## 9. Component Documentation Template

```html
{#
================================================================================
Component: [Component Name]
================================================================================

Description:
    Brief description of what the component does and when to use it.

Parameters:
    name (type, required|optional): Description. Default: value
    
Slots:
    slot_name: Description of slot content
    
Events:
    on_event: When this event fires and what data it passes

Accessibility:
    - ARIA attributes used
    - Keyboard interaction supported
    - Screen reader considerations

Examples:
    Basic:
        {{ component(required_param='value') }}
    
    With options:
        {{ component(required_param='value', optional=true) }}
    
    With slots:
        {% set slot_name %}content{% endset %}
        {% call component('value') %}body{% endcall %}

Dependencies:
    - Other components this requires
    - CSS/JS files needed

================================================================================
#}
```

---

## Quick Reference

### Component Parameter Types

| Type | Jinja2 | Example |
|------|--------|---------|
| String | `str` | `name='John'` |
| Boolean | `bool` | `required=true` |
| Integer | `int` | `max_items=5` |
| List | `list` | `options=[{...}]` |
| Dict | `dict` | `attrs={'data-id': '1'}` |
| None | `none` | `error=none` |

### Common Parameter Patterns

```html
{# Boolean with semantic name #}
show_header=true
is_active=false
enable_sort=true

{# Variant selection #}
variant='primary'   {# primary|secondary|success|danger|warning|info #}
size='md'           {# sm|md|lg|xl #}

{# Optional content #}
icon=none           {# Bootstrap icon name or none #}
help_text=none      {# Additional help or none #}

{# Extra attributes passthrough #}
attrs={'data-testid': 'my-button', 'tabindex': '0'}
```
