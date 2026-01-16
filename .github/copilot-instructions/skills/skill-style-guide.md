# Skill: Style Guide Creation

> **Scope:** Creating and maintaining living style guides and design system documentation for Flask/Jinja2 web applications.

---

## 1. Style Guide Overview

### What is a Living Style Guide?

A living style guide is documentation that is automatically generated from or synchronized with the actual codebase, ensuring it always reflects the current state of the design system.

### Style Guide Components

```
style-guide/
├── design-tokens/          # Colors, typography, spacing
│   ├── colors.html
│   ├── typography.html
│   └── spacing.html
├── components/             # UI component examples
│   ├── buttons.html
│   ├── cards.html
│   ├── forms.html
│   └── modals.html
├── patterns/               # Common UI patterns
│   ├── navigation.html
│   ├── data-display.html
│   └── feedback.html
├── layouts/                # Page layout templates
│   ├── dashboard.html
│   └── forms.html
└── guidelines/             # Usage guidelines
    ├── accessibility.html
    ├── responsive.html
    └── theming.html
```

---

## 2. Design Tokens Documentation

### Color Palette Page

```html
<!-- templates/style-guide/colors.html -->

{% extends 'style-guide/base.html' %}

{% block title %}Colores - Guía de Estilos{% endblock %}

{% block content %}
<main class="sg-content">
    <h1>Paleta de Colores</h1>
    <p class="sg-intro">
        Sistema de colores de la aplicación. Usa las variables CSS 
        para mantener consistencia en toda la interfaz.
    </p>
    
    <!-- Brand Colors -->
    <section class="sg-section">
        <h2>Colores de Marca</h2>
        <div class="sg-color-grid">
            {{ color_swatch('--mlc-teal', '#3F4A49', 'Teal Principal', 
                'Botones primarios, enlaces, estados activos') }}
            {{ color_swatch('--mlc-beige', '#DCD9D0', 'Beige', 
                'Bordes, divisores, fondos sutiles') }}
            {{ color_swatch('--mlc-cream', '#F5F3EF', 'Crema', 
                'Fondo de página en modo claro') }}
        </div>
    </section>
    
    <!-- Semantic Colors -->
    <section class="sg-section">
        <h2>Colores Semánticos</h2>
        <div class="sg-color-grid">
            {{ color_swatch('--color-success', '#198754', 'Éxito', 
                'Confirmaciones, acciones completadas') }}
            {{ color_swatch('--color-warning', '#ffc107', 'Advertencia', 
                'Alertas, pagos pendientes') }}
            {{ color_swatch('--color-danger', '#dc3545', 'Error', 
                'Errores, acciones destructivas') }}
            {{ color_swatch('--color-info', '#0dcaf0', 'Información', 
                'Mensajes informativos') }}
        </div>
    </section>
    
    <!-- Theme Colors -->
    <section class="sg-section">
        <h2>Colores por Tema</h2>
        
        <div class="sg-theme-demo">
            <div class="sg-theme-panel" data-theme="dark">
                <h3>Modo Oscuro (default)</h3>
                <div class="sg-color-grid">
                    {{ color_swatch('--bg-body', '#1a1d1f', 'Fondo') }}
                    {{ color_swatch('--text-primary', '#e5e5e5', 'Texto') }}
                    {{ color_swatch('--bg-card', '#212529', 'Tarjetas') }}
                </div>
            </div>
            
            <div class="sg-theme-panel" data-theme="light">
                <h3>Modo Claro</h3>
                <div class="sg-color-grid">
                    {{ color_swatch('--bg-body', '#F5F3EF', 'Fondo') }}
                    {{ color_swatch('--text-primary', '#3F4A49', 'Texto') }}
                    {{ color_swatch('--bg-card', '#ffffff', 'Tarjetas') }}
                </div>
            </div>
        </div>
    </section>
    
    <!-- Usage Examples -->
    <section class="sg-section">
        <h2>Uso en Código</h2>
        <div class="sg-code-example">
            <pre><code class="language-css">/* Usar variables CSS para colores */
.my-component {
    background-color: var(--bg-card);
    color: var(--text-primary);
    border: 1px solid var(--mlc-beige);
}

/* Para colores de estado */
.alert--success {
    background-color: var(--color-success);
}

/* NUNCA usar colores hardcodeados */
/* ❌ */ color: #3F4A49;
/* ✅ */ color: var(--mlc-teal);</code></pre>
        </div>
    </section>
</main>

{% macro color_swatch(variable, hex, name, description='') %}
<div class="sg-color-swatch">
    <div class="sg-color-preview" style="background-color: {{ hex }};"></div>
    <div class="sg-color-info">
        <strong>{{ name }}</strong>
        <code>{{ variable }}</code>
        <span class="sg-color-hex">{{ hex }}</span>
        {% if description %}
        <p class="sg-color-desc">{{ description }}</p>
        {% endif %}
    </div>
</div>
{% endmacro %}
{% endblock %}
```

