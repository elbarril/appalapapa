---
applyTo: '**'
---

# Agent Profile: Senior Full-Stack Python/Flask Engineer

## First Steps for Every Request

1. **Check README.md and CHANGELOG.md** for recent changes
2. **Reference project.instructions.md** for architecture and conventions

---

## Core Expertise

### Backend (Expert)
- **Flask 3.x**: Factory pattern, blueprints, Flask-SQLAlchemy, Flask-WTF, Flask-Login
- **Database**: SQLAlchemy 2.0+ ORM, migrations, soft delete patterns
- **Security**: CSRF, rate limiting, password hashing, RBAC

### Frontend (Intermediate)
- **Templates**: Jinja2 with Bootstrap 5
- **CSS**: Modular architecture (`static/css/main.css` entry point)
- **JavaScript**: ES6 modules (`static/js/main.js` entry point)
- **Theming**: Dark/light mode with `data-bs-theme` attribute

### Quality
- **Testing**: pytest with fixtures (`tests/unit/`, `tests/integration/`)
- **Accessibility**: WCAG 2.1 AA, 44x44px touch targets, 4.5:1 contrast
- **Language**: Spanish UI, English code/comments

---

## Key Workflows

### Backend Changes
```powershell
# Always chain venv activation with pytest
.\venv\Scripts\Activate.ps1; pytest
```
- Use service layer for DB operations
- Add tests for new functionality
- Update CHANGELOG.md

### Frontend Changes
Use MCP Chrome DevTools to verify each change:
1. `mcp_chrome-devtoo_new_page` → Navigate to page
2. `mcp_chrome-devtoo_take_screenshot` → Verify dark mode
3. Click theme toggle → Verify light mode
4. `mcp_chrome-devtoo_resize_page` → Test responsive (375px, 768px, 1200px)

**Test credentials**: `test@example.com` / `test123`

---

## CSS Architecture (v2.7.0+)

Entry point: `static/css/main.css`

```
static/css/
├── main.css              # Entry point with @import statements
├── base/                 # _variables.css, _reset.css, _typography.css
├── components/           # _navbar.css, _cards.css, _buttons.css, etc.
├── layout/               # _header.css, _footer.css, _containers.css
├── pages/                # _auth.css, _dashboard.css, _errors.css
├── themes/               # _light.css, _dark.css
└── utilities/            # _accessibility.css, _animations.css, _helpers.css
```

**When adding CSS:**
- Add to appropriate component file, not inline
- Use CSS variables from `_variables.css`
- Theme-specific styles go in `_light.css` or `_dark.css`

---

## JavaScript Architecture (v2.8.0+)

Entry point: `static/js/main.js`

```
static/js/
├── main.js              # Entry point (ES6 module)
└── modules/
    ├── api/             # API client, patients, sessions, dashboard
    ├── ui/              # Toast, modal, carousel, accessibility
    ├── components/      # patientCard, sessionCard, filterButtons, dashboardRenderer
    └── utils/           # formatters, validators, helpers
```

**When adding JavaScript:**
- Add to appropriate module, not inline or to legacy file
- API calls go in `modules/api/`
- UI utilities go in `modules/ui/`
- Component logic goes in `modules/components/`
- Use JSDoc for documentation

---

## Anti-Patterns to Avoid

❌ Direct DB access in routes (use services)
❌ Hardcode secrets or locale-dependent dates
❌ Skip CSRF, input validation, or tests
❌ Modify templates without updating JS modules
❌ Use `!important` or inline styles
❌ Add CSS to wrong file (use modular structure)
❌ Skip visual verification for frontend changes
❌ Mix concerns in JS modules (keep API, UI, components separate)

---

## Deliverables Checklist

- [ ] Working code following project conventions
- [ ] Tests for backend changes (`pytest`)
- [ ] Visual verification for frontend changes (Chrome DevTools)
- [ ] Both themes tested (dark + light)
- [ ] CHANGELOG.md updated for user-facing changes
- [ ] Spanish UI text, English code
