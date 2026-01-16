# Skill: Web Performance Optimization

> **Scope:** Performance metrics, optimization strategies, and monitoring techniques for Flask/Jinja2 web applications.

---

## 1. Key Performance Metrics

### Core Web Vitals

| Metric | Full Name | Good | Needs Improvement | Poor | Measures |
|--------|-----------|------|-------------------|------|----------|
| **LCP** | Largest Contentful Paint | ≤2.5s | 2.5s - 4.0s | >4.0s | Loading performance |
| **FID** | First Input Delay | ≤100ms | 100ms - 300ms | >300ms | Interactivity |
| **INP** | Interaction to Next Paint | ≤200ms | 200ms - 500ms | >500ms | Responsiveness |
| **CLS** | Cumulative Layout Shift | ≤0.1 | 0.1 - 0.25 | >0.25 | Visual stability |

### Additional Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| **TTFB** | <600ms | Time to First Byte - server response time |
| **FCP** | <1.8s | First Contentful Paint - first content visible |
| **TTI** | <3.8s | Time to Interactive - page fully interactive |
| **TBT** | <200ms | Total Blocking Time - main thread blocks |
| **Speed Index** | <3.4s | How quickly content is visually displayed |

---

## 2. Performance Budget

### Budget Template for Project

```yaml
# performance-budget.yaml
performance:
  # Core Web Vitals
  lcp: 2.5s
  fid: 100ms
  inp: 200ms
  cls: 0.1

  # Resource budgets
  resources:
    javascript:
      total: 200KB    # Compressed
      per_bundle: 100KB
    css:
      total: 50KB     # Compressed
      critical: 14KB  # Inline CSS
    images:
      hero: 100KB
      thumbnail: 30KB
    fonts:
      total: 100KB
      per_family: 50KB

  # Request counts
  requests:
    total: 50
    third_party: 10
    fonts: 2

  # Page weight
  page_weight:
    target: 500KB
    max: 1MB
```

### Budget Monitoring

```javascript
// static/js/modules/utils/performanceMonitor.js

/**
 * Performance monitoring utilities
 * @module utils/performanceMonitor
 */

/**
 * Check if Core Web Vitals meet thresholds
 * @returns {Promise<Object>} Metrics and their status
 */
export async function checkWebVitals() {
    const metrics = {};
    
    // LCP observation
    const lcpObserver = new PerformanceObserver((entryList) => {
        const entries = entryList.getEntries();
        const lastEntry = entries[entries.length - 1];
        metrics.lcp = {
            value: lastEntry.startTime,
            status: lastEntry.startTime <= 2500 ? 'good' : 
                    lastEntry.startTime <= 4000 ? 'needs-improvement' : 'poor'
        };
    });
    lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
    
    // CLS observation
    let clsValue = 0;
    const clsObserver = new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            if (!entry.hadRecentInput) {
                clsValue += entry.value;
            }
        }
        metrics.cls = {
            value: clsValue,
            status: clsValue <= 0.1 ? 'good' : 
                    clsValue <= 0.25 ? 'needs-improvement' : 'poor'
        };
    });
    clsObserver.observe({ type: 'layout-shift', buffered: true });
    
    // FCP from navigation timing
    const paintEntries = performance.getEntriesByType('paint');
    const fcpEntry = paintEntries.find(e => e.name === 'first-contentful-paint');
    if (fcpEntry) {
        metrics.fcp = {
            value: fcpEntry.startTime,
            status: fcpEntry.startTime <= 1800 ? 'good' : 
                    fcpEntry.startTime <= 3000 ? 'needs-improvement' : 'poor'
        };
    }
    
    return metrics;
}

/**
 * Log performance marks for debugging
 * @param {string} markName - Name of the performance mark
 */
export function mark(markName) {
    if (performance && performance.mark) {
        performance.mark(markName);
    }
}

/**
 * Measure time between two marks
 * @param {string} measureName - Name for the measurement
 * @param {string} startMark - Start mark name
 * @param {string} endMark - End mark name
 * @returns {number|null} Duration in milliseconds
 */
export function measure(measureName, startMark, endMark) {
    try {
        performance.measure(measureName, startMark, endMark);
        const entries = performance.getEntriesByName(measureName);
        return entries.length > 0 ? entries[0].duration : null;
    } catch (e) {
        console.warn(`Performance measure failed: ${e.message}`);
        return null;
    }
}
```

---

## 3. Server-Side Optimization

### Flask Response Optimization

