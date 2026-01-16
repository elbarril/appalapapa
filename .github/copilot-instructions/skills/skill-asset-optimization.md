# Skill: Asset Optimization

> **Scope:** Image, CSS, and JavaScript optimization strategies for Flask/Jinja2 web applications to minimize file sizes and improve load times.

---

## 1. Image Optimization

### Image Format Selection

| Format | Best For | Compression | Browser Support |
|--------|----------|-------------|-----------------|
| **AVIF** | Photos, graphics | Best (50% smaller than JPEG) | Modern browsers |
| **WebP** | Photos, graphics | Great (25-35% smaller) | All modern browsers |
| **JPEG** | Photos | Good | Universal |
| **PNG** | Graphics with transparency | Lossless | Universal |
| **SVG** | Icons, logos, illustrations | Vector (scales) | Universal |

### Image Optimization Pipeline

```python
# scripts/optimize_images.py

from PIL import Image
import os
from pathlib import Path

class ImageOptimizer:
    """Optimize images for web delivery."""
    
    QUALITY_SETTINGS = {
        'high': {'jpeg': 85, 'webp': 82, 'avif': 80},
        'medium': {'jpeg': 75, 'webp': 72, 'avif': 65},
        'low': {'jpeg': 60, 'webp': 55, 'avif': 50}
    }
    
    SIZES = [320, 640, 960, 1280, 1920]
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def optimize_image(self, filepath: Path, quality: str = 'medium'):
        """Optimize a single image to multiple formats and sizes."""
        with Image.open(filepath) as img:
            # Convert to RGB if necessary (for JPEG)
            if img.mode in ('RGBA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[3])
                else:
                    rgb_img.paste(img)
            else:
                rgb_img = img.convert('RGB')
            
            base_name = filepath.stem
            settings = self.QUALITY_SETTINGS[quality]
            
            for width in self.SIZES:
                if width > img.width:
                    continue
                
                # Calculate height maintaining aspect ratio
                ratio = width / img.width
                height = int(img.height * ratio)
                resized = rgb_img.resize((width, height), Image.LANCZOS)
                
                # Save JPEG
                jpeg_path = self.output_dir / f"{base_name}-{width}w.jpg"
                resized.save(jpeg_path, 'JPEG', quality=settings['jpeg'], optimize=True)
                
                # Save WebP
                webp_path = self.output_dir / f"{base_name}-{width}w.webp"
                resized.save(webp_path, 'WebP', quality=settings['webp'])
                
                # Save AVIF (requires pillow-avif-plugin)
                try:
                    avif_path = self.output_dir / f"{base_name}-{width}w.avif"
                    resized.save(avif_path, 'AVIF', quality=settings['avif'])
                except Exception:
                    pass  # AVIF not supported
    
    def process_directory(self, quality: str = 'medium'):
        """Process all images in input directory."""
        extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        
        for filepath in self.input_dir.iterdir():
            if filepath.suffix.lower() in extensions:
                print(f"Optimizing: {filepath.name}")
                self.optimize_image(filepath, quality)


# Usage
if __name__ == '__main__':
    optimizer = ImageOptimizer(
        input_dir='static/images/originals',
        output_dir='static/images/optimized'
    )
    optimizer.process_directory(quality='medium')
```

### Responsive Image Template Macro

