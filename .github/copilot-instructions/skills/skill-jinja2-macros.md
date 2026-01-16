# Skill: Jinja2 Macros

## Overview

Jinja2 macros are reusable template functions that generate HTML components. This skill covers macro creation, parameters, organization, and best practices for the Therapy Session Management Application. The goal is to create a component library that reduces duplication and ensures UI consistency.

---

## Macro Basics

### Syntax

```jinja2
{# Define a macro #}
{% macro macro_name(param1, param2='default') %}
    <!-- HTML content -->
    <p>{{ param1 }} - {{ param2 }}</p>
{% endmacro %}

{# Call a macro #}
{{ macro_name('value1', 'value2') }}
{{ macro_name('value1') }}  {# Uses default for param2 #}
```

### Simple Example

```jinja2
{# Define button macro #}
{% macro button(text, type='button') %}
    <button type="{{ type }}" class="btn btn-primary">
        {{ text }}
    </button>
{% endmacro %}

{# Usage #}
{{ button('Save') }}
{{ button('Submit', type='submit') }}
```

---

## Parameters

### Required Parameters

```jinja2
{% macro patient_card(patient_id, patient_name) %}
    <article class="patient-card" data-patient-id="{{ patient_id }}">
        <h3>{{ patient_name }}</h3>
    </article>
{% endmacro %}

{# Must provide both parameters #}
{{ patient_card(123, 'Juan Pérez') }}
```

### Optional Parameters with Defaults

```jinja2
{% macro alert(message, type='info', dismissible=true) %}
    <div class="alert alert-{{ type }}{% if dismissible %} alert-dismissible{% endif %}" role="alert">
        {{ message }}
        {% if dismissible %}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        {% endif %}
    </div>
{% endmacro %}

{# Different call styles #}
{{ alert('Success!', type='success') }}
{{ alert('Warning', dismissible=false) }}
{{ alert('Info message') }}  {# Uses all defaults #}
```

### Variable Arguments

```jinja2
{# Accept any number of arguments #}
{% macro button_group(buttons=[]) %}
    <div class="btn-group" role="group">
        {% for btn in buttons %}
            <button type="button" class="btn btn-{{ btn.type|default('secondary') }}">
                {{ btn.label }}
            </button>
        {% endfor %}
    </div>
{% endmacro %}

{# Usage #}
{{ button_group([
    {'label': 'Edit', 'type': 'primary'},
    {'label': 'Delete', 'type': 'danger'}
]) }}
```

### Keyword Arguments (**kwargs)

```jinja2
{% macro input_field(name, label, **kwargs) %}
    <div class="mb-3">
        <label for="{{ name }}" class="form-label">{{ label }}</label>
        <input 
            type="{{ kwargs.get('type', 'text') }}" 
            class="form-control {{ kwargs.get('class', '') }}" 
            id="{{ name }}" 
            name="{{ name }}"
            {% if kwargs.get('required') %}required{% endif %}
            {% if kwargs.get('placeholder') %}placeholder="{{ kwargs.placeholder }}"{% endif %}
            value="{{ kwargs.get('value', '') }}">
    </div>
{% endmacro %}

{# Usage #}
{{ input_field('email', 'Correo electrónico', type='email', required=true, placeholder='usuario@ejemplo.com') }}
```

---

## Macro Organization

### File Structure

```
templates/
├── base.html
├── macros/
│   ├── __init__.html        # Imports all macros (optional)
│   ├── buttons.html         # Button components
│   ├── cards.html           # Card components
│   ├── forms.html           # Form components
│   ├── modals.html          # Modal components
│   ├── badges.html          # Badge/tag components
│   └── icons.html           # Icon helpers
├── auth/
├── patients/
└── sessions/
```

### Importing Macros

