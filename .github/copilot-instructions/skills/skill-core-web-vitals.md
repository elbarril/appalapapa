# Skill: Core Web Vitals

> **Scope:** Understanding, measuring, and optimizing Core Web Vitals (LCP, FID/INP, CLS) for Flask/Jinja2 web applications.

---

## 1. Core Web Vitals Overview

### The Three Metrics

| Metric | Name | Measures | Good | Needs Improvement | Poor |
|--------|------|----------|------|-------------------|------|
| **LCP** | Largest Contentful Paint | Loading performance | ≤2.5s | 2.5s - 4.0s | >4.0s |
| **INP** | Interaction to Next Paint | Responsiveness | ≤200ms | 200ms - 500ms | >500ms |
| **CLS** | Cumulative Layout Shift | Visual stability | ≤0.1 | 0.1 - 0.25 | >0.25 |

> **Note:** INP replaced FID (First Input Delay) as a Core Web Vital in March 2024.

### Why Core Web Vitals Matter

- **SEO Ranking Factor**: Google uses CWV as part of page experience signals
- **User Experience**: Directly correlate with user satisfaction
- **Conversion Rates**: Poor CWV = higher bounce rates
- **Accessibility**: Fast, stable pages benefit all users

---

## 2. Largest Contentful Paint (LCP)

### What LCP Measures

LCP measures when the largest content element becomes visible in the viewport.

**LCP Candidates:**
- `<img>` elements
- `<image>` inside `<svg>`
- `<video>` poster images
- Elements with `background-image` via CSS
- Block-level text elements (`<p>`, `<h1>`, etc.)

### Common LCP Issues

| Issue | Impact | Solution |
|-------|--------|----------|
| Slow server response | Delays everything | Optimize TTFB, use caching |
| Render-blocking resources | Delays paint | Defer non-critical CSS/JS |
| Slow resource load times | LCP element loads late | Preload, optimize images |
| Client-side rendering | Content not in HTML | Server-side render critical content |

### LCP Optimization Strategies

#### 1. Optimize Server Response Time (TTFB)

```python
# app/middleware/caching.py

from flask import Flask, make_response
from functools import wraps
import time


def init_performance_headers(app: Flask):
    """Add performance headers to responses."""
    
    @app.after_request
    def add_headers(response):
        # Add timing header for debugging
        if hasattr(g, 'start_time'):
            elapsed = time.perf_counter() - g.start_time
            response.headers['Server-Timing'] = f'total;dur={elapsed*1000:.2f}'
        
        return response


def cache_page(max_age=300):
    """Cache page responses."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.headers['Cache-Control'] = f'public, max-age={max_age}'
            return response
        return decorated
    return decorator
```

#### 2. Preload LCP Resources

```html
<!-- templates/base.html -->
<head>
    <!-- Preload the LCP image -->
    {% block preload %}
    <link rel="preload" 
          href="{{ url_for('static', filename='images/hero.webp') }}" 
          as="image"
          type="image/webp">
    {% endblock %}
    
    <!-- Preload critical fonts -->
    <link rel="preload" 
          href="{{ url_for('static', filename='fonts/inter-var.woff2') }}" 
          as="font" 
          type="font/woff2" 
          crossorigin>
    
    <!-- Preconnect to external origins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
</head>
```

#### 3. Optimize LCP Images

```html
<!-- templates/macros/_images.html -->

{% macro lcp_image(src, alt, width, height, sizes='100vw') %}
{#
    Optimized image for LCP - loaded eagerly with high priority.
    Use only for above-the-fold hero images.
#}
<img 
    src="{{ url_for('static', filename='images/' + src) }}"
    alt="{{ alt }}"
    width="{{ width }}"
    height="{{ height }}"
    sizes="{{ sizes }}"
    loading="eager"
    decoding="sync"
    fetchpriority="high"
    class="lcp-image">
{% endmacro %}
```

#### 4. Inline Critical CSS

```html
<!-- templates/base.html -->
<head>
    <style>
        /* Critical CSS - inline for immediate render */
        :root {
            --mlc-teal: #3F4A49;
            --mlc-cream: #F5F3EF;
        }
        
        body {
            margin: 0;
            font-family: system-ui, sans-serif;
            background: var(--mlc-cream);
        }
        
        .navbar {
            background: var(--mlc-teal);
            padding: 0.5rem 1rem;
            min-height: 56px;
        }
        
        .hero {
            min-height: 400px;
        }
        
        /* Prevent FOUT */
        .hero-title {
            font-size: 2.5rem;
            line-height: 1.2;
        }
    </style>
    
    <!-- Non-critical CSS loaded async -->
    <link rel="preload" href="{{ url_for('static', filename='css/main.css') }}" as="style" onload="this.onload=null;this.rel='stylesheet'">
</head>
```

