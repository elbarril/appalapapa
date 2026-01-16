# Skill: Jinja2 Template Patterns

> **Scope:** Template inheritance, blocks, includes, and organizational patterns for Flask/Jinja2 applications.

---

## 1. Template Inheritance Hierarchy

### Base Template Structure

```html
{# templates/base.html - Root template #}
<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    {# Title with default and override capability #}
    <title>{% block title %}{{ config.APP_NAME }}{% endblock title %}</title>
    
    {# Meta blocks for SEO/social #}
    {% block meta %}
    <meta name="description" content="{% block meta_description %}Sistema de gestión de sesiones{% endblock %}">
    {% endblock meta %}
    
    {# Core CSS - rarely overridden #}
    {% block styles_core %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
    {% endblock styles_core %}
    
    {# Additional page-specific CSS #}
    {% block styles_extra %}{% endblock styles_extra %}
</head>
<body>
    {# Skip link for accessibility #}
    <a href="#main-content" class="visually-hidden-focusable">
        Saltar al contenido principal
    </a>
    
    {# Navigation - can be hidden on specific pages #}
    {% block navigation %}
        {% include 'components/navbar.html' %}
    {% endblock navigation %}
    
    {# Flash messages - consistent placement #}
    {% block flash_messages %}
        {% include 'components/flash_messages.html' %}
    {% endblock flash_messages %}
    
    {# Main content area #}
    <main id="main-content" role="main">
        {% block main %}{% endblock main %}
    </main>
    
    {# Footer #}
    {% block footer %}
        {% include 'components/footer.html' %}
    {% endblock footer %}
    
    {# Modals container #}
    {% block modals %}{% endblock modals %}
    
    {# Core JavaScript #}
    {% block scripts_core %}
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    {% endblock scripts_core %}
    
    {# Page-specific JavaScript #}
    {% block scripts_extra %}{% endblock scripts_extra %}
</body>
</html>
```

### Naming Conventions for Blocks

| Block Name | Purpose | Override Frequency |
|------------|---------|-------------------|
| `title` | Page title | Always |
| `meta` | Meta tags container | Sometimes |
| `meta_description` | SEO description | Sometimes |
| `styles_core` | Framework CSS | Rarely |
| `styles_extra` | Page-specific CSS | Often |
| `navigation` | Header/nav | Rarely |
| `flash_messages` | Notifications | Rarely |
| `main` | Primary content | Always |
| `footer` | Footer content | Rarely |
| `modals` | Modal dialogs | Sometimes |
| `scripts_core` | Framework JS | Rarely |
| `scripts_extra` | Page-specific JS | Often |

---

## 2. Child Template Patterns

### Standard Page Template

```html
{# templates/patients/list.html #}
{% extends 'base.html' %}

{% block title %}Pacientes - {{ super() }}{% endblock title %}

{% block meta_description %}
Lista de pacientes y sesiones de terapia
{% endblock meta_description %}

{% block main %}
<div class="container py-4">
    <h1>Gestión de Pacientes</h1>
    
    {# Page content here #}
</div>
{% endblock main %}

{% block modals %}
    {% include 'patients/_modal_edit.html' %}
    {% include 'patients/_modal_delete.html' %}
{% endblock modals %}

{% block scripts_extra %}
<script src="{{ url_for('static', filename='js/api.js') }}"></script>
<script>
    // Page-specific initialization
    document.addEventListener('DOMContentLoaded', () => {
        initPatientList();
    });
</script>
{% endblock scripts_extra %}
```

### Using `super()` to Extend Blocks

```html
{# Append to parent block content #}
{% block styles_extra %}
{{ super() }}
<link rel="stylesheet" href="{{ url_for('static', filename='css/calendar.css') }}">
{% endblock styles_extra %}

{# Prepend to parent block content #}
{% block scripts_extra %}
<script src="{{ url_for('static', filename='js/chart.js') }}"></script>
{{ super() }}
{% endblock scripts_extra %}
```

---

## 3. Include Patterns