### Typography Page

```html
<!-- templates/style-guide/typography.html -->

{% extends 'style-guide/base.html' %}

{% block content %}
<main class="sg-content">
    <h1>Tipografía</h1>
    
    <!-- Font Family -->
    <section class="sg-section">
        <h2>Familia Tipográfica</h2>
        <div class="sg-type-specimen">
            <p class="sg-font-name">Inter Variable</p>
            <p class="sg-font-sample">
                ABCDEFGHIJKLMNÑOPQRSTUVWXYZ<br>
                abcdefghijklmnñopqrstuvwxyz<br>
                0123456789 !@#$%^&*()
            </p>
            <code>font-family: var(--font-family-sans);</code>
        </div>
    </section>
    
    <!-- Type Scale -->
    <section class="sg-section">
        <h2>Escala Tipográfica</h2>
        <p>Basada en una escala de 1.25 (Major Third) con base de 16px.</p>
        
        <table class="sg-type-scale">
            <thead>
                <tr>
                    <th>Variable</th>
                    <th>Tamaño</th>
                    <th>Uso</th>
                    <th>Ejemplo</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>--font-size-4xl</code></td>
                    <td>2.25rem (36px)</td>
                    <td>Títulos h1</td>
                    <td style="font-size: 2.25rem;">Título Principal</td>
                </tr>
                <tr>
                    <td><code>--font-size-3xl</code></td>
                    <td>1.875rem (30px)</td>
                    <td>Títulos h2</td>
                    <td style="font-size: 1.875rem;">Subtítulo</td>
                </tr>
                <tr>
                    <td><code>--font-size-2xl</code></td>
                    <td>1.5rem (24px)</td>
                    <td>Títulos h3</td>
                    <td style="font-size: 1.5rem;">Sección</td>
                </tr>
                <tr>
                    <td><code>--font-size-xl</code></td>
                    <td>1.25rem (20px)</td>
                    <td>Títulos h4</td>
                    <td style="font-size: 1.25rem;">Subsección</td>
                </tr>
                <tr>
                    <td><code>--font-size-lg</code></td>
                    <td>1.125rem (18px)</td>
                    <td>Texto destacado</td>
                    <td style="font-size: 1.125rem;">Texto grande</td>
                </tr>
                <tr>
                    <td><code>--font-size-base</code></td>
                    <td>1rem (16px)</td>
                    <td>Texto normal</td>
                    <td style="font-size: 1rem;">Texto base</td>
                </tr>
                <tr>
                    <td><code>--font-size-sm</code></td>
                    <td>0.875rem (14px)</td>
                    <td>Texto pequeño</td>
                    <td style="font-size: 0.875rem;">Etiquetas, ayuda</td>
                </tr>
                <tr>
                    <td><code>--font-size-xs</code></td>
                    <td>0.75rem (12px)</td>
                    <td>Texto muy pequeño</td>
                    <td style="font-size: 0.75rem;">Badges, captions</td>
                </tr>
            </tbody>
        </table>
        
        <div class="sg-note sg-note--warning">
            <strong>Accesibilidad:</strong> El tamaño mínimo de texto debe ser 
            14px (0.875rem) para cumplir WCAG 2.1 AA.
        </div>
    </section>
    
    <!-- Headings -->
    <section class="sg-section">
        <h2>Encabezados</h2>
        <div class="sg-heading-examples">
            <h1>Encabezado h1 - Título de página</h1>
            <h2>Encabezado h2 - Sección principal</h2>
            <h3>Encabezado h3 - Subsección</h3>
            <h4>Encabezado h4 - Apartado</h4>
            <h5>Encabezado h5 - Subapartado</h5>
            <h6>Encabezado h6 - Detalle</h6>
        </div>
    </section>
</main>
{% endblock %}
```