```jinja2
{# Import all macros from a file #}
{% import 'macros/buttons.html' as buttons %}

{# Use imported macros #}
{{ buttons.primary('Save') }}
{{ buttons.danger('Delete') }}

{# Import specific macros #}
{% from 'macros/forms.html' import input_field, textarea_field %}

{# Use imported macros directly #}
{{ input_field('name', 'Nombre') }}
{{ textarea_field('notes', 'Notas') }}

{# Import with alias #}
{% from 'macros/cards.html' import patient_card as pcard %}
{{ pcard(patient) }}
```

---

## Project-Specific Macros

### macros/buttons.html - Button Components

```jinja2
{#
    Button Components
    Reusable button macros with consistent styling
#}

{# Primary action button #}
{% macro primary(text, type='button', icon=none, **attrs) %}
    <button type="{{ type }}" class="btn btn-primary {{ attrs.get('class', '') }}" {{ _attrs(attrs) }}>
        {% if icon %}<i class="bi bi-{{ icon }} me-1" aria-hidden="true"></i>{% endif %}
        {{ text }}
    </button>
{% endmacro %}

{# Secondary/outline button #}
{% macro secondary(text, type='button', icon=none, **attrs) %}
    <button type="{{ type }}" class="btn btn-outline-secondary {{ attrs.get('class', '') }}" {{ _attrs(attrs) }}>
        {% if icon %}<i class="bi bi-{{ icon }} me-1" aria-hidden="true"></i>{% endif %}
        {{ text }}
    </button>
{% endmacro %}

{# Danger/delete button #}
{% macro danger(text, type='button', icon='trash', **attrs) %}
    <button type="{{ type }}" class="btn btn-outline-danger {{ attrs.get('class', '') }}" {{ _attrs(attrs) }}>
        <i class="bi bi-{{ icon }} me-1" aria-hidden="true"></i>
        {{ text }}
    </button>
{% endmacro %}

{# Icon-only button #}
{% macro icon(icon_name, label, variant='secondary', **attrs) %}
    <button type="button" class="btn btn-{{ variant }} btn-icon {{ attrs.get('class', '') }}" 
            aria-label="{{ label }}" {{ _attrs(attrs) }}>
        <i class="bi bi-{{ icon_name }}" aria-hidden="true"></i>
    </button>
{% endmacro %}

{# Button group #}
{% macro group(buttons, size='', **attrs) %}
    <div class="btn-group{% if size %} btn-group-{{ size }}{% endif %} {{ attrs.get('class', '') }}" 
         role="group" {{ _attrs(attrs) }}>
        {% for btn in buttons %}
            {{ btn }}
        {% endfor %}
    </div>
{% endmacro %}

{# Helper to render attributes #}
{% macro _attrs(attrs) %}
    {%- for key, value in attrs.items() if key not in ['class', 'type'] -%}
        {{ key }}="{{ value }}"{{ ' ' }}
    {%- endfor -%}
{% endmacro %}
```

**Usage:**
```jinja2
{% from 'macros/buttons.html' import primary, secondary, danger, icon, group %}

{# Simple buttons #}
{{ primary('Guardar', type='submit') }}
{{ secondary('Cancelar') }}
{{ danger('Eliminar', onclick='confirmDelete()') }}

{# Icon button #}
{{ icon('pencil', 'Editar paciente', variant='primary') }}

{# Button group #}
{{ group([
    secondary('Editar', icon='pencil'),
    danger('Eliminar')
], size='sm') }}
```

---

### macros/cards.html - Card Components