```python
# app/middleware/performance.py

from flask import Flask, request, g
from functools import wraps
import time
import gzip
from io import BytesIO


def init_performance_middleware(app: Flask):
    """Initialize performance-related middleware."""
    
    @app.before_request
    def start_timer():
        """Record request start time."""
        g.start_time = time.perf_counter()
    
    @app.after_request
    def add_performance_headers(response):
        """Add performance-related headers."""
        # Calculate response time
        if hasattr(g, 'start_time'):
            elapsed = time.perf_counter() - g.start_time
            response.headers['X-Response-Time'] = f'{elapsed:.4f}s'
        
        # Add cache headers for static content
        if request.path.startswith('/static/'):
            # Cache static files for 1 year (with versioning)
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        
        return response


def compress_response(response):
    """Gzip compress response if beneficial."""
    # Only compress text-based responses
    if response.content_type.startswith(('text/', 'application/json', 'application/javascript')):
        if len(response.data) > 500:  # Only compress if > 500 bytes
            gzip_buffer = BytesIO()
            with gzip.GzipFile(mode='wb', fileobj=gzip_buffer) as f:
                f.write(response.data)
            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Content-Length'] = len(response.data)
    
    return response
```

### Database Query Optimization

```python
# app/services/patient_service.py - Optimized queries

from sqlalchemy.orm import joinedload, selectinload
from app.models import Person, TherapySession


class PatientService:
    """Optimized patient service with eager loading."""
    
    @staticmethod
    def get_with_sessions(patient_id: int, user_id: int):
        """
        Get patient with sessions using eager loading.
        Prevents N+1 query problem.
        """
        # ❌ Bad: N+1 queries
        # patient = Person.query.get(patient_id)
        # sessions = patient.sessions  # Triggers additional query
        
        # ✅ Good: Single query with JOIN
        return Person.query.options(
            selectinload(Person.sessions)
        ).filter(
            Person.id == patient_id,
            Person.user_id == user_id,
            Person.deleted_at.is_(None)
        ).first()
    
    @staticmethod
    def get_dashboard_data(user_id: int):
        """
        Optimized dashboard query - single database round trip.
        """
        from sqlalchemy import func, case
        from datetime import date, timedelta
        
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        # Aggregate query instead of multiple queries
        stats = db.session.query(
            func.count(Person.id).label('total_patients'),
            func.sum(case((Person.is_active == True, 1), else_=0)).label('active_patients'),
            func.count(TherapySession.id).filter(
                TherapySession.session_date >= week_start
            ).label('sessions_this_week')
        ).outerjoin(
            TherapySession, Person.id == TherapySession.person_id
        ).filter(
            Person.user_id == user_id,
            Person.deleted_at.is_(None)
        ).first()
        
        return stats
```

### Template Caching

```python
# app/__init__.py - Template optimization

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Enable template caching in production
    if config_name == 'production':
        app.jinja_env.auto_reload = False
        app.config['TEMPLATES_AUTO_RELOAD'] = False
        
        # Bytecode caching
        from jinja2 import FileSystemBytecodeCache
        app.jinja_env.bytecode_cache = FileSystemBytecodeCache(
            directory='/tmp/jinja_cache'
        )
    
    return app
```

---

## 4. CSS Performance

### Critical CSS Extraction

```html
<!-- templates/base.html - Critical CSS inline -->
<head>
    <!-- Critical CSS inline for above-the-fold content -->
    <style>
        /* Critical CSS - extracted from main.css */
        :root {
            --mlc-teal: #3F4A49;
            --mlc-beige: #DCD9D0;
            --mlc-cream: #F5F3EF;
        }
        
        body {
            margin: 0;
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--mlc-cream);
        }
        
        .navbar {
            background-color: var(--mlc-teal);
            padding: 0.5rem 1rem;
        }
        
        /* Container for initial layout */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        /* Prevent layout shift for common elements */
        img, video {
            max-width: 100%;
            height: auto;
        }
        
        /* Loading skeleton */
        .skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s infinite;
        }
        
        @keyframes skeleton-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    
    <!-- Non-critical CSS loaded async -->
    <link rel="preload" href="{{ url_for('static', filename='css/main.css') }}" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    </noscript>
</head>
```

### CSS Loading Optimization

```html
<!-- Preconnect to external resources -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical fonts -->
<link rel="preload" 
      href="{{ url_for('static', filename='fonts/inter-var.woff2') }}" 
      as="font" 
      type="font/woff2" 
      crossorigin>
```

### Reduce CSS Specificity