### Spacing Page

```html
<!-- templates/style-guide/spacing.html -->

{% extends 'style-guide/base.html' %}

{% block content %}
<main class="sg-content">
    <h1>Espaciado</h1>
    
    <section class="sg-section">
        <h2>Escala de Espaciado</h2>
        <p>Basada en una unidad de 4px (0.25rem) para consistencia visual.</p>
        
        <div class="sg-spacing-scale">
            {% set spacings = [
                ('--spacing-1', '0.25rem', '4px'),
                ('--spacing-2', '0.5rem', '8px'),
                ('--spacing-3', '0.75rem', '12px'),
                ('--spacing-4', '1rem', '16px'),
                ('--spacing-5', '1.25rem', '20px'),
                ('--spacing-6', '1.5rem', '24px'),
                ('--spacing-8', '2rem', '32px'),
                ('--spacing-10', '2.5rem', '40px'),
                ('--spacing-12', '3rem', '48px'),
            ] %}
            
            {% for name, rem, px in spacings %}
            <div class="sg-spacing-item">
                <div class="sg-spacing-visual" style="width: {{ rem }}; height: {{ rem }};"></div>
                <div class="sg-spacing-info">
                    <code>{{ name }}</code>
                    <span>{{ rem }} ({{ px }})</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    
    <section class="sg-section">
        <h2>Uso Recomendado</h2>
        <table class="sg-table">
            <thead>
                <tr>
                    <th>Contexto</th>
                    <th>Variable</th>
                    <th>Ejemplo</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Dentro de componentes</td>
                    <td><code>--spacing-2</code> a <code>--spacing-4</code></td>
                    <td>Padding de botones, espaciado de íconos</td>
                </tr>
                <tr>
                    <td>Entre elementos relacionados</td>
                    <td><code>--spacing-4</code> a <code>--spacing-6</code></td>
                    <td>Gap en grids, margen entre campos</td>
                </tr>
                <tr>
                    <td>Entre secciones</td>
                    <td><code>--spacing-8</code> a <code>--spacing-12</code></td>
                    <td>Separación de secciones de página</td>
                </tr>
            </tbody>
        </table>
    </section>
</main>
{% endblock %}
```

---

## 3. Component Documentation

### Button Component Page