```jinja2
{#
    Card Components
    Reusable card macros for consistent layout
#}

{# Base card wrapper #}
{% macro card(title=none, header_actions=none, footer=none) %}
    <article class="card h-100">
        {% if title or header_actions %}
            <div class="card-header d-flex justify-content-between align-items-center">
                {% if title %}
                    <h5 class="mb-0">{{ title }}</h5>
                {% endif %}
                {% if header_actions %}
                    <div class="card-header-actions">
                        {{ header_actions }}
                    </div>
                {% endif %}
            </div>
        {% endif %}
        
        <div class="card-body">
            {{ caller() }}
        </div>
        
        {% if footer %}
            <div class="card-footer">
                {{ footer }}
            </div>
        {% endif %}
    </article>
{% endmacro %}

{# Patient card #}
{% macro patient_card(patient, sessions=[], allow_delete=true) %}
    <article class="card h-100 patient-card" data-patient-id="{{ patient.id }}">
        {# Header with patient info #}
        <div class="card-header">
            <h5 class="mb-2 patient-name">
                <i class="bi bi-person-fill me-1 text-primary" aria-hidden="true"></i>
                {{ patient.name|title }}
            </h5>
            
            {# Action buttons #}
            <div class="btn-group btn-group-sm w-100" role="group" aria-label="Acciones de paciente">
                <button type="button"
                        class="btn btn-outline-secondary flex-fill"
                        onclick="openEditPatientModal({{ patient.id }}, '{{ patient.name|e }}')"
                        aria-label="Editar paciente {{ patient.name|title }}">
                    <i class="bi bi-pencil me-1" aria-hidden="true"></i>Editar
                </button>
                
                {% if allow_delete %}
                    <button type="button"
                            class="btn btn-outline-danger flex-fill"
                            onclick="openDeletePatientModal({{ patient.id }}, '{{ patient.name|e }}')"
                            aria-label="Eliminar paciente {{ patient.name|title }}">
                        <i class="bi bi-trash me-1" aria-hidden="true"></i>Eliminar
                    </button>
                {% endif %}
            </div>
        </div>
        
        {# Sessions carousel #}
        {% if sessions %}
            <div class="card-body p-0">
                {{ session_carousel(patient.id, sessions) }}
            </div>
        {% endif %}
        
        {# Footer with add session button #}
        <div class="card-footer">
            <button type="button" 
                    class="btn btn-sm btn-primary w-100"
                    onclick="openAddSessionModal({{ patient.id }}, '{{ patient.name|e }}')"
                    aria-label="Agregar sesión para {{ patient.name|title }}">
                <i class="bi bi-plus-circle me-1" aria-hidden="true"></i>Nueva Sesión
            </button>
        </div>
    </article>
{% endmacro %}

{# Session carousel (internal helper) #}
{% macro session_carousel(patient_id, sessions) %}
    <div id="carousel-{{ patient_id }}" class="carousel slide" data-bs-ride="false">
        {# Carousel items #}
        <div class="carousel-inner">
            {% for session in sessions %}
                <div class="carousel-item {% if loop.first %}active{% endif %}" data-session-id="{{ session.id }}">
                    {{ session_card(session, patient_id) }}
                </div>
            {% endfor %}
        </div>
        
        {# Indicators (only if multiple sessions) #}
        {% if sessions|length > 1 %}
            <div class="carousel-indicators carousel-indicators-bottom">
                {% for session in sessions %}
                    <button type="button" 
                            data-bs-target="#carousel-{{ patient_id }}" 
                            data-bs-slide-to="{{ loop.index0 }}" 
                            {% if loop.first %}class="active" aria-current="true"{% endif %}
                            aria-label="Sesión {{ loop.index }}"></button>
                {% endfor %}
            </div>
        {% endif %}
    </div>
{% endmacro %}

{# Individual session card #}
{% macro session_card(session, patient_id) %}
    <div class="p-3 session-card" data-session-id="{{ session.id }}">
        {# Session details #}
        <div class="d-flex justify-content-between align-items-start mb-2">
            <div>
                <p class="mb-1 fw-medium session-date">
                    <i class="bi bi-calendar3 me-1" aria-hidden="true"></i>
                    {{ session.formatted_date }}
                </p>
                <p class="mb-0 session-price">
                    <i class="bi bi-cash me-1" aria-hidden="true"></i>
                    {{ session.formatted_price }}
                </p>
            </div>
            
            {# Payment status badge #}
            <span class="badge {{ 'bg-warning' if session.pending else 'bg-success' }} session-status">
                {{ 'PENDIENTE' if session.pending else 'PAGADO' }}
            </span>
        </div>
        
        {# Action buttons #}
        <div class="btn-group w-100" role="group">
            {% if session.pending %}
                <button type="button" 
                        class="btn btn-success flex-fill toggle-payment-btn"
                        onclick="togglePayment({{ session.id }})"
                        aria-label="Marcar sesión como pagada">
                    <i class="bi bi-check-circle me-1" aria-hidden="true"></i>Pagado
                </button>
            {% else %}
                <button type="button" 
                        class="btn btn-outline-warning flex-fill toggle-payment-btn"
                        onclick="togglePayment({{ session.id }})"
                        aria-label="Marcar sesión como pendiente">
                    <i class="bi bi-clock me-1" aria-hidden="true"></i>Pendiente
                </button>
            {% endif %}
            
            <button type="button" 
                    class="btn btn-outline-secondary flex-fill"
                    onclick="openEditSessionModal({{ session.id }}, {{ patient_id }})"
                    aria-label="Editar sesión">
                <i class="bi bi-pencil" aria-hidden="true"></i>
            </button>
            
            <button type="button" 
                    class="btn btn-outline-danger flex-fill"
                    onclick="openDeleteSessionModal({{ session.id }}, '{{ session.formatted_date|e }}')"
                    aria-label="Eliminar sesión">
                <i class="bi bi-trash" aria-hidden="true"></i>
            </button>
        </div>
    </div>
{% endmacro %}
```