### File Naming Convention

```
templates/
├── base.html                    # Root template
├── components/                   # Reusable UI components
│   ├── navbar.html              # Main navigation
│   ├── footer.html              # Page footer
│   ├── flash_messages.html      # Alert messages
│   ├── pagination.html          # Pagination controls
│   └── loading_spinner.html     # Loading indicator
├── patients/
│   ├── list.html                # Page template
│   ├── form_person.html         # Page template
│   ├── _card.html               # Partial (underscore prefix)
│   ├── _modal_edit.html         # Modal partial
│   └── _modal_delete.html       # Modal partial
└── sessions/
    ├── form_session.html        # Page template
    └── _carousel.html           # Partial
```

**Naming Rules:**
- **Page templates:** `name.html` - Full pages that extend base
- **Partials:** `_name.html` - Fragments included in pages
- **Components:** `components/name.html` - Reusable across modules

### Basic Include

```html
{# Simple include #}
{% include 'components/footer.html' %}

{# Include with context (default behavior) #}
{% include 'patients/_card.html' %}

{# Include without parent context #}
{% include 'components/pagination.html' without context %}

{# Include with explicit context #}
{% include 'patients/_card.html' with context %}
```

### Include with Variables

```html
{# Pass variables to included template #}
{% set card_patient = patient %}
{% set show_actions = true %}
{% include 'patients/_card.html' %}

{# Or use set block for complex content #}
{% set card_footer %}
    <button class="btn btn-primary">Acción especial</button>
{% endset %}
{% include 'patients/_card.html' %}
```

### Conditional Includes

```html
{# Include based on condition #}
{% if current_user.is_authenticated %}
    {% include 'components/navbar_authenticated.html' %}
{% else %}
    {% include 'components/navbar_public.html' %}
{% endif %}

{# Include with fallback #}
{% include ['components/navbar_' ~ user_role ~ '.html', 'components/navbar_default.html'] %}
```

### Include with ignore missing

```html
{# Don't error if template doesn't exist #}
{% include 'components/optional_banner.html' ignore missing %}

{# With fallback list #}
{% include ['custom/header.html', 'components/header.html'] ignore missing %}
```

---

## 4. Partial Template Design

### Card Partial Example

```html
{# templates/patients/_card.html #}
{# 
    Required: patient (Person object)
    Optional: show_actions (bool, default: true)
              card_class (str, additional classes)
#}
{% set show_actions = show_actions | default(true) %}
{% set card_class = card_class | default('') %}

<article class="card h-100 {{ card_class }}" 
         data-patient-id="{{ patient.id }}"
         aria-labelledby="patient-name-{{ patient.id }}">
    <div class="card-header">
        <h3 id="patient-name-{{ patient.id }}" class="card-title h5 mb-0">
            {{ patient.name }}
        </h3>
    </div>
    
    <div class="card-body">
        {% if patient.notes %}
        <p class="card-text text-body-secondary">{{ patient.notes }}</p>
        {% endif %}
        
        <dl class="row mb-0">
            <dt class="col-sm-6">Sesiones:</dt>
            <dd class="col-sm-6">{{ patient.sessions | length }}</dd>
            
            <dt class="col-sm-6">Pendiente:</dt>
            <dd class="col-sm-6">{{ patient.total_pending | format_currency }}</dd>
        </dl>
    </div>
    
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
```

### Modal Partial Example

```html
{# templates/patients/_modal_delete.html #}
<div class="modal fade" 
     id="deletePatientModal" 
     tabindex="-1" 
     aria-labelledby="deletePatientModalLabel" 
     aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title h5" id="deletePatientModalLabel">
                    Confirmar eliminación
                </h2>
                <button type="button" 
                        class="btn-close" 
                        data-bs-dismiss="modal" 
                        aria-label="Cerrar"></button>
            </div>
            <div class="modal-body">
                <p>¿Está seguro de eliminar al paciente <strong id="deletePatientName"></strong>?</p>
                <p class="text-danger mb-0">
                    <i class="bi bi-exclamation-triangle" aria-hidden="true"></i>
                    Esta acción no se puede deshacer.
                </p>
            </div>
            <div class="modal-footer">
                <button type="button" 
                        class="btn btn-secondary" 
                        data-bs-dismiss="modal">
                    Cancelar
                </button>
                <button type="button" 
                        class="btn btn-danger" 
                        id="confirmDeletePatient"
                        onclick="confirmDeletePatient()">
                    <i class="bi bi-trash" aria-hidden="true"></i>
                    Eliminar
                </button>
            </div>
        </div>
    </div>
</div>
```