```html
<!-- templates/style-guide/components/buttons.html -->

{% extends 'style-guide/base.html' %}
{% from 'macros/_buttons.html' import button %}

{% block content %}
<main class="sg-content">
    <h1>Botones</h1>
    <p class="sg-intro">
        Componentes interactivos para acciones del usuario.
        Todos los botones cumplen con el tamaño mínimo de 44x44px 
        para accesibilidad táctil.
    </p>
    
    <!-- Variants -->
    <section class="sg-section">
        <h2>Variantes</h2>
        
        <div class="sg-component-demo">
            <div class="sg-demo-preview">
                {{ button(text='Principal', variant='primary') }}
                {{ button(text='Secundario', variant='secondary') }}
                {{ button(text='Éxito', variant='success') }}
                {{ button(text='Advertencia', variant='warning') }}
                {{ button(text='Peligro', variant='danger') }}
                {{ button(text='Enlace', variant='link') }}
            </div>
            
            <div class="sg-demo-code">
                <pre><code class="language-jinja2">{% raw %}{% from 'macros/_buttons.html' import button %}

{{ button(text='Principal', variant='primary') }}
{{ button(text='Secundario', variant='secondary') }}
{{ button(text='Éxito', variant='success') }}
{{ button(text='Advertencia', variant='warning') }}
{{ button(text='Peligro', variant='danger') }}
{{ button(text='Enlace', variant='link') }}{% endraw %}</code></pre>
            </div>
        </div>
    </section>
    
    <!-- Sizes -->
    <section class="sg-section">
        <h2>Tamaños</h2>
        
        <div class="sg-component-demo">
            <div class="sg-demo-preview">
                {{ button(text='Pequeño', size='sm') }}
                {{ button(text='Normal', size='md') }}
                {{ button(text='Grande', size='lg') }}
            </div>
            
            <div class="sg-demo-code">
                <pre><code class="language-jinja2">{% raw %}{{ button(text='Pequeño', size='sm') }}
{{ button(text='Normal', size='md') }}
{{ button(text='Grande', size='lg') }}{% endraw %}</code></pre>
            </div>
        </div>
    </section>
    
    <!-- With Icons -->
    <section class="sg-section">
        <h2>Con Íconos</h2>
        
        <div class="sg-component-demo">
            <div class="sg-demo-preview">
                {{ button(text='Guardar', icon='check', variant='success') }}
                {{ button(text='Eliminar', icon='trash', variant='danger') }}
                {{ button(text='Siguiente', icon='arrow-right', icon_position='end') }}
            </div>
            
            <div class="sg-demo-code">
                <pre><code class="language-jinja2">{% raw %}{{ button(text='Guardar', icon='check', variant='success') }}
{{ button(text='Eliminar', icon='trash', variant='danger') }}
{{ button(text='Siguiente', icon='arrow-right', icon_position='end') }}{% endraw %}</code></pre>
            </div>
        </div>
    </section>
    
    <!-- States -->
    <section class="sg-section">
        <h2>Estados</h2>
        
        <div class="sg-component-demo">
            <div class="sg-demo-preview">
                {{ button(text='Normal') }}
                {{ button(text='Deshabilitado', disabled=true) }}
                {{ button(text='Cargando...', loading=true) }}
            </div>
        </div>
        
        <div class="sg-states-table">
            <table class="sg-table">
                <thead>
                    <tr>
                        <th>Estado</th>
                        <th>Descripción</th>
                        <th>Uso</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>:hover</td>
                        <td>Cursor sobre el botón</td>
                        <td>Oscurece fondo 10%</td>
                    </tr>
                    <tr>
                        <td>:focus-visible</td>
                        <td>Foco por teclado</td>
                        <td>Outline de 2px offset 2px</td>
                    </tr>
                    <tr>
                        <td>:active</td>
                        <td>Click activo</td>
                        <td>Oscurece fondo 15%</td>
                    </tr>
                    <tr>
                        <td>:disabled</td>
                        <td>No interactivo</td>
                        <td>Opacity 0.65, cursor not-allowed</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
    
    <!-- API Reference -->
    <section class="sg-section">
        <h2>Referencia API</h2>
        
        <table class="sg-table sg-api-table">
            <thead>
                <tr>
                    <th>Parámetro</th>
                    <th>Tipo</th>
                    <th>Default</th>
                    <th>Descripción</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>text</code></td>
                    <td>string</td>
                    <td><em>requerido</em></td>
                    <td>Texto del botón</td>
                </tr>
                <tr>
                    <td><code>variant</code></td>
                    <td>'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'link'</td>
                    <td>'primary'</td>
                    <td>Estilo visual del botón</td>
                </tr>
                <tr>
                    <td><code>size</code></td>
                    <td>'sm' | 'md' | 'lg'</td>
                    <td>'md'</td>
                    <td>Tamaño del botón</td>
                </tr>
                <tr>
                    <td><code>type</code></td>
                    <td>'button' | 'submit' | 'reset'</td>
                    <td>'button'</td>
                    <td>Tipo HTML del botón</td>
                </tr>
                <tr>
                    <td><code>icon</code></td>
                    <td>string</td>
                    <td>none</td>
                    <td>Nombre del ícono Bootstrap (sin prefijo bi-)</td>
                </tr>
                <tr>
                    <td><code>icon_position</code></td>
                    <td>'start' | 'end'</td>
                    <td>'start'</td>
                    <td>Posición del ícono</td>
                </tr>
                <tr>
                    <td><code>disabled</code></td>
                    <td>boolean</td>
                    <td>false</td>
                    <td>Deshabilitar botón</td>
                </tr>
                <tr>
                    <td><code>loading</code></td>
                    <td>boolean</td>
                    <td>false</td>
                    <td>Mostrar spinner de carga</td>
                </tr>
                <tr>
                    <td><code>full_width</code></td>
                    <td>boolean</td>
                    <td>false</td>
                    <td>Botón ancho completo</td>
                </tr>
            </tbody>
        </table>
    </section>
    
    <!-- Accessibility -->
    <section class="sg-section">
        <h2>Accesibilidad</h2>
        
        <ul class="sg-a11y-list">
            <li>
                <strong>Tamaño mínimo:</strong> 44x44px para objetivos táctiles
            </li>
            <li>
                <strong>Contraste:</strong> Ratio mínimo 4.5:1 entre texto y fondo
            </li>
            <li>
                <strong>Focus visible:</strong> Outline claramente visible al navegar con teclado
            </li>
            <li>
                <strong>Estados:</strong> aria-disabled="true" cuando está deshabilitado
            </li>
            <li>
                <strong>Carga:</strong> role="status" y aria-busy="true" durante loading
            </li>
        </ul>
    </section>
</main>
{% endblock %}
```