```css
/* ❌ Bad: High specificity, hard to override */
body div.container section.content article.card div.card-body h3.card-title {
    color: #333;
}

/* ✅ Good: Low specificity, easy to maintain */
.card-title {
    color: var(--text-primary);
}

/* ❌ Bad: ID selectors (specificity 100) */
#main-header .nav-link {
    color: white;
}

/* ✅ Good: Class selectors (specificity 10) */
.header__nav-link {
    color: var(--nav-link-color);
}
```

---

## 5. JavaScript Performance

### Code Splitting Strategy

```javascript
// static/js/main.js - Dynamic imports for code splitting

/**
 * Lazy load modules based on page context
 */
async function initPage() {
    const currentPath = window.location.pathname;
    
    // Only load dashboard module on dashboard page
    if (currentPath === '/' || currentPath === '/patients') {
        const { initDashboard } = await import('./modules/components/dashboardRenderer.js');
        initDashboard();
    }
    
    // Only load form validation on form pages
    if (document.querySelector('form[data-validate]')) {
        const { initFormValidation } = await import('./modules/utils/validators.js');
        initFormValidation();
    }
    
    // Only load carousel on pages with carousels
    if (document.querySelector('[data-carousel]')) {
        const { initCarousel } = await import('./modules/ui/carousel.js');
        initCarousel();
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPage);
} else {
    initPage();
}
```

### Debounce and Throttle

```javascript
// static/js/modules/utils/helpers.js

/**
 * Debounce function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function calls
 * @param {Function} func - Function to throttle
 * @param {number} limit - Minimum time between calls in milliseconds
 * @returns {Function} Throttled function
 */
export function throttle(func, limit = 100) {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Usage examples
const handleScroll = throttle(() => {
    console.log('Scroll position:', window.scrollY);
}, 100);

const handleSearch = debounce((query) => {
    fetchSearchResults(query);
}, 300);

window.addEventListener('scroll', handleScroll);
searchInput.addEventListener('input', (e) => handleSearch(e.target.value));
```

### Event Delegation

```javascript
// ❌ Bad: Event listener per element
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', handleDelete);
});

// ✅ Good: Single delegated listener
document.addEventListener('click', (e) => {
    const deleteBtn = e.target.closest('.delete-btn');
    if (deleteBtn) {
        handleDelete(deleteBtn);
    }
});
```

### Efficient DOM Manipulation

```javascript
// ❌ Bad: Multiple reflows
items.forEach(item => {
    const el = document.createElement('div');
    el.textContent = item.name;
    container.appendChild(el);  // Triggers reflow each time
});

// ✅ Good: Single reflow with DocumentFragment
const fragment = document.createDocumentFragment();
items.forEach(item => {
    const el = document.createElement('div');
    el.textContent = item.name;
    fragment.appendChild(el);
});
container.appendChild(fragment);  // Single reflow

// ✅ Better: Use innerHTML for large lists
container.innerHTML = items.map(item => `
    <div class="item">${escapeHtml(item.name)}</div>
`).join('');
```

### Request Animation Frame

```javascript
// ❌ Bad: Direct style manipulation on scroll
window.addEventListener('scroll', () => {
    element.style.transform = `translateY(${window.scrollY}px)`;
});

// ✅ Good: Use requestAnimationFrame
let ticking = false;

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(() => {
            element.style.transform = `translateY(${window.scrollY}px)`;
            ticking = false;
        });
        ticking = true;
    }
});
```

---

## 6. Image Optimization

### Responsive Images

```html
<!-- templates/macros/_images.html -->

{% macro responsive_image(
    src,
    alt,
    sizes='100vw',
    widths=[320, 640, 960, 1280],
    loading='lazy',
    class_name=''
) %}
<img 
    src="{{ url_for('static', filename='images/' + src) }}"
    srcset="{% for w in widths %}{{ url_for('static', filename='images/optimized/' + src|replace('.', f'-{w}w.')) }} {{ w }}w{% if not loop.last %}, {% endif %}{% endfor %}"
    sizes="{{ sizes }}"
    alt="{{ alt }}"
    loading="{{ loading }}"
    decoding="async"
    class="{{ class_name }}"
>
{% endmacro %}

{# Usage #}
{{ responsive_image(
    src='hero.jpg',
    alt='Dashboard hero image',
    sizes='(max-width: 768px) 100vw, 50vw',
    loading='eager'
) }}
```

### Image Placeholders (Prevent CLS)