---

## 5. Loop Patterns

### Basic Loop with Index

```html
{% for patient in patients %}
<div class="col-md-6 col-lg-4 mb-4">
    {% include 'patients/_card.html' %}
</div>
{% else %}
<div class="col-12">
    <div class="alert alert-info" role="status">
        <i class="bi bi-info-circle" aria-hidden="true"></i>
        No hay pacientes registrados.
    </div>
</div>
{% endfor %}
```

### Loop Variables

```html
{% for session in sessions %}
<tr class="{% if loop.first %}table-active{% endif %}
           {% if loop.last %}border-bottom-0{% endif %}">
    <td>{{ loop.index }}</td>  {# 1-based index #}
    <td>{{ session.date | format_date }}</td>
    <td>{{ session.price | format_currency }}</td>
</tr>
{% endfor %}

{# Available loop variables:
   loop.index      - 1-based iteration count
   loop.index0     - 0-based iteration count  
   loop.revindex   - Reverse 1-based count
   loop.revindex0  - Reverse 0-based count
   loop.first      - True on first iteration
   loop.last       - True on last iteration
   loop.length     - Total number of items
   loop.cycle()    - Cycle through values
   loop.depth      - Nesting depth (starts at 1)
   loop.depth0     - Nesting depth (starts at 0)
   loop.previtem   - Previous item (if available)
   loop.nextitem   - Next item (if available)
   loop.changed()  - True if value changed from last iteration
#}
```

### Grouped Loops

```html
{# Group sessions by month #}
{% for month, month_sessions in sessions | groupby('month') %}
<section class="mb-4">
    <h2 class="h4">{{ month | format_month }}</h2>
    <div class="table-responsive">
        <table class="table">
            {% for session in month_sessions %}
            <tr>
                <td>{{ session.date | format_date }}</td>
                <td>{{ session.price | format_currency }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</section>
{% endfor %}
```

### Batch/Chunk Loops (Grid Layout)

```html
{# Create rows of 3 cards each #}
{% for row in patients | batch(3, '') %}
<div class="row mb-4">
    {% for patient in row %}
        {% if patient %}
        <div class="col-md-4">
            {% include 'patients/_card.html' %}
        </div>
        {% else %}
        <div class="col-md-4">
            {# Empty placeholder for grid alignment #}
        </div>
        {% endif %}
    {% endfor %}
</div>
{% endfor %}
```

---

## 6. Conditional Rendering

### Simple Conditions

```html
{# Basic if/else #}
{% if patient.sessions %}
    <span class="badge bg-success">Activo</span>
{% else %}
    <span class="badge bg-secondary">Sin sesiones</span>
{% endif %}

{# Ternary-style inline #}
<span class="badge {{ 'bg-success' if patient.active else 'bg-secondary' }}">
    {{ 'Activo' if patient.active else 'Inactivo' }}
</span>
```

### Complex Conditions

```html
{% if current_user.is_admin %}
    {% include 'components/admin_toolbar.html' %}
{% elif current_user.is_therapist %}
    {% include 'components/therapist_toolbar.html' %}
{% elif current_user.is_authenticated %}
    {% include 'components/viewer_toolbar.html' %}
{% else %}
    {% include 'components/public_toolbar.html' %}
{% endif %}
```

### Testing Values