---

## 4. Pattern Library

### Form Patterns

```html
<!-- templates/style-guide/patterns/forms.html -->

{% extends 'style-guide/base.html' %}

{% block content %}
<main class="sg-content">
    <h1>Patrones de Formularios</h1>
    
    <!-- Basic Form -->
    <section class="sg-section">
        <h2>Formulario Básico</h2>
        <p>Estructura estándar para formularios con validación.</p>
        
        <div class="sg-pattern-demo">
            <form class="sg-demo-form" novalidate>
                <div class="mb-3">
                    <label for="name" class="form-label">
                        Nombre <span class="text-danger">*</span>
                    </label>
                    <input type="text" 
                           class="form-control" 
                           id="name" 
                           required
                           aria-describedby="name-help">
                    <div id="name-help" class="form-text">
                        Nombre completo del paciente
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" 
                           class="form-control" 
                           id="email"
                           placeholder="ejemplo@correo.com">
                </div>
                
                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-primary">
                        Guardar
                    </button>
                    <button type="button" class="btn btn-secondary">
                        Cancelar
                    </button>
                </div>
            </form>
        </div>
        
        <div class="sg-guidelines">
            <h3>Guías de Uso</h3>
            <ul>
                <li>Marcar campos requeridos con asterisco rojo</li>
                <li>Usar <code>aria-describedby</code> para texto de ayuda</li>
                <li>Botón primario (submit) primero, secundario después</li>
                <li>Incluir botón de cancelar para formularios modales</li>
            </ul>
        </div>
    </section>
    
    <!-- Validation States -->
    <section class="sg-section">
        <h2>Estados de Validación</h2>
        
        <div class="sg-pattern-demo">
            <!-- Valid -->
            <div class="mb-3">
                <label class="form-label">Campo Válido</label>
                <input type="text" 
                       class="form-control is-valid" 
                       value="Valor correcto">
                <div class="valid-feedback">
                    ¡Se ve bien!
                </div>
            </div>
            
            <!-- Invalid -->
            <div class="mb-3">
                <label class="form-label">Campo Inválido</label>
                <input type="text" 
                       class="form-control is-invalid" 
                       value=""
                       aria-invalid="true"
                       aria-describedby="error-msg">
                <div id="error-msg" class="invalid-feedback">
                    Este campo es requerido.
                </div>
            </div>
        </div>
    </section>
    
    <!-- Inline Form -->
    <section class="sg-section">
        <h2>Formulario Inline</h2>
        <p>Para filtros y búsquedas en una sola línea.</p>
        
        <div class="sg-pattern-demo">
            <form class="row g-3 align-items-center">
                <div class="col-auto">
                    <label for="search" class="visually-hidden">Buscar</label>
                    <input type="text" 
                           class="form-control" 
                           id="search" 
                           placeholder="Buscar paciente...">
                </div>
                <div class="col-auto">
                    <select class="form-select" aria-label="Filtrar por estado">
                        <option value="">Todos</option>
                        <option value="active">Activos</option>
                        <option value="inactive">Inactivos</option>
                    </select>
                </div>
                <div class="col-auto">
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-search" aria-hidden="true"></i>
                        Buscar
                    </button>
                </div>
            </form>
        </div>
    </section>
</main>
{% endblock %}
```

