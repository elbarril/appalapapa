# Skill: Semantic HTML5

> **Scope:** Semantic HTML elements, landmark regions, document structure, and meaningful markup for accessibility and SEO.

---

## 1. Document Structure

### Complete Document Outline

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Sistema de gestión de sesiones de terapia">
    <title>Gestión de Pacientes - TherapyApp</title>
</head>
<body>
    <!-- Skip link for keyboard users -->
    <a href="#main-content" class="visually-hidden-focusable">
        Saltar al contenido principal
    </a>
    
    <!-- Site header with navigation -->
    <header role="banner">
        <nav aria-label="Navegación principal">
            <!-- Primary navigation -->
        </nav>
    </header>
    
    <!-- Flash messages / notifications -->
    <div role="status" aria-live="polite" id="notifications">
        <!-- Dynamic notifications -->
    </div>
    
    <!-- Main content area -->
    <main id="main-content">
        <!-- Page content -->
    </main>
    
    <!-- Complementary content -->
    <aside aria-label="Información adicional">
        <!-- Sidebar content -->
    </aside>
    
    <!-- Site footer -->
    <footer role="contentinfo">
        <!-- Footer content -->
    </footer>
</body>
</html>
```

### Language Declaration

```html
<!-- Primary language -->
<html lang="es">

<!-- Mixed language content -->
<html lang="es">
<body>
    <p>El sistema usa <span lang="en">cookies</span> para mejorar la experiencia.</p>
    
    <!-- Block of different language -->
    <blockquote lang="en">
        <p>The only way to do great work is to love what you do.</p>
        <footer>— Steve Jobs</footer>
    </blockquote>
</body>
</html>
```

---

## 2. Landmark Elements

### Landmark Reference

| Element | ARIA Role | Purpose | Quantity |
|---------|-----------|---------|----------|
| `<header>` | `banner` | Site/section header | One per page (banner) |
| `<nav>` | `navigation` | Navigation links | Multiple allowed |
| `<main>` | `main` | Primary content | Exactly one |
| `<article>` | `article` | Self-contained content | Multiple allowed |
| `<section>` | `region` | Thematic grouping | Multiple allowed |
| `<aside>` | `complementary` | Related content | Multiple allowed |
| `<footer>` | `contentinfo` | Site/section footer | One per page (contentinfo) |

### Header Element

```html
<!-- Site header (appears once at top) -->
<header role="banner">
    <a href="/" class="logo">
        <img src="/logo.svg" alt="TherapyApp">
    </a>
    <nav aria-label="Navegación principal">
        <!-- Navigation links -->
    </nav>
</header>

<!-- Section header (inside article/section) -->
<article>
    <header>
        <h2>Título del Artículo</h2>
        <p class="meta">
            <time datetime="2026-01-15">15 de enero, 2026</time>
        </p>
    </header>
    <!-- Article content -->
</article>
```

### Navigation Element

```html
<!-- Primary navigation -->
<nav aria-label="Navegación principal">
    <ul>
        <li><a href="/" aria-current="page">Inicio</a></li>
        <li><a href="/patients">Pacientes</a></li>
        <li><a href="/sessions">Sesiones</a></li>
    </ul>
</nav>

<!-- Secondary navigation -->
<nav aria-label="Navegación de usuario">
    <ul>
        <li><a href="/profile">Mi Perfil</a></li>
        <li><a href="/logout">Cerrar Sesión</a></li>
    </ul>
</nav>

<!-- Breadcrumb navigation -->
<nav aria-label="Ruta de navegación">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/">Inicio</a></li>
        <li class="breadcrumb-item"><a href="/patients">Pacientes</a></li>
        <li class="breadcrumb-item active" aria-current="page">Juan García</li>
    </ol>
</nav>

<!-- Pagination navigation -->
<nav aria-label="Paginación">
    <ul class="pagination">
        <li><a href="?page=1" aria-label="Página anterior">Anterior</a></li>
        <li><a href="?page=1">1</a></li>
        <li><a href="?page=2" aria-current="page">2</a></li>
        <li><a href="?page=3">3</a></li>
        <li><a href="?page=3" aria-label="Página siguiente">Siguiente</a></li>
    </ul>