```html
{# Check if defined #}
{% if patient is defined %}
    {{ patient.name }}
{% endif %}

{# Check if none/null #}
{% if patient.notes is not none %}
    <p>{{ patient.notes }}</p>
{% endif %}

{# Check string content #}
{% if patient.notes %}  {# Empty string is falsy #}
    <p>{{ patient.notes }}</p>
{% endif %}

{# Check collection #}
{% if patients | length > 0 %}
    {# Has items #}
{% endif %}

{# Type tests #}
{% if value is string %}...{% endif %}
{% if value is number %}...{% endif %}
{% if value is sequence %}...{% endif %}
{% if value is mapping %}...{% endif %}
{% if value is callable %}...{% endif %}
```

---

## 7. Template Fragments for AJAX

### Returning Partial HTML

```python
# In route - return only the partial for AJAX requests
@patients_bp.route('/list')
def patient_list():
    patients = PatientService.get_all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return only the list partial for AJAX
        return render_template('patients/_list.html', patients=patients)
    
    # Return full page for normal requests
    return render_template('patients/list.html', patients=patients)
```

### Fragment Template Structure

```html
{# templates/patients/_list.html - Partial for AJAX updates #}
{% for patient in patients %}
<article class="card mb-3" 
         id="patient-{{ patient.id }}"
         data-patient-id="{{ patient.id }}">
    <div class="card-body">
        <h3 class="card-title h5">{{ patient.name }}</h3>
        {# ... card content ... #}
    </div>
</article>
{% else %}
<div class="alert alert-info" role="status">
    No hay pacientes que coincidan con el filtro.
</div>
{% endfor %}
```

### JavaScript Integration