---

## 5. Interactive Style Guide

### Theme Switcher Demo

```html
<!-- templates/style-guide/theming.html -->

{% extends 'style-guide/base.html' %}

{% block content %}
<main class="sg-content">
    <h1>Sistema de Temas</h1>
    
    <section class="sg-section">
        <h2>Cambio de Tema</h2>
        <p>
            La aplicación soporta modo oscuro (default) y modo claro.
            El tema se persiste en localStorage.
        </p>
        
        <div class="sg-theme-toggle-demo">
            <button class="btn btn-outline-secondary" 
                    onclick="toggleThemeDemo()">
                <i class="bi bi-sun-moon"></i>
                Alternar Tema
            </button>
            
            <span class="sg-current-theme">
                Tema actual: <strong id="current-theme-display">dark</strong>
            </span>
        </div>
    </section>
    
    <section class="sg-section">
        <h2>Variables por Tema</h2>
        
        <div class="sg-theme-comparison">
            <!-- Dark Theme Panel -->
            <div class="sg-theme-panel" data-bs-theme="dark">
                <h3>Modo Oscuro</h3>
                <div class="sg-sample-card">
                    <div class="card">
                        <div class="card-header">Encabezado</div>
                        <div class="card-body">
                            <p>Contenido de ejemplo en modo oscuro.</p>
                            <button class="btn btn-primary">Acción</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Light Theme Panel -->
            <div class="sg-theme-panel" data-bs-theme="light">
                <h3>Modo Claro</h3>
                <div class="sg-sample-card">
                    <div class="card">
                        <div class="card-header">Encabezado</div>
                        <div class="card-body">
                            <p>Contenido de ejemplo en modo claro.</p>
                            <button class="btn btn-primary">Acción</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="sg-section">
        <h2>Implementación</h2>
        
        <h3>HTML</h3>
        <pre><code class="language-html">&lt;html data-bs-theme="dark"&gt;
  ...
&lt;/html&gt;</code></pre>
        
        <h3>CSS</h3>
        <pre><code class="language-css">/* Variables base (modo oscuro) */
:root {
    --bg-body: #1a1d1f;
    --text-primary: #e5e5e5;
}

/* Override para modo claro */
[data-bs-theme="light"] {
    --bg-body: #F5F3EF;
    --text-primary: #3F4A49;
}</code></pre>
        
        <h3>JavaScript</h3>
        <pre><code class="language-javascript">// Alternar tema
function toggleTheme() {
    const html = document.documentElement;
    const current = html.dataset.bsTheme;
    const next = current === 'dark' ? 'light' : 'dark';
    
    html.dataset.bsTheme = next;
    localStorage.setItem('theme', next);
}

// Cargar tema guardado
function loadSavedTheme() {
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.dataset.bsTheme = saved;
    }
}</code></pre>
    </section>
</main>

<script>
function toggleThemeDemo() {
    const html = document.documentElement;
    const current = html.dataset.bsTheme;
    const next = current === 'dark' ? 'light' : 'dark';
    html.dataset.bsTheme = next;
    document.getElementById('current-theme-display').textContent = next;
}
</script>
{% endblock %}
```

---

## 6. Style Guide CSS