```html
<!-- templates/macros/_images.html -->

{% macro image_with_placeholder(src, alt, width, height, class_name='') %}
<div class="image-container" style="aspect-ratio: {{ width }}/{{ height }}">
    <img 
        src="{{ url_for('static', filename='images/' + src) }}"
        alt="{{ alt }}"
        width="{{ width }}"
        height="{{ height }}"
        loading="lazy"
        decoding="async"
        class="image-fade {{ class_name }}"
        onload="this.classList.add('loaded')"
    >
</div>
{% endmacro %}
```

```css
/* static/css/components/_images.css */

.image-container {
    position: relative;
    background-color: var(--bg-skeleton);
    overflow: hidden;
}

.image-fade {
    opacity: 0;
    transition: opacity 0.3s ease;
}

.image-fade.loaded {
    opacity: 1;
}
```

### Modern Image Formats

```html
<!-- Use picture element for format fallbacks -->
<picture>
    <!-- AVIF for modern browsers (best compression) -->
    <source 
        srcset="{{ url_for('static', filename='images/hero.avif') }}"
        type="image/avif">
    
    <!-- WebP fallback -->
    <source 
        srcset="{{ url_for('static', filename='images/hero.webp') }}"
        type="image/webp">
    
    <!-- JPEG fallback for older browsers -->
    <img 
        src="{{ url_for('static', filename='images/hero.jpg') }}"
        alt="Dashboard hero"
        loading="lazy"
        decoding="async">
</picture>
```

---

## 7. Font Optimization

### Font Loading Strategy

```css
/* static/css/base/_typography.css */

/* Font-display: swap to prevent invisible text */
@font-face {
    font-family: 'Inter';
    src: url('../fonts/inter-var.woff2') format('woff2-variations');
    font-weight: 100 900;
    font-style: normal;
    font-display: swap;  /* Show fallback font immediately */
}

/* System font stack fallback */
:root {
    --font-family-sans: 'Inter', system-ui, -apple-system, 'Segoe UI', 
                         Roboto, 'Helvetica Neue', Arial, sans-serif;
}
```

### Subset Fonts

```html
<!-- Only load Latin characters if that's all you need -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&subset=latin&display=swap" rel="stylesheet">
```

### Preload Critical Fonts

```html
<head>
    <!-- Preload the most critical font weight -->
    <link 
        rel="preload" 
        href="{{ url_for('static', filename='fonts/inter-var.woff2') }}" 
        as="font" 
        type="font/woff2" 
        crossorigin>
</head>
```

---

## 8. Caching Strategies

### Flask Caching Configuration

```python
# app/config.py

class ProductionConfig(Config):
    """Production configuration with caching."""
    
    # Response caching
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year for static files
    
    # Template caching
    TEMPLATES_AUTO_RELOAD = False


# app/middleware/caching.py

from flask import make_response
from functools import wraps


def cache_control(max_age=3600, public=True):
    """Add cache control headers to response."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            
            visibility = 'public' if public else 'private'
            response.headers['Cache-Control'] = f'{visibility}, max-age={max_age}'
            
            return response
        return decorated_function
    return decorator


# Usage in routes
@app.route('/api/v1/stats')
@cache_control(max_age=300)  # Cache for 5 minutes
def get_stats():
    return jsonify(stats)
```

### Static Asset Versioning

```python
# app/__init__.py

import hashlib
import os


def get_file_hash(filepath):
    """Generate hash for cache busting."""
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:8]
    return None


def versioned_static(filename):
    """Generate versioned URL for static files."""
    filepath = os.path.join(app.static_folder, filename)
    file_hash = get_file_hash(filepath)
    if file_hash:
        return f'/static/{filename}?v={file_hash}'
    return f'/static/{filename}'


# Register as Jinja2 function
app.jinja_env.globals['versioned_static'] = versioned_static
```

```html
<!-- Usage in templates -->
<link rel="stylesheet" href="{{ versioned_static('css/main.css') }}">
<script src="{{ versioned_static('js/main.js') }}"></script>
```

### Service Worker Caching

```javascript
// static/sw.js - Service Worker for offline caching

const CACHE_NAME = 'mlc-app-v1';
const STATIC_ASSETS = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/css/bootstrap.min.css',
    '/static/js/bootstrap.bundle.min.js'
];

// Install: Cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS);
        })
    );
});

// Fetch: Serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            // Return cached version or fetch from network
            return response || fetch(event.request).then((fetchResponse) => {
                // Cache successful responses
                if (fetchResponse.ok && event.request.method === 'GET') {
                    const responseClone = fetchResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return fetchResponse;
            });
        })
    );
});
```

---

## 9. Performance Testing