```javascript
// Fetch and replace content
async function refreshPatientList(filter = 'all') {
    const response = await fetch(`/patients/list?filter=${filter}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
    
    const html = await response.text();
    document.getElementById('patient-list-container').innerHTML = html;
}
```

---

## 8. Content Blocks Pattern

### Defining Reusable Content Blocks

```html
{# Define content block that can be reused #}
{% set page_actions %}
<div class="btn-group" role="group">
    <a href="{{ url_for('patients.add') }}" class="btn btn-primary">
        <i class="bi bi-plus-lg" aria-hidden="true"></i>
        Nuevo Paciente
    </a>
    <button type="button" class="btn btn-outline-secondary" onclick="exportData()">
        <i class="bi bi-download" aria-hidden="true"></i>
        Exportar
    </button>
</div>
{% endset %}

{# Use in multiple places #}
<header class="d-flex justify-content-between align-items-center mb-4">
    <h1>Pacientes</h1>
    {{ page_actions }}
</header>

{# ... page content ... #}

<footer class="d-flex justify-content-end mt-4">
    {{ page_actions }}
</footer>
```

### Caller Pattern for Wrapper Components

```html
{# Define a card wrapper macro that accepts content via caller #}
{% macro card_wrapper(title, id=none, class='') %}
<div class="card {{ class }}" {% if id %}id="{{ id }}"{% endif %}>
    <div class="card-header">
        <h3 class="card-title h5 mb-0">{{ title }}</h3>
    </div>
    <div class="card-body">
        {{ caller() }}
    </div>
</div>
{% endmacro %}

{# Usage with call block #}
{% call card_wrapper('Información del Paciente', id='patient-info') %}
    <dl class="row mb-0">
        <dt class="col-sm-4">Nombre:</dt>
        <dd class="col-sm-8">{{ patient.name }}</dd>
        <dt class="col-sm-4">Email:</dt>
        <dd class="col-sm-8">{{ patient.email or 'No especificado' }}</dd>
    </dl>
{% endcall %}
```

---

## 9. Error and Empty State Templates

### Standardized Empty States

```html
{# templates/components/_empty_state.html #}
{#
    Required: message (str)
    Optional: icon (str, Bootstrap icon name)
              action_url (str)
              action_text (str)
#}
{% set icon = icon | default('inbox') %}

<div class="text-center py-5" role="status">
    <i class="bi bi-{{ icon }} display-1 text-body-secondary" aria-hidden="true"></i>
    <p class="lead text-body-secondary mt-3">{{ message }}</p>
    
    {% if action_url and action_text %}
    <a href="{{ action_url }}" class="btn btn-primary mt-2">
        <i class="bi bi-plus-lg" aria-hidden="true"></i>
        {{ action_text }}
    </a>
    {% endif %}
</div>
```

### Usage

```html
{% if patients %}
    {# Display patient list #}
{% else %}
    {% set message = 'No hay pacientes registrados' %}
    {% set action_url = url_for('patients.add') %}
    {% set action_text = 'Agregar primer paciente' %}
    {% include 'components/_empty_state.html' %}
{% endif %}
```

### Error Message Template

```html
{# templates/components/_error_message.html #}
{% set type = type | default('danger') %}
{% set icon = icon | default('exclamation-triangle') %}
{% set dismissible = dismissible | default(true) %}

<div class="alert alert-{{ type }} {{ 'alert-dismissible fade show' if dismissible }}" 
     role="alert">
    <i class="bi bi-{{ icon }} me-2" aria-hidden="true"></i>
    {{ message }}
    
    {% if dismissible %}
    <button type="button" 
            class="btn-close" 
            data-bs-dismiss="alert" 
            aria-label="Cerrar"></button>
    {% endif %}
</div>
```

---

## 10. Template Organization Best Practices

### Directory Structure

```
templates/
├── base.html                     # Root layout
├── components/                    # Shared UI components
│   ├── navbar.html
│   ├── footer.html
│   ├── flash_messages.html
│   ├── pagination.html
│   ├── _empty_state.html         # Partial (underscore)
│   └── _loading.html             # Partial
├── layouts/                       # Alternative layouts
│   ├── auth.html                  # Auth pages layout
│   └── print.html                 # Print-friendly layout
├── macros/                        # Reusable macros
│   ├── forms.html                 # Form field macros
│   ├── tables.html                # Table macros
│   └── cards.html                 # Card macros
├── patients/                      # Patient module
│   ├── list.html                  # Page template
│   ├── form_person.html           # Page template
│   ├── _card.html                 # Partial
│   └── _modal_edit.html           # Modal partial
└── errors/                        # Error pages
    ├── 403.html
    ├── 404.html
    └── 500.html
```

### Import Pattern for Macros

```html
{# At top of template file #}
{% from 'macros/forms.html' import form_field, form_errors %}
{% from 'macros/cards.html' import patient_card, session_card %}

{# Usage #}
{{ form_field(form.name) }}
{{ patient_card(patient, show_actions=true) }}
```

### Template Comments

```html
{# 
    Template: patients/list.html
    Purpose: Display paginated list of patients with filters
    Context variables:
        - patients: list of Person objects
        - pagination: Pagination object
        - filter: current filter value ('all', 'pending', 'paid')
    Includes:
        - patients/_card.html (requires: patient, show_actions)
        - components/pagination.html (requires: pagination)
#}
{% extends 'base.html' %}

{# ... template content ... #}
```

---

## Quick Reference

### Block Inheritance

| Operation | Syntax | Result |
|-----------|--------|--------|
| Override | `{% block name %}new{% endblock %}` | Replaces parent |
| Extend | `{{ super() }}` | Includes parent content |
| Prepend | `content{{ super() }}` | Add before parent |
| Append | `{{ super() }}content` | Add after parent |

### Include Variations

| Syntax | Behavior |
|--------|----------|
| `{% include 'x.html' %}` | Include with context |
| `{% include 'x.html' without context %}` | No parent variables |
| `{% include 'x.html' ignore missing %}` | Don't error if missing |
| `{% include ['a.html', 'b.html'] %}` | First available |

### File Naming

| Pattern | Type | Example |
|---------|------|---------|
| `name.html` | Page template | `list.html` |
| `_name.html` | Partial | `_card.html` |
| `form_name.html` | Form page | `form_person.html` |
| `_modal_name.html` | Modal partial | `_modal_delete.html` |