#### 5. Remove Render-Blocking Scripts

```html
<!-- ❌ Bad: Blocks rendering -->
<script src="/static/js/main.js"></script>

<!-- ✅ Good: Deferred loading -->
<script src="/static/js/main.js" defer></script>

<!-- ✅ Good: Module (deferred by default) -->
<script src="/static/js/main.js" type="module"></script>
```

---

## 3. Interaction to Next Paint (INP)

### What INP Measures

INP measures the latency of all user interactions (clicks, taps, key presses) and reports the worst interaction, representing overall page responsiveness.

### Common INP Issues

| Issue | Impact | Solution |
|-------|--------|----------|
| Long JavaScript tasks | Blocks main thread | Break up long tasks |
| Heavy event handlers | Slow response to input | Optimize handlers |
| Large DOM size | Slow style/layout recalc | Reduce DOM complexity |
| Third-party scripts | Compete for main thread | Defer, lazy load |

### INP Optimization Strategies

#### 1. Break Up Long Tasks

```javascript
// static/js/modules/utils/scheduler.js

/**
 * Yield to the main thread to prevent blocking.
 * @returns {Promise<void>}
 */
export function yieldToMain() {
    return new Promise(resolve => {
        setTimeout(resolve, 0);
    });
}

/**
 * Process items in chunks, yielding between each chunk.
 * @param {Array} items - Items to process
 * @param {Function} processor - Function to process each item
 * @param {number} chunkSize - Items per chunk
 */
export async function processInChunks(items, processor, chunkSize = 50) {
    for (let i = 0; i < items.length; i += chunkSize) {
        const chunk = items.slice(i, i + chunkSize);
        
        for (const item of chunk) {
            processor(item);
        }
        
        // Yield to main thread between chunks
        await yieldToMain();
    }
}

// Usage
async function renderLargeList(items) {
    const container = document.getElementById('list');
    
    await processInChunks(items, (item) => {
        const el = document.createElement('div');
        el.textContent = item.name;
        container.appendChild(el);
    }, 20);
}
```

#### 2. Use requestIdleCallback

```javascript
// static/js/modules/utils/idleQueue.js

/**
 * Queue of tasks to run when browser is idle.
 */
class IdleQueue {
    constructor() {
        this.queue = [];
        this.isProcessing = false;
    }
    
    /**
     * Add a task to the idle queue.
     * @param {Function} task - Task to run
     * @param {number} timeout - Max wait time in ms
     */
    add(task, timeout = 2000) {
        this.queue.push({ task, timeout });
        this.process();
    }
    
    process() {
        if (this.isProcessing || this.queue.length === 0) return;
        
        this.isProcessing = true;
        
        const processNext = (deadline) => {
            while (this.queue.length > 0 && deadline.timeRemaining() > 0) {
                const { task } = this.queue.shift();
                try {
                    task();
                } catch (e) {
                    console.error('Idle task error:', e);
                }
            }
            
            if (this.queue.length > 0) {
                requestIdleCallback(processNext, { timeout: this.queue[0].timeout });
            } else {
                this.isProcessing = false;
            }
        };
        
        if ('requestIdleCallback' in window) {
            requestIdleCallback(processNext, { timeout: this.queue[0].timeout });
        } else {
            // Fallback for Safari
            setTimeout(() => {
                const deadline = { timeRemaining: () => 50 };
                processNext(deadline);
            }, 1);
        }
    }
}

export const idleQueue = new IdleQueue();

// Usage
import { idleQueue } from './idleQueue.js';

idleQueue.add(() => {
    // Non-urgent analytics
    sendAnalytics();
});

idleQueue.add(() => {
    // Preload next page resources
    prefetchNextPage();
});
```

#### 3. Optimize Event Handlers

```javascript
// static/js/modules/ui/interactions.js

/**
 * Debounced and optimized event handling.
 */

// ❌ Bad: Heavy work in handler
document.addEventListener('scroll', () => {
    // Expensive DOM queries and calculations
    const items = document.querySelectorAll('.item');
    items.forEach(item => {
        const rect = item.getBoundingClientRect();
        // ...complex calculations
    });
});

// ✅ Good: Throttled with requestAnimationFrame
let ticking = false;
document.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(() => {
            updateOnScroll();
            ticking = false;
        });
        ticking = true;
    }
});

// ❌ Bad: Synchronous handler
button.addEventListener('click', () => {
    // Heavy computation blocks next paint
    const result = expensiveCalculation();
    updateUI(result);
});

// ✅ Good: Defer heavy work
button.addEventListener('click', () => {
    // Immediate visual feedback
    button.classList.add('loading');
    
    // Defer heavy work
    requestAnimationFrame(() => {
        const result = expensiveCalculation();
        updateUI(result);
        button.classList.remove('loading');
    });
});
```