</nav>
```

### Main Element

```html
<!-- Exactly one per page -->
<main id="main-content">
    <h1>Gestión de Pacientes</h1>
    
    <!-- Primary page content -->
    <section aria-labelledby="active-patients">
        <h2 id="active-patients">Pacientes Activos</h2>
        <!-- Content -->
    </section>
</main>
```

### Article Element

```html
<!-- Self-contained, independently distributable content -->
<article aria-labelledby="patient-123-title">
    <header>
        <h2 id="patient-123-title">Juan García</h2>
        <p>Paciente desde <time datetime="2025-03-15">marzo 2025</time></p>
    </header>
    
    <section aria-labelledby="patient-123-sessions">
        <h3 id="patient-123-sessions">Sesiones Recientes</h3>
        <!-- Session list -->
    </section>
    
    <footer>
        <p>Última actualización: <time datetime="2026-01-14">14/01/2026</time></p>
    </footer>
</article>

<!-- Card as article (when self-contained) -->
<article class="card" aria-labelledby="session-456-title">
    <div class="card-header">
        <h3 id="session-456-title" class="card-title">
            <time datetime="2026-01-15">Miércoles 15/01/2026</time>
        </h3>
    </div>
    <div class="card-body">
        <p>Sesión de terapia individual</p>
        <p><strong>Precio:</strong> $150.00</p>
    </div>
</article>
```

### Section Element

```html
<!-- Thematic grouping with heading -->
<section aria-labelledby="pending-payments">
    <h2 id="pending-payments">Pagos Pendientes</h2>
    
    <ul>
        <li>Juan García - $300.00</li>
        <li>María López - $150.00</li>
    </ul>
</section>

<!-- Nested sections for hierarchy -->
<section aria-labelledby="reports">
    <h2 id="reports">Reportes</h2>
    
    <section aria-labelledby="monthly-reports">
        <h3 id="monthly-reports">Reportes Mensuales</h3>
        <!-- Content -->
    </section>
    
    <section aria-labelledby="annual-reports">
        <h3 id="annual-reports">Reportes Anuales</h3>
        <!-- Content -->
    </section>
</section>
```

### Aside Element

```html
<!-- Sidebar with related content -->
<aside aria-labelledby="quick-stats">
    <h2 id="quick-stats">Estadísticas Rápidas</h2>
    <dl>
        <dt>Total Pacientes</dt>
        <dd>45</dd>
        <dt>Sesiones Este Mes</dt>
        <dd>128</dd>
    </dl>
</aside>

<!-- Inline aside (pull quote, note) -->
<article>
    <p>La terapia cognitivo-conductual es efectiva...</p>
    
    <aside aria-label="Nota importante">
        <p><strong>Nota:</strong> Los resultados pueden variar según el paciente.</p>
    </aside>
    
    <p>Continuando con el tratamiento...</p>
</article>
```

### Footer Element

```html
<!-- Site footer -->
<footer role="contentinfo">
    <nav aria-label="Enlaces del pie de página">
        <ul>
            <li><a href="/privacy">Privacidad</a></li>
            <li><a href="/terms">Términos</a></li>
            <li><a href="/contact">Contacto</a></li>
        </ul>
    </nav>
    <p><small>&copy; 2026 TherapyApp. Todos los derechos reservados.</small></p>
</footer>

<!-- Article/section footer -->
<article>
    <h2>Título del Artículo</h2>
    <p>Contenido...</p>
    
    <footer>
        <p>Autor: Dr. García</p>
        <p>Publicado: <time datetime="2026-01-15">15/01/2026</time></p>
    </footer>
</article>
```

---

## 3. Heading Hierarchy

### Proper Heading Structure

```html
<!-- Correct: Logical hierarchy -->
<main>
    <h1>Panel de Control</h1>                    <!-- Level 1: Page title -->
    
    <section>
        <h2>Pacientes Activos</h2>               <!-- Level 2: Section -->
        
        <article>
            <h3>Juan García</h3>                 <!-- Level 3: Item -->
            
            <section>
                <h4>Sesiones Recientes</h4>      <!-- Level 4: Subsection -->
            </section>
        </article>
    </section>
    
    <section>
        <h2>Pagos Pendientes</h2>                <!-- Level 2: Another section -->
    </section>