```html
<!-- templates/macros/_images.html -->

{% macro picture(
    src,
    alt,
    widths=[320, 640, 960, 1280],
    sizes='100vw',
    loading='lazy',
    class_name='',
    aspect_ratio=none
) %}
{#
    Responsive picture element with modern format support.
    
    Parameters:
        src (str): Base image filename (without extension)
        alt (str): Alt text for accessibility
        widths (list): Available image widths
        sizes (str): Sizes attribute for responsive selection
        loading (str): 'lazy' or 'eager'
        class_name (str): CSS classes for img element
        aspect_ratio (str): Optional aspect ratio (e.g., '16/9')
#}
{% set base_path = 'images/optimized/' %}
<picture>
    {# AVIF sources - best compression #}
    <source 
        type="image/avif"
        srcset="{% for w in widths %}{{ url_for('static', filename=base_path + src + '-' + w|string + 'w.avif') }} {{ w }}w{% if not loop.last %}, {% endif %}{% endfor %}"
        sizes="{{ sizes }}">
    
    {# WebP sources - good compression, wide support #}
    <source 
        type="image/webp"
        srcset="{% for w in widths %}{{ url_for('static', filename=base_path + src + '-' + w|string + 'w.webp') }} {{ w }}w{% if not loop.last %}, {% endif %}{% endfor %}"
        sizes="{{ sizes }}">
    
    {# JPEG fallback #}
    <img 
        src="{{ url_for('static', filename=base_path + src + '-' + widths[-1]|string + 'w.jpg') }}"
        srcset="{% for w in widths %}{{ url_for('static', filename=base_path + src + '-' + w|string + 'w.jpg') }} {{ w }}w{% if not loop.last %}, {% endif %}{% endfor %}"
        sizes="{{ sizes }}"
        alt="{{ alt }}"
        loading="{{ loading }}"
        decoding="async"
        class="{{ class_name }}"
        {% if aspect_ratio %}style="aspect-ratio: {{ aspect_ratio }}"{% endif %}>
</picture>
{% endmacro %}


{% macro svg_icon(name, size=24, class_name='', aria_label=none) %}
{#
    Inline SVG icon from sprite.
    
    Parameters:
        name (str): Icon name in sprite
        size (int): Icon size in pixels
        class_name (str): Additional CSS classes
        aria_label (str): Accessible label (if interactive)
#}
<svg 
    class="icon {{ class_name }}"
    width="{{ size }}"
    height="{{ size }}"
    {% if aria_label %}
    role="img"
    aria-label="{{ aria_label }}"
    {% else %}
    aria-hidden="true"
    {% endif %}>
    <use href="{{ url_for('static', filename='images/icons.svg') }}#{{ name }}"></use>
</svg>
{% endmacro %}
```

### SVG Sprite Generation

```python
# scripts/generate_svg_sprite.py

import os
from pathlib import Path
import re

def generate_svg_sprite(icons_dir: str, output_file: str):
    """Combine individual SVG icons into a single sprite."""
    icons_path = Path(icons_dir)
    symbols = []
    
    for svg_file in sorted(icons_path.glob('*.svg')):
        icon_name = svg_file.stem
        content = svg_file.read_text()
        
        # Extract viewBox
        viewbox_match = re.search(r'viewBox="([^"]+)"', content)
        viewbox = viewbox_match.group(1) if viewbox_match else '0 0 24 24'
        
        # Extract path content
        path_match = re.search(r'<svg[^>]*>(.*)</svg>', content, re.DOTALL)
        if path_match:
            inner_content = path_match.group(1).strip()
            symbols.append(f'''  <symbol id="{icon_name}" viewBox="{viewbox}">
    {inner_content}
  </symbol>''')
    
    sprite = f'''<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
{chr(10).join(symbols)}
</svg>'''
    
    Path(output_file).write_text(sprite)
    print(f"Generated sprite with {len(symbols)} icons: {output_file}")


if __name__ == '__main__':
    generate_svg_sprite(
        icons_dir='static/images/icons',
        output_file='static/images/icons.svg'
    )
```

---

## 2. CSS Optimization

### CSS Minification