**Usage:**
```jinja2
{% from 'macros/cards.html' import card, patient_card %}

{# Generic card with caller content #}
{% call card(title='Mi Card') %}
    <p>Card content goes here</p>
{% endcall %}

{# Patient card with sessions #}
{{ patient_card(patient, sessions=patient.sessions, allow_delete=current_user.is_admin) }}
```

---

### macros/forms.html - Form Components

```jinja2
{#
    Form Components
    Reusable form field macros
#}

{# Text input field #}
{% macro input_field(name, label, type='text', value='', required=false, placeholder='', help_text='', error='') %}
    <div class="mb-3">
        <label for="{{ name }}" class="form-label">
            {{ label }}
            {% if required %}<span class="text-danger" aria-label="requerido">*</span>{% endif %}
        </label>
        <input 
            type="{{ type }}" 
            class="form-control {% if error %}is-invalid{% endif %}" 
            id="{{ name }}" 
            name="{{ name }}"
            value="{{ value }}"
            {% if required %}required aria-required="true"{% endif %}
            {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
            {% if error %}aria-invalid="true" aria-describedby="{{ name }}-error"{% endif %}>
        
        {% if help_text %}
            <div class="form-text">{{ help_text }}</div>
        {% endif %}
        
        {% if error %}
            <div class="invalid-feedback" id="{{ name }}-error">{{ error }}</div>
        {% endif %}
    </div>
{% endmacro %}

{# Textarea field #}
{% macro textarea_field(name, label, value='', rows=3, required=false, placeholder='', help_text='', error='') %}
    <div class="mb-3">
        <label for="{{ name }}" class="form-label">
            {{ label }}
            {% if required %}<span class="text-danger" aria-label="requerido">*</span>{% endif %}
        </label>
        <textarea 
            class="form-control {% if error %}is-invalid{% endif %}" 
            id="{{ name }}" 
            name="{{ name }}"
            rows="{{ rows }}"
            {% if required %}required aria-required="true"{% endif %}
            {% if placeholder %}placeholder="{{ placeholder }}"{% endif %}
            {% if error %}aria-invalid="true" aria-describedby="{{ name }}-error"{% endif %}>{{ value }}</textarea>
        
        {% if help_text %}
            <div class="form-text">{{ help_text }}</div>
        {% endif %}
        
        {% if error %}
            <div class="invalid-feedback" id="{{ name }}-error">{{ error }}</div>
        {% endif %}
    </div>
{% endmacro %}

{# Select field #}
{% macro select_field(name, label, options=[], selected='', required=false, help_text='', error='') %}
    <div class="mb-3">
        <label for="{{ name }}" class="form-label">
            {{ label }}
            {% if required %}<span class="text-danger" aria-label="requerido">*</span>{% endif %}
        </label>
        <select 
            class="form-select {% if error %}is-invalid{% endif %}" 
            id="{{ name }}" 
            name="{{ name }}"
            {% if required %}required aria-required="true"{% endif %}
            {% if error %}aria-invalid="true" aria-describedby="{{ name }}-error"{% endif %}>
            {% for option in options %}
                <option value="{{ option.value }}" {% if option.value == selected %}selected{% endif %}>
                    {{ option.label }}
                </option>
            {% endfor %}
        </select>
        
        {% if help_text %}
            <div class="form-text">{{ help_text }}</div>
        {% endif %}
        
        {% if error %}
            <div class="invalid-feedback" id="{{ name }}-error">{{ error }}</div>
        {% endif %}
    </div>
{% endmacro %}

{# Checkbox field #}
{% macro checkbox_field(name, label, checked=false, help_text='', error='') %}
    <div class="mb-3 form-check">
        <input 
            type="checkbox" 
            class="form-check-input {% if error %}is-invalid{% endif %}" 
            id="{{ name }}" 
            name="{{ name }}"
            {% if checked %}checked{% endif %}
            {% if error %}aria-invalid="true" aria-describedby="{{ name }}-error"{% endif %}>
        <label class="form-check-label" for="{{ name }}">
            {{ label }}
        </label>
        
        {% if help_text %}
            <div class="form-text">{{ help_text }}</div>
        {% endif %}
        
        {% if error %}
            <div class="invalid-feedback" id="{{ name }}-error">{{ error }}</div>
        {% endif %}
    </div>
{% endmacro %}

{# Form buttons group #}
{% macro form_actions(submit_text='Guardar', cancel_url=none, cancel_text='Cancelar') %}
    <div class="d-flex gap-2 justify-content-end">
        {% if cancel_url %}
            <a href="{{ cancel_url }}" class="btn btn-outline-secondary">{{ cancel_text }}</a>
        {% endif %}
        <button type="submit" class="btn btn-primary">{{ submit_text }}</button>
    </div>
{% endmacro %}
```