</main>

<!-- Wrong: Skipping levels -->
<main>
    <h1>Panel de Control</h1>
    <h3>Pacientes</h3>      <!-- ❌ Skipped h2 -->
    <h5>Juan García</h5>    <!-- ❌ Skipped h4 -->
</main>
```

### Visual vs. Semantic Styling

```html
<!-- Correct: Use CSS for visual styling, keep semantic hierarchy -->
<h2 class="h4">Sección Pequeña</h2>  <!-- Semantically h2, visually h4 size -->

<h3 class="display-4">Título Grande</h3>  <!-- Semantically h3, visually large -->

<!-- Wrong: Using heading level for styling -->
<h4>Main Title</h4>  <!-- ❌ Using h4 just because you want smaller text -->
```

### One H1 Per Page

```html
<!-- Correct: Single h1 for page title -->
<body>
    <header>
        <nav><!-- Logo is not h1 --></nav>
    </header>
    
    <main>
        <h1>Gestión de Pacientes</h1>  <!-- The one h1 -->
        <!-- ... -->
    </main>
</body>

<!-- Wrong: Multiple h1 elements -->
<body>
    <header>
        <h1>TherapyApp</h1>  <!-- ❌ -->
    </header>
    <main>
        <h1>Pacientes</h1>   <!-- ❌ -->
    </main>
</body>
```

---

## 4. Text Content Elements

### Paragraphs and Line Breaks

```html
<!-- Paragraph for blocks of text -->
<p>Este es un párrafo completo con una idea o tema.</p>
<p>Este es otro párrafo con información diferente.</p>

<!-- Line break only for content where breaks matter -->
<address>
    Calle Principal 123<br>
    Ciudad, CP 12345<br>
    País
</address>

<!-- Wrong: Using br for spacing -->
<p>Primer párrafo</p>
<br><br>  <!-- ❌ Use margins/padding instead -->
<p>Segundo párrafo</p>
```

### Emphasis and Importance

```html
<!-- Emphasis (stress, pronunciation) - renders italic -->
<p>Debes <em>siempre</em> confirmar la cita.</p>

<!-- Strong importance - renders bold -->
<p><strong>Advertencia:</strong> Esta acción no se puede deshacer.</p>

<!-- Nested for stronger emphasis -->
<p><strong><em>Muy importante:</em></strong> Guardar antes de salir.</p>

<!-- Wrong: Using for visual styling only -->
<p><strong>Nombre:</strong> Juan</p>  <!-- ❌ Use CSS if not important -->
```

### Quotations

```html
<!-- Block quotation -->
<blockquote cite="https://example.com/source">
    <p>La salud mental es tan importante como la salud física.</p>
    <footer>— <cite>Dr. García</cite></footer>
</blockquote>

<!-- Inline quotation -->
<p>El paciente mencionó que <q>se siente mucho mejor esta semana</q>.</p>

<!-- Citation -->
<p>Como se describe en <cite>Manual de Terapia Cognitiva</cite>...</p>
```

### Abbreviations and Definitions

```html
<!-- Abbreviation with expansion -->
<p>El <abbr title="Trastorno por Déficit de Atención e Hiperactividad">TDAH</abbr> 
   afecta a muchos pacientes.</p>

<!-- Definition -->
<p><dfn>Terapia cognitivo-conductual</dfn> es un tipo de psicoterapia 
   que ayuda a cambiar patrones de pensamiento.</p>

<!-- Definition list -->
<dl>
    <dt>TCC</dt>
    <dd>Terapia Cognitivo-Conductual</dd>
    
    <dt>EMDR</dt>
    <dd>Desensibilización y Reprocesamiento por Movimientos Oculares</dd>
</dl>
```

### Code and Technical Content

```html
<!-- Inline code -->
<p>Use <code>flask run</code> para iniciar el servidor.</p>

