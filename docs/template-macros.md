# Template Macros Documentation

This document describes the Jinja2 template macros for the Therapy Session Management Application.

## Architecture Overview

Templates use a component-based architecture with reusable macros:

```
templates/
├── base.html                 # Base template
├── macros/                   # Reusable macros
│   ├── _forms.html          # Form input macros
│   ├── _cards.html          # Card component macros
│   ├── _modals.html         # Modal dialog macros
│   └── _buttons.html        # Button macros
├── partials/                 # Partial templates
│   ├── _navbar.html         # Navigation bar
│   ├── _footer.html         # Page footer
│   └── _flash_messages.html # Flash message alerts
└── errors/
    └── _error_page.html     # Shared error page macro
```

---

## Form Macros (`macros/_forms.html`)

### Importing

```jinja2
{% from 'macros/_forms.html' import text_input, password_input, select_input %}
```

### `text_input`

Render a text input field with label and error handling.

```jinja2
{{ text_input(form.name, 
    label='Nombre completo', 
    icon='person', 
    placeholder='Ingresa el nombre',
    required=true) }}
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `field` | WTForms Field | - | Form field object |
| `label` | string | `None` | Override label text |
| `icon` | string | `None` | Bootstrap icon name (without `bi-` prefix) |
| `placeholder` | string | `''` | Placeholder text |
| `autocomplete` | string | `None` | Autocomplete attribute |
| `extra_classes` | string | `''` | Additional CSS classes |
| `required` | bool | `false` | Show required indicator |
| `maxlength` | int | `None` | Maximum character length |

### `password_input`

Render a password input field with lock icon.

```jinja2
{{ password_input(form.password, 
    label='Contraseña',
    autocomplete='current-password',
    required=true,
    help_text='Mínimo 8 caracteres') }}
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `field` | WTForms Field | - | Form field object |
| `label` | string | `None` | Override label text |
| `autocomplete` | string | `'current-password'` | Autocomplete value |
| `required` | bool | `false` | Show required indicator |
| `help_text` | string | `None` | Help text below input |

### `confirm_password_input`

Render a confirm password field.

```jinja2
{{ confirm_password_input(form.confirm_password, required=true) }}
```

### `email_input`

Render an email input field with envelope icon.

```jinja2
{{ email_input(form.email, 
    placeholder='tu@email.com',
    required=true) }}
```

### `select_input`

Render a select dropdown.

```jinja2
{{ select_input(form.patient_id, 
    label='Paciente',
    icon='person') }}
```

### `textarea_input`

Render a textarea field.

```jinja2
{{ textarea_input(form.notes, 
    label='Notas',
    rows=4,
    placeholder='Notas opcionales...') }}
```

### `date_input`

Render a date picker field.

```jinja2
{{ date_input(form.session_date, 
    label='Fecha de sesión',
    required=true) }}
```

### `number_input`

Render a number input field.

```jinja2
{{ number_input(form.price, 
    label='Precio',
    icon='currency-dollar',
    min=0,
    step='0.01',
    required=true) }}
```

### `checkbox_input`

Render a checkbox field.

```jinja2
{{ checkbox_input(form.pending, label='Pago pendiente') }}
```

---

## Card Macros (`macros/_cards.html`)

### Importing

```jinja2
{% from 'macros/_cards.html' import patient_card, session_card, auth_card %}
```

### `session_card`

Render a session card inside a carousel item.

```jinja2
{{ session_card(
    session_id=session.id,
    patient_id=patient.id,
    date='Lunes 15/01/2026',
    price='$100.00',
    pending=true) }}
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `session_id` | int | Session ID |
| `patient_id` | int | Parent patient ID |
| `date` | string | Formatted date string |
| `price` | string | Formatted price string |
| `pending` | bool | Whether payment is pending |

### `sessions_carousel`

Render a carousel with session cards.

```jinja2
{{ sessions_carousel(
    patient_id=patient.id,
    patient_name=patient.name,
    sessions=sessions_list) }}
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `patient_id` | int | Patient ID (for carousel ID) |
| `patient_name` | string | Patient name (for aria-label) |
| `sessions` | list | List of tuples: `[(id, date, price, pending), ...]` |

### `patient_card`

Render a complete patient card with sessions carousel.

```jinja2
{{ patient_card(
    patient_id=patient.id,
    patient_name=patient.name,
    sessions=sessions_list,
    allow_delete=true,
    animation_delay=0.1) }}
```

### `auth_card`

Render an authentication page card container.

```jinja2
{% call auth_card() %}
    <h2>Iniciar Sesión</h2>
    <form>...</form>
{% endcall %}
```

### `empty_state`

Render an empty state message.

```jinja2
{{ empty_state(
    icon='inbox',
    title='No hay pacientes',
    message='Agrega tu primer paciente para comenzar') }}
```

---