#### 4. Reduce DOM Size

```html
<!-- ❌ Bad: Deeply nested DOM -->
<div class="wrapper">
    <div class="container">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-body">
                        <div class="content">
                            <p>Text</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ✅ Good: Flatter structure -->
<article class="card">
    <p class="card__content">Text</p>
</article>
```

```javascript
// Virtualize long lists
// Only render visible items

import { initVirtualList } from './virtualList.js';

initVirtualList({
    container: '#patient-list',
    itemHeight: 80,
    items: patients,
    renderItem: (patient) => `
        <div class="patient-card">
            <h3>${patient.name}</h3>
        </div>
    `
});
```

---

## 4. Cumulative Layout Shift (CLS)

### What CLS Measures

CLS measures visual stability - how much visible content shifts during page load and interaction.

**CLS Formula:**
```
Layout Shift Score = Impact Fraction × Distance Fraction
```

### Common CLS Causes

| Cause | Impact | Solution |
|-------|--------|----------|
| Images without dimensions | Content shifts when loaded | Set width/height |
| Ads/embeds without size | Space allocated late | Reserve space |
| Web fonts causing FOUT | Text reflows | font-display: swap + fallback |
| Dynamic content injection | Pushes content down | Reserve space or animate |
| Animations triggering layout | Repeated shifts | Use transform/opacity only |

### CLS Optimization Strategies

#### 1. Always Set Image Dimensions

```html
<!-- ❌ Bad: No dimensions -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ Good: Explicit dimensions -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ Good: CSS aspect-ratio -->
<img src="photo.jpg" alt="Photo" style="aspect-ratio: 4/3; width: 100%;">
```

```css
/* Reserve space with aspect-ratio */
.image-container {
    aspect-ratio: 16 / 9;
    width: 100%;
    background-color: var(--bg-placeholder);
}

.image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
```

#### 2. Reserve Space for Dynamic Content

```html
<!-- templates/patients/list.html -->

<!-- Reserve space for patient cards that load via API -->
<div id="patient-list" class="patient-grid" style="min-height: 600px;">
    <!-- Skeleton placeholders -->
    {% for i in range(6) %}
    <div class="patient-card patient-card--skeleton" aria-hidden="true">
        <div class="skeleton skeleton--avatar"></div>
        <div class="skeleton skeleton--text"></div>
        <div class="skeleton skeleton--text skeleton--short"></div>
    </div>
    {% endfor %}
</div>
```

```css
/* Prevent layout shift when content loads */
.patient-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: var(--spacing-md);
    /* Minimum height prevents collapse */
    min-height: 400px;
}

.patient-card {
    /* Fixed height prevents shift when content varies */
    min-height: 150px;
}
```

#### 3. Optimize Font Loading

```css
/* static/css/base/_typography.css */

/* Use font-display: swap for quick text render */
@font-face {
    font-family: 'Inter';
    src: url('../fonts/inter-var.woff2') format('woff2');
    font-weight: 100 900;
    font-display: swap;
}

/* Size-adjusted fallback to minimize reflow */
@font-face {
    font-family: 'Inter-fallback';
    src: local('Arial');
    ascent-override: 90%;
    descent-override: 22%;
    line-gap-override: 0%;
    size-adjust: 107%;
}

body {
    font-family: 'Inter', 'Inter-fallback', system-ui, sans-serif;
}
```

#### 4. Avoid Layout-Triggering Animations

```css
/* ❌ Bad: Animates layout properties */
.card {
    transition: height 0.3s, width 0.3s, margin 0.3s;
}

.card:hover {
    height: 200px;
    width: 350px;
    margin: 20px;
}

/* ✅ Good: Only animates transform/opacity */
.card {
    transition: transform 0.3s, opacity 0.3s;
}

.card:hover {
    transform: scale(1.05);
}
```

#### 5. Handle Dynamic Content Insertion