<!-- Keyboard input -->
<p>Presione <kbd>Ctrl</kbd> + <kbd>S</kbd> para guardar.</p>

<!-- Sample output -->
<p>El sistema mostrará: <samp>Operación completada</samp></p>

<!-- Preformatted code block -->
<pre><code>
def hello():
    print("Hola, mundo")
</code></pre>

<!-- Variable -->
<p>El valor de <var>x</var> es calculado automáticamente.</p>
```

### Time and Dates

```html
<!-- Machine-readable dates -->
<time datetime="2026-01-15">15 de enero, 2026</time>

<!-- With time -->
<time datetime="2026-01-15T14:30:00">15/01/2026 a las 14:30</time>

<!-- Duration (ISO 8601) -->
<p>Duración: <time datetime="PT1H30M">1 hora 30 minutos</time></p>

<!-- In context -->
<article>
    <h2>Sesión de Terapia</h2>
    <p>Fecha: <time datetime="2026-01-15">Miércoles 15/01/2026</time></p>
    <p>Hora: <time datetime="14:30">2:30 PM</time></p>
</article>
```

### Addresses

```html
<!-- Contact information for article/document author -->
<address>
    <a href="mailto:contacto@therapyapp.com">contacto@therapyapp.com</a><br>
    <a href="tel:+1234567890">+1 234 567 890</a>
</address>

<!-- Physical address -->
<address>
    Consultorio TherapyApp<br>
    Calle Principal 123, Oficina 456<br>
    Ciudad, Estado 12345
</address>
```

---

## 5. Lists

### Unordered Lists

```html
<!-- Navigation menu -->
<nav>
    <ul>
        <li><a href="/">Inicio</a></li>
        <li><a href="/patients">Pacientes</a></li>
        <li><a href="/sessions">Sesiones</a></li>
    </ul>
</nav>

<!-- Feature list (no specific order) -->
<ul>
    <li>Gestión de pacientes</li>
    <li>Seguimiento de pagos</li>
    <li>Reportes automáticos</li>
</ul>
```

### Ordered Lists

```html
<!-- Steps in a process -->
<ol>
    <li>Inicie sesión en el sistema</li>
    <li>Seleccione el paciente</li>
    <li>Agregue una nueva sesión</li>
    <li>Confirme los datos</li>
</ol>

<!-- Ranking or priority -->
<ol>
    <li>Pagos pendientes más antiguos</li>
    <li>Citas de hoy</li>
    <li>Seguimientos programados</li>
</ol>

<!-- Custom start number -->
<ol start="5">
    <li>Quinto paso</li>
    <li>Sexto paso</li>
</ol>
```

### Description Lists

```html
<!-- Key-value pairs -->
<dl>
    <dt>Nombre</dt>
    <dd>Juan García</dd>
    
    <dt>Email</dt>
    <dd>juan@example.com</dd>
    
    <dt>Teléfono</dt>
    <dd>+1 234 567 890</dd>
</dl>

<!-- Multiple values for one term -->
<dl>
    <dt>Métodos de pago aceptados</dt>
    <dd>Efectivo</dd>
    <dd>Transferencia bancaria</dd>
    <dd>Tarjeta de crédito</dd>
</dl>

<!-- Multiple terms for one definition -->
<dl>
    <dt>TCC</dt>
    <dt>Terapia Cognitivo-Conductual</dt>
    <dd>Tipo de psicoterapia que ayuda a identificar y cambiar 
        patrones de pensamiento negativos.</dd>
</dl>
```

### Nested Lists

```html
<ul>
    <li>
        Pacientes Activos
        <ul>
            <li>Con sesiones pendientes</li>
            <li>Con pagos al día</li>
        </ul>
    </li>
    <li>
        Pacientes Inactivos
        <ul>
            <li>Alta voluntaria</li>
            <li>Sin actividad reciente</li>
        </ul>
    </li>