```python
# scripts/build_css.py

import csscompressor
from pathlib import Path
import re


def minify_css(input_file: str, output_file: str):
    """Minify CSS file."""
    content = Path(input_file).read_text()
    minified = csscompressor.compress(content)
    Path(output_file).write_text(minified)
    
    original_size = len(content)
    minified_size = len(minified)
    savings = (1 - minified_size / original_size) * 100
    
    print(f"CSS: {original_size:,} → {minified_size:,} bytes ({savings:.1f}% reduction)")


def combine_css_files(input_dir: str, output_file: str, order: list = None):
    """Combine multiple CSS files into one."""
    css_dir = Path(input_dir)
    combined = []
    
    if order:
        files = [css_dir / f for f in order if (css_dir / f).exists()]
    else:
        files = sorted(css_dir.glob('*.css'))
    
    for css_file in files:
        content = css_file.read_text()
        # Remove @import statements (already combined)
        content = re.sub(r'@import\s+[^;]+;', '', content)
        combined.append(f"/* === {css_file.name} === */\n{content}")
    
    Path(output_file).write_text('\n\n'.join(combined))
    print(f"Combined {len(files)} CSS files into {output_file}")


# Build pipeline
if __name__ == '__main__':
    # Combine CSS files
    combine_css_files(
        'static/css',
        'static/dist/combined.css',
        order=['base/_variables.css', 'base/_reset.css', 'components/_buttons.css']
    )
    
    # Minify
    minify_css('static/dist/combined.css', 'static/dist/main.min.css')
```

### Remove Unused CSS (PurgeCSS)

```javascript
// purgecss.config.js

module.exports = {
    content: [
        'templates/**/*.html',
        'static/js/**/*.js'
    ],
    css: ['static/css/main.css'],
    output: 'static/dist/',
    safelist: {
        // Keep dynamically added classes
        standard: [
            /^modal/,
            /^toast/,
            /^alert/,
            /^carousel/,
            /^show$/,
            /^fade$/,
            /^active$/,
            /^disabled$/
        ],
        // Keep classes with these patterns
        deep: [
            /data-bs-theme/
        ]
    },
    // Remove unused keyframes
    keyframes: true,
    // Remove unused font-face
    fontFace: true
};
```

```json
// package.json scripts
{
    "scripts": {
        "css:purge": "purgecss --config purgecss.config.js",
        "css:minify": "cleancss -o static/dist/main.min.css static/dist/main.css",
        "css:build": "npm run css:purge && npm run css:minify"
    }
}
```

### Critical CSS Extraction

```python
# scripts/extract_critical_css.py

"""
Extract critical CSS for above-the-fold content.
Uses penthouse or critical npm packages.
"""

import subprocess
import json
from pathlib import Path


def extract_critical_css(url: str, output_file: str, width: int = 1300, height: int = 900):
    """Extract critical CSS using penthouse."""
    
    # penthouse must be installed: npm install -g penthouse
    result = subprocess.run([
        'penthouse',
        url,
        'static/css/main.css',
        '--width', str(width),
        '--height', str(height),
        '--forceInclude', '.navbar,.container,.card'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        Path(output_file).write_text(result.stdout)
        print(f"Critical CSS extracted: {len(result.stdout)} bytes")
    else:
        print(f"Error: {result.stderr}")


# Generate critical CSS for key pages
PAGES = [
    ('http://localhost:5000/', 'static/dist/critical-home.css'),
    ('http://localhost:5000/login', 'static/dist/critical-login.css'),
]

if __name__ == '__main__':
    for url, output in PAGES:
        extract_critical_css(url, output)
```

### CSS Variable Optimization