## Modal Macros (`macros/_modals.html`)

### Importing

```jinja2
{% from 'macros/_modals.html' import modal, confirm_modal, edit_modal %}
```

### `modal`

Render a basic modal dialog structure.

```jinja2
{% call modal('myModal', 'Modal Title', icon='pencil-square') %}
    <div class="modal-body">
        <p>Modal content here</p>
    </div>
    <div class="modal-footer">
        <button class="btn btn-primary">Save</button>
    </div>
{% endcall %}
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | string | - | Modal ID |
| `title` | string | - | Modal title |
| `icon` | string | `None` | Bootstrap icon |
| `icon_color` | string | `'text-mlc-teal'` | Icon color class |
| `size` | string | `''` | Modal size: `'sm'`, `'lg'`, `'xl'` |

### `confirm_modal`

Render a confirmation modal for delete actions.

```jinja2
{{ confirm_modal(
    id='deletePatientModal',
    title='Eliminar Paciente',
    hidden_input_id='deletePatientId',
    item_name_id='deletePatientName',
    confirm_btn_id='confirmDeletePatient',
    message='¿Estás seguro de eliminar a {name}?',
    warning='Esta acción no se puede deshacer',
    confirm_text='Eliminar') }}
```

### `edit_modal`

Render an edit form modal.

```jinja2
{{ edit_modal(
    id='editPatientModal',
    title='Editar Paciente',
    form_id='editPatientForm') }}
```

### `dashboard_modals`

Include all dashboard modals (add patient, edit patient, delete patient, etc.).

```jinja2
{{ dashboard_modals() }}
```

---

## Button Macros (`macros/_buttons.html`)

### Importing

```jinja2
{% from 'macros/_buttons.html' import submit_button, cancel_button, form_buttons %}
```

### `submit_button`

Render a primary submit button.

```jinja2
{{ submit_button('Guardar', icon='check-lg') }}
```

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `text` | string | - | Button text |
| `icon` | string | `None` | Bootstrap icon |
| `full_width` | bool | `true` | Full width button |
| `size` | string | `''` | Size: `'sm'`, `'lg'` |

### `cancel_button`

Render a cancel link styled as button.

```jinja2
{{ cancel_button(url_for('patients.index')) }}
```

### `icon_button`

Render a button with icon.

```jinja2
{{ icon_button(
    type='button',
    text='Edit',
    icon='pencil',
    variant='primary',
    outline=true,
    size='sm') }}
```

### `link_button`

Render a link styled as button.

```jinja2
{{ link_button(
    url=url_for('patients.create'),
    text='Nuevo Paciente',
    icon='plus-lg') }}
```

### `form_buttons`

Render a form button group (submit + cancel).

```jinja2
{{ form_buttons(
    submit_text='Guardar Cambios',
    submit_icon='check-lg',
    cancel_url=url_for('patients.index')) }}
```

---

## Partials

### `_navbar.html`

Navigation bar partial. Included in `base.html`.

### `_footer.html`

Page footer partial. Included in `base.html`.

### `_flash_messages.html`

Flash message alerts with proper ARIA roles.

```jinja2
{% include 'partials/_flash_messages.html' %}
```

---

## Error Page Macro

### `_error_page.html`

Shared error page macro for 403, 404, 500 pages.

```jinja2
{% from 'errors/_error_page.html' import error_page %}

{% call error_page(
    code=404,
    title='Página no encontrada',
    message='La página que buscas no existe') %}
    <a href="{{ url_for('main.index') }}">Volver al inicio</a>
{% endcall %}
```

---

## Accessibility Features

All macros include built-in accessibility:

- **ARIA Labels**: Interactive elements have descriptive labels
- **Error Announcements**: Form errors use `role="alert"`
- **Focus Management**: Modals trap focus correctly
- **Icon Decoration**: Icons use `aria-hidden="true"`
- **Required Fields**: Visual and ARIA indication

---

## Usage Examples

### Complete Login Form

```jinja2
{% from 'macros/_forms.html' import email_input, password_input %}
{% from 'macros/_buttons.html' import submit_button %}
{% from 'macros/_cards.html' import auth_card %}

{% call auth_card() %}
    <h2 class="text-center mb-4">Iniciar Sesión</h2>
    
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ email_input(form.email, placeholder='tu@email.com', required=true) }}
        {{ password_input(form.password, required=true) }}
        {{ submit_button('Ingresar', icon='box-arrow-in-right') }}
    </form>
{% endcall %}
```

### Patient Card with Sessions

```jinja2
{% from 'macros/_cards.html' import patient_card %}

{% for patient in patients %}
    {{ patient_card(
        patient_id=patient.id,
        patient_name=patient.name,
        sessions=patient.formatted_sessions,
        animation_delay=loop.index * 0.05) }}
{% endfor %}
```

---

*Last Updated: January 15, 2026*