**Usage:**
```jinja2
{% from 'macros/forms.html' import input_field, textarea_field, select_field, checkbox_field, form_actions %}

<form method="POST">
    {{ form.hidden_tag() }}
    
    {{ input_field('name', 'Nombre del Paciente', required=true, placeholder='Ej: Juan Pérez') }}
    
    {{ textarea_field('notes', 'Notas', placeholder='Observaciones adicionales...') }}
    
    {{ input_field('session_date', 'Fecha de Sesión', type='date', required=true) }}
    
    {{ input_field('session_price', 'Precio', type='number', required=true, value='150') }}
    
    {{ checkbox_field('pending', 'Marcar como pendiente', checked=true) }}
    
    {{ form_actions(submit_text='Guardar Paciente', cancel_url=url_for('patients.index')) }}
</form>
```

---

### macros/modals.html - Modal Components

```jinja2
{#
    Modal Components
    Reusable modal dialog macros
#}

{# Base modal wrapper #}
{% macro modal(id, title, size='', static_backdrop=false) %}
    <div class="modal fade" id="{{ id }}" tabindex="-1" 
         aria-labelledby="{{ id }}-label" aria-hidden="true"
         {% if static_backdrop %}data-bs-backdrop="static" data-bs-keyboard="false"{% endif %}>
        <div class="modal-dialog{% if size %} modal-{{ size }}{% endif %}">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="{{ id }}-label">{{ title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <div class="modal-body">
                    {{ caller() }}
                </div>
            </div>
        </div>
    </div>
{% endmacro %}

{# Confirmation modal #}
{% macro confirm_modal(id, title, message, confirm_text='Confirmar', confirm_class='btn-primary', cancel_text='Cancelar') %}
    <div class="modal fade" id="{{ id }}" tabindex="-1" aria-labelledby="{{ id }}-label" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="{{ id }}-label">{{ title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <div class="modal-body">
                    <p>{{ message }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ cancel_text }}</button>
                    <button type="button" class="btn {{ confirm_class }}" id="{{ id }}-confirm">{{ confirm_text }}</button>
                </div>
            </div>
        </div>
    </div>
{% endmacro %}

{# Form modal #}
{% macro form_modal(id, title, form_id, size='') %}
    <div class="modal fade" id="{{ id }}" tabindex="-1" aria-labelledby="{{ id }}-label" aria-hidden="true">
        <div class="modal-dialog{% if size %} modal-{{ size }}{% endif %}">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="{{ id }}-label">{{ title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <form id="{{ form_id }}" method="POST">
                    <div class="modal-body">
                        {{ caller() }}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-primary">Guardar</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
{% endmacro %}
```