```css
/* static/css/base/_variables.css */

:root {
    /* 
     * Design tokens - single source of truth
     * Reduces CSS size by avoiding repeated values
     */
    
    /* Color palette */
    --color-teal-50: #f0f4f4;
    --color-teal-100: #d1dddc;
    --color-teal-500: #3F4A49;
    --color-teal-600: #2d3635;
    --color-teal-700: #1f2524;
    
    /* Semantic colors - reference palette */
    --color-primary: var(--color-teal-500);
    --color-primary-hover: var(--color-teal-600);
    --color-primary-active: var(--color-teal-700);
    
    /* Spacing scale - consistent rhythm */
    --space-unit: 0.25rem;
    --space-1: calc(var(--space-unit) * 1);   /* 4px */
    --space-2: calc(var(--space-unit) * 2);   /* 8px */
    --space-3: calc(var(--space-unit) * 3);   /* 12px */
    --space-4: calc(var(--space-unit) * 4);   /* 16px */
    --space-6: calc(var(--space-unit) * 6);   /* 24px */
    --space-8: calc(var(--space-unit) * 8);   /* 32px */
    
    /* Typography - modular scale */
    --text-base: 1rem;
    --text-scale: 1.25;
    --text-sm: calc(var(--text-base) / var(--text-scale));
    --text-lg: calc(var(--text-base) * var(--text-scale));
    --text-xl: calc(var(--text-lg) * var(--text-scale));
    --text-2xl: calc(var(--text-xl) * var(--text-scale));
}
```

---

## 3. JavaScript Optimization

### Bundle Size Analysis

```javascript
// webpack.config.js - with bundle analyzer

const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
    plugins: [
        new BundleAnalyzerPlugin({
            analyzerMode: 'static',
            reportFilename: 'bundle-report.html',
            openAnalyzer: false
        })
    ]
};
```

### Tree Shaking

```javascript
// ❌ Bad: Import entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ Good: Import only what you need
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// ✅ Better: Use native or lightweight alternatives
function debounce(fn, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn.apply(this, args), wait);
    };
}
```

### Code Splitting

```javascript
// static/js/main.js - Dynamic imports

/**
 * Load modules on demand based on page needs
 */
async function initializeApp() {
    // Core modules - always loaded
    const { initTheme } = await import('./modules/ui/theme.js');
    initTheme();
    
    // Conditional loading based on page content
    const pageModules = {
        // Dashboard page
        '[data-page="dashboard"]': () => import('./modules/components/dashboardRenderer.js'),
        
        // Forms
        'form[data-validate]': () => import('./modules/utils/validators.js'),
        
        // Modals
        '[data-modal-trigger]': () => import('./modules/ui/modal.js'),
        
        // Carousels
        '.carousel': () => import('./modules/ui/carousel.js'),
        
        // Charts
        '[data-chart]': () => import('./modules/components/charts.js')
    };
    
    // Load only needed modules
    for (const [selector, loader] of Object.entries(pageModules)) {
        if (document.querySelector(selector)) {
            const module = await loader();
            module.init?.();
        }
    }
}

// Start when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
```

### Minification

```javascript
// scripts/build-js.mjs

import { minify } from 'terser';
import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, basename } from 'path';

const JS_DIR = 'static/js';
const DIST_DIR = 'static/dist';

async function minifyFile(inputPath, outputPath) {
    const code = readFileSync(inputPath, 'utf8');
    
    const result = await minify(code, {
        compress: {
            dead_code: true,
            drop_console: true,  // Remove console.log in production
            drop_debugger: true,
            passes: 2
        },
        mangle: {
            toplevel: true
        },
        format: {
            comments: false
        },
        sourceMap: {
            filename: basename(outputPath),
            url: basename(outputPath) + '.map'
        }
    });
    
    writeFileSync(outputPath, result.code);
    if (result.map) {
        writeFileSync(outputPath + '.map', result.map);
    }
    
    const originalSize = code.length;
    const minifiedSize = result.code.length;
    const savings = ((1 - minifiedSize / originalSize) * 100).toFixed(1);
    
    console.log(`${basename(inputPath)}: ${originalSize} → ${minifiedSize} bytes (${savings}% reduction)`);
}

// Process all JS files
const files = readdirSync(JS_DIR).filter(f => f.endsWith('.js'));
for (const file of files) {
    await minifyFile(
        join(JS_DIR, file),
        join(DIST_DIR, file.replace('.js', '.min.js'))
    );
}
```