```css
/* static/css/style-guide.css */

/**
 * Style Guide Styles
 * 
 * Styles specific to the style guide pages.
 * Uses BEM naming and design tokens from main styles.
 */

/* ==========================================================================
   Layout
   ========================================================================== */

.sg-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-8) var(--spacing-4);
}

.sg-intro {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-8);
}

.sg-section {
    margin-bottom: var(--spacing-12);
    padding-bottom: var(--spacing-8);
    border-bottom: 1px solid var(--border-color);
}

.sg-section:last-child {
    border-bottom: none;
}

/* ==========================================================================
   Color Swatches
   ========================================================================== */

.sg-color-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: var(--spacing-4);
}

.sg-color-swatch {
    background: var(--bg-card);
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.sg-color-preview {
    height: 80px;
}

.sg-color-info {
    padding: var(--spacing-3);
}

.sg-color-info strong {
    display: block;
    margin-bottom: var(--spacing-1);
}

.sg-color-info code {
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

.sg-color-hex {
    display: block;
    font-family: var(--font-family-mono);
    font-size: var(--font-size-xs);
    color: var(--text-muted);
}

.sg-color-desc {
    margin-top: var(--spacing-2);
    font-size: var(--font-size-sm);
    color: var(--text-secondary);
}

/* ==========================================================================
   Component Demos
   ========================================================================== */

.sg-component-demo {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.sg-demo-preview {
    padding: var(--spacing-6);
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-3);
    align-items: center;
}

.sg-demo-code {
    background: var(--bg-code);
    padding: var(--spacing-4);
    border-top: 1px solid var(--border-color);
    overflow-x: auto;
}

.sg-demo-code pre {
    margin: 0;
}

/* ==========================================================================
   Tables
   ========================================================================== */

.sg-table {
    width: 100%;
    border-collapse: collapse;
}

.sg-table th,
.sg-table td {
    padding: var(--spacing-3);
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.sg-table th {
    font-weight: var(--font-weight-semibold);
    background: var(--bg-subtle);
}

.sg-api-table code {
    background: var(--bg-code);
    padding: var(--spacing-1) var(--spacing-2);
    border-radius: var(--radius-sm);
    font-size: var(--font-size-sm);
}

/* ==========================================================================
   Notes & Guidelines
   ========================================================================== */

.sg-note {
    padding: var(--spacing-4);
    border-radius: var(--radius-md);
    margin: var(--spacing-4) 0;
}

.sg-note--warning {
    background: rgba(var(--color-warning-rgb), 0.1);
    border-left: 4px solid var(--color-warning);
}

.sg-note--info {
    background: rgba(var(--color-info-rgb), 0.1);
    border-left: 4px solid var(--color-info);
}

.sg-guidelines ul {
    padding-left: var(--spacing-5);
}

.sg-guidelines li {
    margin-bottom: var(--spacing-2);
}

/* ==========================================================================
   Theme Panels
   ========================================================================== */

.sg-theme-comparison {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-4);
}

.sg-theme-panel {
    padding: var(--spacing-4);
    border-radius: var(--radius-lg);
}

.sg-theme-panel[data-bs-theme="dark"] {
    background: #1a1d1f;
    color: #e5e5e5;
}

.sg-theme-panel[data-bs-theme="light"] {
    background: #F5F3EF;
    color: #3F4A49;
}

/* ==========================================================================
   Responsive
   ========================================================================== */

@media (max-width: 768px) {
    .sg-theme-comparison {
        grid-template-columns: 1fr;
    }
    
    .sg-color-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

---

## 7. Style Guide Navigation

```html
<!-- templates/style-guide/base.html -->