```javascript
// static/js/modules/ui/dynamicContent.js

/**
 * Insert content without causing layout shift.
 */

// ❌ Bad: Inserts at top, shifts everything down
function addNotification(message) {
    const container = document.getElementById('notifications');
    container.insertAdjacentHTML('afterbegin', `
        <div class="notification">${message}</div>
    `);
}

// ✅ Good: Fixed position overlay, no shift
function addNotification(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.right = '20px';
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 5000);
}

// ✅ Good: Animate in without shift
function addListItem(item) {
    const container = document.getElementById('list');
    const el = document.createElement('div');
    el.className = 'list-item list-item--entering';
    el.innerHTML = renderItem(item);
    
    // Animate height from 0
    el.style.height = '0';
    el.style.opacity = '0';
    container.appendChild(el);
    
    requestAnimationFrame(() => {
        el.style.height = el.scrollHeight + 'px';
        el.style.opacity = '1';
    });
}
```

---

## 5. Measuring Core Web Vitals

### JavaScript API

```javascript
// static/js/modules/utils/webVitals.js

/**
 * Measure and report Core Web Vitals.
 * @module utils/webVitals
 */

/**
 * Observe and report LCP
 */
export function observeLCP(callback) {
    const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        
        callback({
            metric: 'LCP',
            value: lastEntry.startTime,
            rating: lastEntry.startTime <= 2500 ? 'good' : 
                    lastEntry.startTime <= 4000 ? 'needs-improvement' : 'poor',
            element: lastEntry.element
        });
    });
    
    observer.observe({ type: 'largest-contentful-paint', buffered: true });
}

/**
 * Observe and report CLS
 */
export function observeCLS(callback) {
    let clsValue = 0;
    let clsEntries = [];
    
    const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            if (!entry.hadRecentInput) {
                clsValue += entry.value;
                clsEntries.push(entry);
            }
        }
        
        callback({
            metric: 'CLS',
            value: clsValue,
            rating: clsValue <= 0.1 ? 'good' : 
                    clsValue <= 0.25 ? 'needs-improvement' : 'poor',
            entries: clsEntries
        });
    });
    
    observer.observe({ type: 'layout-shift', buffered: true });
}

/**
 * Observe and report INP
 */
export function observeINP(callback) {
    let maxINP = 0;
    
    const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            // INP considers all interactions
            if (entry.duration > maxINP) {
                maxINP = entry.duration;
                
                callback({
                    metric: 'INP',
                    value: entry.duration,
                    rating: entry.duration <= 200 ? 'good' : 
                            entry.duration <= 500 ? 'needs-improvement' : 'poor',
                    interactionType: entry.name
                });
            }
        }
    });
    
    observer.observe({ type: 'event', buffered: true, durationThreshold: 16 });
}

/**
 * Initialize all Web Vitals observers
 */
export function initWebVitals(onReport) {
    observeLCP(onReport);
    observeCLS(onReport);
    observeINP(onReport);
}

// Usage
initWebVitals((metric) => {
    console.log(`${metric.metric}: ${metric.value.toFixed(2)} (${metric.rating})`);
    
    // Send to analytics
    if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/v1/analytics/vitals', JSON.stringify(metric));
    }
});
```

### Using web-vitals Library

```javascript
// static/js/modules/utils/webVitalsReporter.js

import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

/**
 * Report all web vitals to analytics endpoint.
 */
export function reportWebVitals() {
    const sendToAnalytics = (metric) => {
        const body = JSON.stringify({
            name: metric.name,
            value: metric.value,
            rating: metric.rating,
            id: metric.id,
            navigationType: metric.navigationType,
            delta: metric.delta
        });
        
        // Use sendBeacon for reliable delivery
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/api/v1/analytics/vitals', body);
        } else {
            fetch('/api/v1/analytics/vitals', {
                body,
                method: 'POST',
                keepalive: true
            });
        }
    };
    
    onLCP(sendToAnalytics);
    onINP(sendToAnalytics);
    onCLS(sendToAnalytics);
    onFCP(sendToAnalytics);
    onTTFB(sendToAnalytics);
}
```

---

## 6. Debugging Core Web Vitals

### Chrome DevTools

```javascript
// Console commands for debugging

// Show LCP element
new PerformanceObserver((list) => {
    const entries = list.getEntries();
    console.log('LCP Element:', entries[entries.length - 1].element);
}).observe({ type: 'largest-contentful-paint', buffered: true });

// Show layout shifts
new PerformanceObserver((list) => {
    list.getEntries().forEach(entry => {
        if (!entry.hadRecentInput) {
            console.log('Layout Shift:', entry.value, entry.sources);
        }
    });
}).observe({ type: 'layout-shift', buffered: true });

// Show slow interactions
new PerformanceObserver((list) => {
    list.getEntries().forEach(entry => {
        if (entry.duration > 100) {
            console.log('Slow Interaction:', entry.name, entry.duration);
        }
    });
}).observe({ type: 'event', buffered: true, durationThreshold: 16 });
```