</ul>
```

---

## 6. Tables

### Semantic Table Structure

```html
<table>
    <caption>Sesiones del mes de enero 2026</caption>
    
    <thead>
        <tr>
            <th scope="col">Fecha</th>
            <th scope="col">Paciente</th>
            <th scope="col">Precio</th>
            <th scope="col">Estado</th>
        </tr>
    </thead>
    
    <tbody>
        <tr>
            <td><time datetime="2026-01-15">15/01/2026</time></td>
            <td>Juan García</td>
            <td>$150.00</td>
            <td><span class="badge bg-success">Pagado</span></td>
        </tr>
        <tr>
            <td><time datetime="2026-01-14">14/01/2026</time></td>
            <td>María López</td>
            <td>$150.00</td>
            <td><span class="badge bg-warning">Pendiente</span></td>
        </tr>
    </tbody>
    
    <tfoot>
        <tr>
            <th scope="row" colspan="2">Total</th>
            <td>$300.00</td>
            <td></td>
        </tr>
    </tfoot>
</table>
```

### Row and Column Headers

```html
<!-- Column headers -->
<thead>
    <tr>
        <th scope="col">Columna 1</th>
        <th scope="col">Columna 2</th>
    </tr>
</thead>

<!-- Row headers -->
<tbody>
    <tr>
        <th scope="row">Fila 1</th>
        <td>Datos</td>
    </tr>
    <tr>
        <th scope="row">Fila 2</th>
        <td>Datos</td>
    </tr>
</tbody>

<!-- Complex headers with id/headers -->
<table>
    <thead>
        <tr>
            <th id="name">Nombre</th>
            <th id="q1">Q1</th>
            <th id="q2">Q2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th id="juan" headers="name">Juan</th>
            <td headers="juan q1">$500</td>
            <td headers="juan q2">$600</td>
        </tr>
    </tbody>
</table>
```

### Responsive Tables

```html
<!-- Wrapper for horizontal scroll -->
<div class="table-responsive">
    <table class="table">
        <!-- Table content -->
    </table>
</div>

<!-- Or use cards on mobile instead of tables -->
<div class="d-none d-md-block">
    <table class="table"><!-- Desktop table --></table>
</div>
<div class="d-md-none">
    <!-- Mobile card layout -->
</div>
```

---

## 7. Forms

### Semantic Form Structure

```html
<form action="/patients/add" method="POST">
    <!-- Hidden CSRF token -->
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    
    <!-- Grouped fields -->
    <fieldset>
        <legend>Información Personal</legend>
        
        <div class="mb-3">
            <label for="name" class="form-label">Nombre completo</label>
            <input type="text" 
                   id="name" 
                   name="name" 
                   class="form-control"
                   required
                   autocomplete="name"
                   aria-describedby="name-help">
            <div id="name-help" class="form-text">
                Ingrese nombre y apellido
            </div>
        </div>
        
        <div class="mb-3">
            <label for="email" class="form-label">Correo electrónico</label>
            <input type="email" 
                   id="email" 
                   name="email" 
                   class="form-control"
                   autocomplete="email"
                   aria-describedby="email-error"
                   aria-invalid="false">
            <div id="email-error" class="invalid-feedback">
                Ingrese un correo válido
            </div>
        </div>
    </fieldset>
    
    <fieldset>
        <legend>Preferencias</legend>
        
        <!-- Radio group -->
        <div class="mb-3">
            <div class="form-check">
                <input type="radio" 
                       id="contact-email" 
                       name="contact_method" 
                       value="email"
                       class="form-check-input">
                <label for="contact-email" class="form-check-label">
                    Por correo
                </label>
            </div>
            <div class="form-check">
                <input type="radio" 
                       id="contact-phone" 
                       name="contact_method" 
                       value="phone"
                       class="form-check-input">
                <label for="contact-phone" class="form-check-label">
                    Por teléfono
                </label>
            </div>
        </div>
    </fieldset>
    
    <!-- Form actions -->
    <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">
            Guardar
        </button>
        <a href="/patients" class="btn btn-secondary">
            Cancelar
        </a>
    </div>