### Remove Dead Code

```javascript
// static/js/modules/utils/helpers.js

/**
 * Utilities that are actually used in the codebase.
 * Regularly audit and remove unused functions.
 */

// ✅ Used - keep
export function formatCurrency(amount) {
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS'
    }).format(amount);
}

// ✅ Used - keep
export function debounce(fn, wait = 300) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn.apply(this, args), wait);
    };
}

// ❌ Unused - remove
// export function deprecatedHelper() { ... }
```

---

## 4. Build Pipeline

### Complete Build Script

```python
# scripts/build.py

"""
Asset build pipeline for production.
Optimizes images, CSS, and JavaScript.
"""

import subprocess
import shutil
from pathlib import Path
import hashlib
import json


class AssetBuilder:
    """Build and optimize all static assets."""
    
    def __init__(self):
        self.static_dir = Path('static')
        self.dist_dir = self.static_dir / 'dist'
        self.manifest = {}
    
    def clean(self):
        """Remove old build artifacts."""
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.dist_dir.mkdir(parents=True)
        print("✓ Cleaned dist directory")
    
    def build_css(self):
        """Build and minify CSS."""
        # Combine CSS files
        css_files = [
            'css/base/_variables.css',
            'css/base/_reset.css',
            'css/base/_typography.css',
            'css/components/_buttons.css',
            'css/components/_cards.css',
            'css/components/_forms.css',
            'css/components/_navbar.css',
            'css/components/_modals.css',
            'css/layout/_containers.css',
            'css/themes/_dark.css',
            'css/themes/_light.css',
            'css/utilities/_accessibility.css',
        ]
        
        combined = []
        for css_file in css_files:
            path = self.static_dir / css_file
            if path.exists():
                combined.append(path.read_text())
        
        combined_css = '\n'.join(combined)
        
        # Minify (using csscompressor if available)
        try:
            import csscompressor
            minified = csscompressor.compress(combined_css)
        except ImportError:
            minified = combined_css
        
        # Write with hash
        css_hash = hashlib.md5(minified.encode()).hexdigest()[:8]
        output_file = self.dist_dir / f'main.{css_hash}.css'
        output_file.write_text(minified)
        
        self.manifest['css/main.css'] = f'dist/main.{css_hash}.css'
        print(f"✓ Built CSS: {len(combined_css)} → {len(minified)} bytes")
    
    def build_js(self):
        """Build and minify JavaScript."""
        # For simple projects, just copy and minify main.js
        main_js = self.static_dir / 'js' / 'main.js'
        
        if main_js.exists():
            content = main_js.read_text()
            
            # Simple minification (remove comments, extra whitespace)
            # For production, use terser via subprocess
            try:
                result = subprocess.run(
                    ['npx', 'terser', str(main_js), '--compress', '--mangle'],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    minified = result.stdout
                else:
                    minified = content
            except Exception:
                minified = content
            
            js_hash = hashlib.md5(minified.encode()).hexdigest()[:8]
            output_file = self.dist_dir / f'main.{js_hash}.js'
            output_file.write_text(minified)
            
            self.manifest['js/main.js'] = f'dist/main.{js_hash}.js'
            print(f"✓ Built JS: {len(content)} → {len(minified)} bytes")
    
    def generate_manifest(self):
        """Generate asset manifest for cache busting."""
        manifest_file = self.dist_dir / 'manifest.json'
        manifest_file.write_text(json.dumps(self.manifest, indent=2))
        print(f"✓ Generated manifest with {len(self.manifest)} entries")
    
    def build(self):
        """Run complete build pipeline."""
        print("Building assets...")
        self.clean()
        self.build_css()
        self.build_js()
        self.generate_manifest()
        print("Build complete!")


if __name__ == '__main__':
    builder = AssetBuilder()
    builder.build()
```

### Flask Asset Loading