**Usage:**
```jinja2
{% from 'macros/modals.html' import modal, confirm_modal, form_modal %}

{# Generic modal #}
{% call modal('myModal', 'Modal Title') %}
    <p>Modal content goes here</p>
{% endcall %}

{# Confirmation modal #}
{{ confirm_modal(
    'deleteConfirm', 
    'Confirmar Eliminación', 
    '¿Está seguro de eliminar este paciente?',
    confirm_text='Eliminar',
    confirm_class='btn-danger'
) }}

{# Form modal #}
{% call form_modal('editPatientModal', 'Editar Paciente', 'editPatientForm') %}
    {{ input_field('name', 'Nombre', required=true) }}
    {{ textarea_field('notes', 'Notas') }}
{% endcall %}
```

---

## Advanced Patterns

### Caller Content

```jinja2
{# Define macro that accepts caller content #}
{% macro card(title) %}
    <div class="card">
        <div class="card-header">{{ title }}</div>
        <div class="card-body">
            {{ caller() }}  {# Content passed by caller #}
        </div>
    </div>
{% endmacro %}

{# Use with {% call %} block #}
{% call card('My Title') %}
    <p>This content is passed to the caller() in the macro</p>
    <button>Click me</button>
{% endcall %}
```

### Conditional Content Blocks

```jinja2
{% macro card(title, has_footer=false) %}
    <div class="card">
        <div class="card-header">{{ title }}</div>
        <div class="card-body">
            {{ caller() if caller else 'No content' }}
        </div>
        {% if has_footer %}
            <div class="card-footer">
                {{ caller.footer() if caller.footer is defined else '' }}
            </div>
        {% endif %}
    </div>
{% endmacro %}

{# Usage with named callers #}
{% call(footer) card('Title', has_footer=true) %}
    <p>Main content</p>
    {% set footer %}
        <button>Footer button</button>
    {% endset %}
{% endcall %}
```

### Macro Variables

```jinja2
{% macro list_items(items) %}
    {# Variables accessible within macro #}
    {% set item_count = items|length %}
    {% set is_empty = item_count == 0 %}
    
    {% if is_empty %}
        <p>No hay elementos</p>
    {% else %}
        <ul>
            {% for item in items %}
                <li>{{ loop.index }}. {{ item }}</li>
            {% endfor %}
        </ul>
        <p>Total: {{ item_count }} elementos</p>
    {% endif %}
{% endmacro %}
```

---

## Best Practices

### Naming Conventions