</form>
```

### Input Types

```html
<!-- Text inputs -->
<input type="text" name="name">           <!-- General text -->
<input type="email" name="email">         <!-- Email validation -->
<input type="tel" name="phone">           <!-- Phone keyboard on mobile -->
<input type="url" name="website">         <!-- URL validation -->
<input type="password" name="password">   <!-- Hidden input -->
<input type="search" name="q">            <!-- Search styling -->

<!-- Number inputs -->
<input type="number" name="quantity" min="1" max="100" step="1">
<input type="range" name="rating" min="1" max="5">

<!-- Date/time inputs -->
<input type="date" name="date">           <!-- Date picker -->
<input type="time" name="time">           <!-- Time picker -->
<input type="datetime-local" name="dt">   <!-- Date + time -->
<input type="month" name="month">         <!-- Month picker -->
<input type="week" name="week">           <!-- Week picker -->

<!-- Other inputs -->
<input type="color" name="color">         <!-- Color picker -->
<input type="file" name="attachment">     <!-- File upload -->
<input type="hidden" name="id">           <!-- Hidden data -->
```

### Labels and Descriptions

```html
<!-- Explicit label association -->
<label for="patient-name">Nombre del paciente</label>
<input type="text" id="patient-name" name="name">

<!-- Implicit label (wrapping) -->
<label>
    Nombre del paciente
    <input type="text" name="name">
</label>

<!-- With description -->
<label for="notes">Notas</label>
<textarea id="notes" 
          name="notes" 
          aria-describedby="notes-desc notes-hint"></textarea>
<div id="notes-desc" class="form-text">Opcional</div>
<div id="notes-hint" class="form-text">Máximo 500 caracteres</div>

<!-- With error message -->
<label for="email">Correo</label>
<input type="email" 
       id="email" 
       name="email" 
       aria-describedby="email-error"
       aria-invalid="true"
       class="is-invalid">
<div id="email-error" class="invalid-feedback" role="alert">
    El correo ingresado no es válido
</div>
```

---

## 8. Interactive Elements

### Buttons

```html
<!-- Submit button -->
<button type="submit">Guardar</button>

<!-- Reset button (use sparingly) -->
<button type="reset">Limpiar formulario</button>

<!-- Generic button (for JavaScript) -->
<button type="button" onclick="doSomething()">Acción</button>

<!-- Disabled state -->
<button type="submit" disabled aria-disabled="true">
    Guardando...
</button>

<!-- With loading state -->
<button type="submit" id="save-btn">
    <span class="spinner-border spinner-border-sm d-none" 
          role="status" 
          aria-hidden="true"></span>
    <span class="btn-text">Guardar</span>
</button>
```

### Links vs. Buttons

```html
<!-- Link: Navigation to another page/resource -->
<a href="/patients/123">Ver paciente</a>

<!-- Button: Action that doesn't navigate -->
<button type="button" onclick="openModal()">Abrir modal</button>

<!-- Wrong: Button styled as link for navigation -->
<button onclick="location.href='/patients'">Ver pacientes</button>  <!-- ❌ -->

<!-- Wrong: Link for action without navigation -->
<a href="#" onclick="deleteItem(); return false;">Eliminar</a>  <!-- ❌ -->

<!-- Correct: Link that looks like button -->
<a href="/patients/add" class="btn btn-primary">Agregar paciente</a>

<!-- Correct: Button that looks like link -->
<button type="button" class="btn btn-link">Más información</button>
```

### Details and Summary

```html
<!-- Collapsible content -->
<details>
    <summary>Mostrar detalles de la sesión</summary>
    <div class="details-content">
        <p>Fecha: 15/01/2026</p>
        <p>Duración: 1 hora</p>
        <p>Notas: Progreso significativo esta semana.</p>
    </div>
</details>

<!-- Open by default -->
<details open>
    <summary>Información importante</summary>
    <p>Este contenido es visible por defecto.</p>
</details>

<!-- Styled as accordion -->
<details class="accordion-item">
    <summary class="accordion-header">Pregunta frecuente 1</summary>
    <div class="accordion-body">
        Respuesta a la pregunta...
    </div>