```python
# app/utils/assets.py

import json
from pathlib import Path
from flask import current_app


def get_asset_manifest():
    """Load asset manifest for cache-busted URLs."""
    manifest_path = Path(current_app.static_folder) / 'dist' / 'manifest.json'
    
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())
    return {}


def asset_url(filename: str) -> str:
    """Get cache-busted URL for an asset."""
    manifest = get_asset_manifest()
    
    # Return hashed version if available
    if filename in manifest:
        return f"/static/{manifest[filename]}"
    
    # Fallback to original
    return f"/static/{filename}"


# Register as Jinja2 function
def init_asset_helpers(app):
    """Register asset helpers with Jinja2."""
    app.jinja_env.globals['asset_url'] = asset_url
```

```html
<!-- templates/base.html -->
<head>
    <!-- Use cache-busted URLs -->
    <link rel="stylesheet" href="{{ asset_url('css/main.css') }}">
</head>
<body>
    <!-- ... -->
    <script src="{{ asset_url('js/main.js') }}" type="module"></script>
</body>
```

---

## 5. Compression

### Server-Side Compression

```python
# app/middleware/compression.py

from flask import Flask
from flask_compress import Compress

compress = Compress()


def init_compression(app: Flask):
    """Initialize response compression."""
    
    # Compression settings
    app.config['COMPRESS_MIMETYPES'] = [
        'text/html',
        'text/css',
        'text/javascript',
        'application/javascript',
        'application/json',
        'application/xml',
        'image/svg+xml'
    ]
    app.config['COMPRESS_LEVEL'] = 6  # Balance speed vs compression
    app.config['COMPRESS_MIN_SIZE'] = 500  # Only compress > 500 bytes
    
    compress.init_app(app)
```

### Nginx Compression Config

```nginx
# nginx.conf

# Enable gzip
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_min_length 256;
gzip_types
    text/plain
    text/css
    text/javascript
    application/javascript
    application/json
    application/xml
    image/svg+xml;

# Enable Brotli (if module available)
brotli on;
brotli_comp_level 6;
brotli_types
    text/plain
    text/css
    text/javascript
    application/javascript
    application/json;
```

---

## 6. Asset Optimization Checklist

### Images
- [ ] Use appropriate format (AVIF > WebP > JPEG/PNG)
- [ ] Generate responsive sizes (srcset)
- [ ] Compress images (quality 60-85%)
- [ ] Use SVG sprites for icons
- [ ] Set explicit width/height attributes
- [ ] Lazy load below-fold images

### CSS
- [ ] Remove unused CSS (PurgeCSS)
- [ ] Minify CSS files
- [ ] Extract critical CSS
- [ ] Use CSS variables for theming
- [ ] Combine files in production
- [ ] Enable compression

### JavaScript
- [ ] Tree shake unused code
- [ ] Code split by route/feature
- [ ] Minify with terser
- [ ] Remove console.log in production
- [ ] Use dynamic imports
- [ ] Enable compression

### General
- [ ] Generate asset manifest
- [ ] Use cache-busting hashes
- [ ] Set proper cache headers
- [ ] Enable Brotli/Gzip compression
- [ ] Monitor bundle sizes

---

## 7. Size Budgets

| Asset Type | Budget | Warning |
|------------|--------|---------|
| **Total CSS** | 50KB | 75KB |
| **Critical CSS** | 14KB | 20KB |
| **Total JS** | 200KB | 300KB |
| **Main bundle** | 100KB | 150KB |
| **Per chunk** | 50KB | 75KB |
| **Hero image** | 100KB | 150KB |
| **Thumbnail** | 30KB | 50KB |
| **Icon sprite** | 20KB | 30KB |

---

## Related Skills

- [Web Performance](skill-web-performance.md)
- [Lazy Loading](skill-lazy-loading.md)
- [CSS Architecture](skill-css-architecture.md)
- [JavaScript Modules](skill-javascript-modules.md)