### Lighthouse Integration

```javascript
// scripts/lighthouse-test.js

const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runLighthouse(url) {
    const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
    
    const options = {
        logLevel: 'info',
        output: 'json',
        port: chrome.port,
        onlyCategories: ['performance']
    };
    
    const result = await lighthouse(url, options);
    
    const { performance } = result.lhr.categories;
    const metrics = result.lhr.audits;
    
    console.log('Performance Score:', performance.score * 100);
    console.log('LCP:', metrics['largest-contentful-paint'].displayValue);
    console.log('FID:', metrics['max-potential-fid'].displayValue);
    console.log('CLS:', metrics['cumulative-layout-shift'].displayValue);
    console.log('Speed Index:', metrics['speed-index'].displayValue);
    
    await chrome.kill();
    
    // Fail if performance score is below threshold
    if (performance.score < 0.9) {
        process.exit(1);
    }
}

runLighthouse('http://localhost:5000');
```

### Performance Timing API

```javascript
// static/js/modules/utils/performanceReporter.js

/**
 * Collect and report performance metrics
 */
export function reportPerformance() {
    // Wait for page to fully load
    window.addEventListener('load', () => {
        // Give time for LCP to settle
        setTimeout(() => {
            const timing = performance.timing;
            const navigation = performance.getEntriesByType('navigation')[0];
            
            const metrics = {
                // Network metrics
                dns: timing.domainLookupEnd - timing.domainLookupStart,
                tcp: timing.connectEnd - timing.connectStart,
                ttfb: timing.responseStart - timing.requestStart,
                
                // Document metrics
                domParsing: timing.domInteractive - timing.responseEnd,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                load: timing.loadEventEnd - timing.navigationStart,
                
                // Resource counts
                resourceCount: performance.getEntriesByType('resource').length,
                
                // Transfer size
                transferSize: navigation?.transferSize || 0
            };
            
            // Log or send to analytics
            console.table(metrics);
            
            // Send to backend
            if (navigator.sendBeacon) {
                navigator.sendBeacon('/api/v1/metrics', JSON.stringify(metrics));
            }
        }, 3000);
    });
}
```

---

## 10. Performance Checklist

### Before Deploy

```markdown
## Performance Checklist

### Critical Rendering Path
- [ ] Critical CSS inlined in <head>
- [ ] Non-critical CSS loaded async
- [ ] JavaScript deferred or async
- [ ] Web fonts preloaded

### Images
- [ ] All images have width/height attributes
- [ ] Lazy loading on below-fold images
- [ ] WebP/AVIF formats with fallbacks
- [ ] Responsive images with srcset

### JavaScript
- [ ] Code splitting implemented
- [ ] Event delegation used
- [ ] Debounce/throttle on frequent events
- [ ] No layout thrashing

### Server
- [ ] Gzip/Brotli compression enabled
- [ ] Proper cache headers set
- [ ] Database queries optimized
- [ ] Static asset versioning

### Monitoring
- [ ] Core Web Vitals tracked
- [ ] Performance budget defined
- [ ] Lighthouse CI in pipeline
```

### Performance CI Integration

```yaml
# .github/workflows/performance.yml

name: Performance Check

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start application
        run: |
          docker-compose up -d
          sleep 10
      
      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            http://localhost:5000/
            http://localhost:5000/login
          budgetPath: ./performance-budget.json
          uploadArtifacts: true
      
      - name: Assert performance
        run: |
          # Fail if performance drops below threshold
          node scripts/check-performance.js
```

---

## 11. Quick Reference

### Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| LCP | <2.5s | <4.0s |
| FID/INP | <100ms | <300ms |
| CLS | <0.1 | <0.25 |
| TTFB | <600ms | <1.0s |
| Total JS | <200KB | <500KB |
| Total CSS | <50KB | <100KB |

### Common Performance Fixes

| Issue | Solution |
|-------|----------|
| Slow LCP | Preload hero image, inline critical CSS |
| High CLS | Set image dimensions, reserve space for dynamic content |
| Long FID/INP | Code split, defer non-critical JS |
| Slow TTFB | Enable caching, optimize queries |
| Large bundles | Tree shaking, code splitting |
| Render blocking | Async CSS, defer JS |

---

## Related Skills

- [Asset Optimization](skill-asset-optimization.md)
- [Lazy Loading](skill-lazy-loading.md)
- [Core Web Vitals](skill-core-web-vitals.md)
- [CSS Architecture](skill-css-architecture.md)
- [JavaScript Modules](skill-javascript-modules.md)