```jinja2
{# ✅ DO: Descriptive, specific names #}
{% macro patient_card() %}...{% endmacro %}
{% macro input_field() %}...{% endmacro %}
{% macro delete_button() %}...{% endmacro %}

{# ❌ DON'T: Vague or generic names #}
{% macro card1() %}...{% endmacro %}
{% macro field() %}...{% endmacro %}
{% macro btn() %}...{% endmacro %}
```

### Parameter Order

```jinja2
{# ✅ DO: Required first, optional last, logical grouping #}
{% macro button(text, type='button', icon=none, class='', onclick='') %}

{# ❌ DON'T: Random order #}
{% macro button(icon=none, text, onclick='', class='', type='button') %}
```

### Documentation

```jinja2
{#
    Patient Card Component
    
    Renders a patient card with sessions carousel and action buttons.
    
    Parameters:
        patient (object): Patient object with id and name
        sessions (list): List of session objects
        allow_delete (bool): Whether to show delete button (default: true)
    
    Example:
        {{ patient_card(patient, sessions=patient.sessions, allow_delete=current_user.is_admin) }}
#}
{% macro patient_card(patient, sessions=[], allow_delete=true) %}
    ...
{% endmacro %}
```

### Default Values

```jinja2
{# ✅ DO: Provide sensible defaults #}
{% macro alert(message, type='info', dismissible=true) %}

{# ✅ DO: Use none for optional complex objects #}
{% macro card(title=none, footer=none) %}

{# ❌ DON'T: Use mutable defaults #}
{% macro list(items=[]) %}  {# This is actually safe in Jinja2, but not in Python #}
```

---

## Testing Macros

### Macro Testing Template

```jinja2
{# test_macros.html - for visual testing #}
{% extends 'base.html' %}

{% from 'macros/buttons.html' import primary, secondary, danger %}
{% from 'macros/cards.html' import card %}
{% from 'macros/forms.html' import input_field %}

{% block main %}
    <div class="container py-4">
        <h1>Macro Test Suite</h1>
        
        <section class="mb-5">
            <h2>Buttons</h2>
            {{ primary('Primary Button') }}
            {{ secondary('Secondary Button') }}
            {{ danger('Delete') }}
        </section>
        
        <section class="mb-5">
            <h2>Cards</h2>
            {% call card(title='Test Card') %}
                <p>Card content</p>
            {% endcall %}
        </section>
        
        <section class="mb-5">
            <h2>Forms</h2>
            {{ input_field('test', 'Test Input', required=true) }}
        </section>
    </div>
{% endblock %}
```

---

## Migration Strategy

### Phase 1: Create Macro Library
1. Create `templates/macros/` directory
2. Create individual macro files (buttons, cards, forms, modals)
3. Document each macro

### Phase 2: Convert Existing Templates
1. Identify repeated patterns in current templates
2. Create macros for those patterns
3. Replace duplicated code with macro calls

### Phase 3: Refactor Templates
1. Import macros at top of templates
2. Replace inline HTML with macro calls
3. Test each page after conversion

### Phase 4: Cleanup
1. Remove unused template code
2. Standardize macro usage across all templates
3. Update documentation

---

## Checklist for Jinja2 Macros

### Organization
- [ ] Macros organized by component type
- [ ] One file per component category
- [ ] Imports at top of templates

### Documentation
- [ ] Each macro has comment block
- [ ] Parameters documented with types
- [ ] Usage examples provided

### Parameters
- [ ] Required parameters first
- [ ] Optional parameters have defaults
- [ ] Parameter names are descriptive

### Accessibility
- [ ] ARIA labels included
- [ ] Required field indicators
- [ ] Error message associations

### Consistency
- [ ] Naming convention followed
- [ ] CSS classes match BEM
- [ ] Bootstrap classes used correctly

---

## Related Skills

- [skill-template-patterns.md](./skill-template-patterns.md) - Template inheritance
- [skill-html-semantics.md](./skill-html-semantics.md) - Semantic HTML
- [skill-component-design.md](./skill-component-design.md) - Component patterns

---

*Last Updated: January 15, 2026*