<!DOCTYPE html>
<html lang="es" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Guía de Estilos{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style-guide.css') }}">
</head>
<body>
    <div class="sg-layout">
        <aside class="sg-sidebar">
            <div class="sg-logo">
                <a href="{{ url_for('style_guide.index') }}">
                    Guía de Estilos
                </a>
            </div>
            
            <nav class="sg-nav">
                <h3>Fundamentos</h3>
                <ul>
                    <li><a href="{{ url_for('style_guide.colors') }}">Colores</a></li>
                    <li><a href="{{ url_for('style_guide.typography') }}">Tipografía</a></li>
                    <li><a href="{{ url_for('style_guide.spacing') }}">Espaciado</a></li>
                    <li><a href="{{ url_for('style_guide.icons') }}">Íconos</a></li>
                </ul>
                
                <h3>Componentes</h3>
                <ul>
                    <li><a href="{{ url_for('style_guide.buttons') }}">Botones</a></li>
                    <li><a href="{{ url_for('style_guide.cards') }}">Tarjetas</a></li>
                    <li><a href="{{ url_for('style_guide.forms') }}">Formularios</a></li>
                    <li><a href="{{ url_for('style_guide.modals') }}">Modales</a></li>
                    <li><a href="{{ url_for('style_guide.alerts') }}">Alertas</a></li>
                    <li><a href="{{ url_for('style_guide.badges') }}">Badges</a></li>
                </ul>
                
                <h3>Patrones</h3>
                <ul>
                    <li><a href="{{ url_for('style_guide.navigation') }}">Navegación</a></li>
                    <li><a href="{{ url_for('style_guide.data_display') }}">Datos</a></li>
                    <li><a href="{{ url_for('style_guide.feedback') }}">Feedback</a></li>
                </ul>
                
                <h3>Guías</h3>
                <ul>
                    <li><a href="{{ url_for('style_guide.accessibility') }}">Accesibilidad</a></li>
                    <li><a href="{{ url_for('style_guide.theming') }}">Temas</a></li>
                    <li><a href="{{ url_for('style_guide.responsive') }}">Responsive</a></li>
                </ul>
            </nav>
        </aside>
        
        <div class="sg-main">
            {% block content %}{% endblock %}
        </div>
    </div>
    
    <script src="{{ url_for('static', filename='js/main.js') }}" type="module"></script>
</body>
</html>
```

---

## 8. Style Guide Flask Blueprint

```python
# app/routes/style_guide.py

from flask import Blueprint, render_template

bp = Blueprint('style_guide', __name__, url_prefix='/style-guide')


@bp.route('/')
def index():
    """Style guide home page."""
    return render_template('style-guide/index.html')


@bp.route('/colors')
def colors():
    """Color palette documentation."""
    return render_template('style-guide/colors.html')


@bp.route('/typography')
def typography():
    """Typography documentation."""
    return render_template('style-guide/typography.html')


@bp.route('/spacing')
def spacing():
    """Spacing scale documentation."""
    return render_template('style-guide/spacing.html')


@bp.route('/components/buttons')
def buttons():
    """Button component documentation."""
    return render_template('style-guide/components/buttons.html')


@bp.route('/components/cards')
def cards():
    """Card component documentation."""
    return render_template('style-guide/components/cards.html')


@bp.route('/components/forms')
def forms():
    """Form component documentation."""
    return render_template('style-guide/components/forms.html')


@bp.route('/theming')
def theming():
    """Theme system documentation."""
    return render_template('style-guide/theming.html')


@bp.route('/accessibility')
def accessibility():
    """Accessibility guidelines."""
    return render_template('style-guide/accessibility.html')
```

---

## 9. Style Guide Checklist

### Design Tokens
- [ ] Color palette documented with usage guidelines
- [ ] Typography scale with examples
- [ ] Spacing scale with use cases
- [ ] Border radii and shadows
- [ ] Theme variables for dark/light modes

### Components
- [ ] All components have live demos
- [ ] Variants and states shown
- [ ] API/props reference table
- [ ] Code examples (copy-paste ready)
- [ ] Accessibility notes

### Patterns
- [ ] Common UI patterns documented
- [ ] Form patterns with validation
- [ ] Layout patterns
- [ ] Navigation patterns

### Guidelines
- [ ] Accessibility requirements
- [ ] Responsive design rules
- [ ] Theme implementation
- [ ] Best practices and anti-patterns

### Maintenance
- [ ] Style guide uses same CSS as app
- [ ] Components are imported from macros
- [ ] Regular review schedule
- [ ] Versioned with changelog

---

## Related Skills

- [Documentation](skill-documentation.md)
- [Component Design](skill-component-design.md)
- [CSS Architecture](skill-css-architecture.md)
- [WCAG Accessibility](skill-wcag-accessibility.md)