### Visual Debugging Overlay

```javascript
// static/js/modules/debug/vitalsOverlay.js

/**
 * Visual overlay showing CWV in real-time.
 * Only for development!
 */
export function showVitalsOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'vitals-overlay';
    overlay.innerHTML = `
        <style>
            #vitals-overlay {
                position: fixed;
                bottom: 10px;
                left: 10px;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-family: monospace;
                font-size: 12px;
                z-index: 99999;
            }
            .vital { margin: 4px 0; }
            .vital--good { color: #0cce6b; }
            .vital--needs-improvement { color: #ffa400; }
            .vital--poor { color: #ff4e42; }
        </style>
        <div class="vital" id="vital-lcp">LCP: --</div>
        <div class="vital" id="vital-inp">INP: --</div>
        <div class="vital" id="vital-cls">CLS: --</div>
    `;
    document.body.appendChild(overlay);
    
    // Update overlay with metrics
    const updateMetric = (id, value, rating) => {
        const el = document.getElementById(id);
        el.textContent = `${id.replace('vital-', '').toUpperCase()}: ${value}`;
        el.className = `vital vital--${rating}`;
    };
    
    // Observe metrics
    new PerformanceObserver((list) => {
        const entry = list.getEntries().pop();
        updateMetric('vital-lcp', `${entry.startTime.toFixed(0)}ms`,
            entry.startTime <= 2500 ? 'good' : entry.startTime <= 4000 ? 'needs-improvement' : 'poor');
    }).observe({ type: 'largest-contentful-paint', buffered: true });
    
    let cls = 0;
    new PerformanceObserver((list) => {
        list.getEntries().forEach(entry => {
            if (!entry.hadRecentInput) cls += entry.value;
        });
        updateMetric('vital-cls', cls.toFixed(3),
            cls <= 0.1 ? 'good' : cls <= 0.25 ? 'needs-improvement' : 'poor');
    }).observe({ type: 'layout-shift', buffered: true });
}
```

---

## 7. Core Web Vitals Checklist

### LCP Optimization
- [ ] Preload LCP image with `<link rel="preload">`
- [ ] Use `fetchpriority="high"` on LCP element
- [ ] Inline critical CSS
- [ ] Defer non-critical JavaScript
- [ ] Optimize server response time (TTFB < 600ms)
- [ ] Use CDN for static assets
- [ ] Compress images (WebP/AVIF)

### INP Optimization
- [ ] Break up long JavaScript tasks (< 50ms)
- [ ] Use `requestIdleCallback` for non-urgent work
- [ ] Debounce/throttle event handlers
- [ ] Reduce DOM size (< 1500 elements)
- [ ] Defer third-party scripts
- [ ] Use web workers for heavy computation

### CLS Optimization
- [ ] Set width/height on all images
- [ ] Reserve space for dynamic content
- [ ] Use `font-display: swap` with size-adjusted fallback
- [ ] Avoid inserting content above existing content
- [ ] Use transform for animations (not layout properties)
- [ ] Add `aspect-ratio` to media containers

---

## 8. Quick Reference

### Target Metrics

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| LCP | ≤2.5s | ≤4.0s | >4.0s |
| INP | ≤200ms | ≤500ms | >500ms |
| CLS | ≤0.1 | ≤0.25 | >0.25 |
| TTFB | ≤600ms | ≤1.0s | >1.0s |
| FCP | ≤1.8s | ≤3.0s | >3.0s |

### Common Fixes

| Issue | Metric | Fix |
|-------|--------|-----|
| Slow hero image | LCP | Preload, optimize, use WebP |
| FOUT/FOIT | LCP, CLS | font-display: swap, preload fonts |
| Render-blocking CSS | LCP | Inline critical, async rest |
| Heavy JavaScript | INP | Code split, defer, break tasks |
| Images without size | CLS | Add width/height attributes |
| Dynamic ads/embeds | CLS | Reserve space with min-height |
| Slow server | LCP | Cache, CDN, optimize queries |

---

## Related Skills

- [Web Performance](skill-web-performance.md)
- [Asset Optimization](skill-asset-optimization.md)
- [Lazy Loading](skill-lazy-loading.md)
- [CSS Architecture](skill-css-architecture.md)