</details>
```

### Dialog Element

```html
<!-- Native dialog -->
<dialog id="confirm-dialog" aria-labelledby="dialog-title">
    <h2 id="dialog-title">Confirmar acción</h2>
    <p>¿Está seguro de continuar?</p>
    <form method="dialog">
        <button value="cancel">Cancelar</button>
        <button value="confirm">Confirmar</button>
    </form>
</dialog>

<script>
    const dialog = document.getElementById('confirm-dialog');
    
    // Show as modal
    dialog.showModal();
    
    // Show as non-modal
    dialog.show();
    
    // Close
    dialog.close();
</script>
```

---

## 9. Media Elements

### Images

```html
<!-- Basic image with alt text -->
<img src="/images/patient-photo.jpg" 
     alt="Foto de perfil de Juan García"
     width="150" 
     height="150">

<!-- Decorative image (empty alt) -->
<img src="/images/decoration.svg" alt="" aria-hidden="true">

<!-- Figure with caption -->
<figure>
    <img src="/images/chart.png" 
         alt="Gráfico mostrando progreso mensual: enero 40%, febrero 60%, marzo 80%">
    <figcaption>Progreso del tratamiento en el primer trimestre</figcaption>
</figure>

<!-- Responsive images -->
<img src="/images/hero.jpg"
     srcset="/images/hero-320.jpg 320w,
             /images/hero-640.jpg 640w,
             /images/hero-1280.jpg 1280w"
     sizes="(max-width: 320px) 280px,
            (max-width: 640px) 600px,
            1200px"
     alt="Descripción de la imagen">

<!-- Picture element for art direction -->
<picture>
    <source media="(min-width: 1200px)" srcset="/images/hero-desktop.jpg">
    <source media="(min-width: 768px)" srcset="/images/hero-tablet.jpg">
    <img src="/images/hero-mobile.jpg" alt="Descripción">
</picture>
```

### Icons

```html
<!-- Decorative icon (hidden from AT) -->
<i class="bi bi-calendar" aria-hidden="true"></i>
<span>Calendario</span>

<!-- Icon-only button (needs accessible name) -->
<button type="button" aria-label="Editar paciente">
    <i class="bi bi-pencil" aria-hidden="true"></i>
</button>

<!-- Icon with visible text -->
<button type="button">
    <i class="bi bi-plus-lg" aria-hidden="true"></i>
    <span>Agregar</span>
</button>

<!-- SVG icon inline -->
<svg aria-hidden="true" focusable="false" width="24" height="24">
    <use href="/icons.svg#calendar"></use>
</svg>
```

---

## 10. Quick Reference

### Element Selection Guide

| Content Type | Element | Example |
|--------------|---------|---------|
| Page header | `<header>` | Site banner, logo, nav |
| Navigation | `<nav>` | Main menu, breadcrumbs |
| Primary content | `<main>` | Main page content |
| Independent content | `<article>` | Blog post, patient card |
| Thematic section | `<section>` | Groups with heading |
| Related content | `<aside>` | Sidebar, callout |
| Footer info | `<footer>` | Copyright, links |
| Date/time | `<time>` | `datetime` attribute |
| Abbreviation | `<abbr>` | `title` attribute |
| Definition | `<dfn>` | First use of term |
| Code | `<code>` | Inline code |
| Keyboard | `<kbd>` | Keyboard shortcuts |
| Quote (block) | `<blockquote>` | Long quotations |
| Quote (inline) | `<q>` | Short quotations |

### Common Anti-Patterns

| ❌ Wrong | ✅ Correct | Why |
|----------|-----------|-----|
| `<div class="header">` | `<header>` | Use semantic elements |
| `<div onclick="">` | `<button type="button">` | Buttons are keyboard accessible |
| `<a href="#">` | `<button type="button">` | Links are for navigation |
| `<b>Important</b>` | `<strong>Important</strong>` | Use semantic emphasis |
| `<i>Term</i>` | `<em>Term</em>` | Use semantic emphasis |
| `<br><br>` | `<p>` or CSS margin | Use proper spacing |
| `<h4>` for small text | `<h2 class="h4">` | Keep heading hierarchy |
| Empty `<th>` | `<td>` | Only use th for headers |
