# Frontend Contributing Guidelines

This document provides guidelines for contributing to the frontend of the Therapy Session Management Application.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for Playwright tests)
- VS Code (recommended)

### Setup

1. Clone the repository:
   ```powershell
   git clone <repo-url>
   cd appalapapa
   ```

2. Create and activate virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Start development server:
   ```powershell
   flask run
   ```

5. Open browser at `http://localhost:5000`

---

## Development Workflow

### Before Making Changes

1. **Pull latest changes**:
   ```powershell
   git pull origin main
   ```

2. **Create a feature branch**:
   ```powershell
   git checkout -b feature/your-feature-name
   ```

3. **Check README.md and CHANGELOG.md** for recent updates

### Making CSS Changes

1. Identify the correct component file in `static/css/components/`
2. Use CSS variables from `base/_variables.css`
3. Follow BEM naming convention
4. Test in both dark and light themes
5. Verify responsive design at 375px, 768px, 1200px

**File locations:**
| Change Type | File |
|-------------|------|
| Colors/spacing | `base/_variables.css` |
| Buttons | `components/_buttons.css` |
| Cards | `components/_cards.css` |
| Forms | `components/_forms.css` |
| Modals | `components/_modals.css` |
| Theme colors | `themes/_dark.css` or `themes/_light.css` |

### Making JavaScript Changes

1. Identify the correct module in `static/js/modules/`
2. Add JSDoc documentation to all functions
3. Use event delegation when possible
4. Handle errors gracefully with try-catch
5. Update any affected templates

**File locations:**
| Change Type | File |
|-------------|------|
| API calls | `modules/api/*.js` |
| Toast/Modal | `modules/ui/*.js` |
| Patient/Session UI | `modules/components/*.js` |
| Formatting | `modules/utils/formatters.js` |

### Making Template Changes

1. Use macros from `templates/macros/` when possible
2. Follow accessibility guidelines (ARIA attributes)
3. Use `data-*` attributes for JavaScript hooks
4. Keep templates focused and small
5. Update JavaScript if HTML structure changes

**Important:** Template changes often require JavaScript updates. Check:
- `static/js/modules/components/` for component rendering
- `static/js/modules/api/` for data fetching

---

## Verification Checklist

### Visual Verification

Before committing, verify each change:

1. **Dark mode screenshot** at desktop viewport
2. **Light mode screenshot** (click theme toggle)
3. **Mobile viewport** (375px width)
4. **Tablet viewport** (768px width)
5. **Desktop viewport** (1200px width)

### Accessibility Checks

- [ ] Tab through all interactive elements
- [ ] Verify focus indicators are visible
- [ ] Check ARIA labels on buttons without text
- [ ] Verify form labels are linked to inputs
- [ ] Check color contrast with browser DevTools

### Code Quality

- [ ] No `console.log()` statements (use `console.error()` for errors only)
- [ ] No hardcoded colors (use CSS variables)
- [ ] No `!important` (except in utilities)
- [ ] JSDoc on all JavaScript functions
- [ ] Spanish text for UI, English for code comments

---

## Testing

### Running Backend Tests

```powershell
.\venv\Scripts\Activate.ps1; pytest
```

### Running Frontend Tests (Playwright)

```powershell
# Install Playwright browsers (first time only)
playwright install chromium

# Run frontend tests
pytest tests/frontend/ -v
```

### Test Categories

| Directory | Purpose |
|-----------|---------|
| `tests/unit/` | Unit tests for models, services |
| `tests/integration/` | API and route tests |
| `tests/frontend/` | Visual, accessibility, interaction tests |

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `style`: CSS/visual changes
- `refactor`: Code restructuring
- `docs`: Documentation
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(dashboard): add patient search filter
fix(carousel): correct keyboard navigation
style(cards): improve badge contrast in light mode
docs(frontend): update CSS component documentation
```

### When to Update CHANGELOG

Update `CHANGELOG.md` for:
- New features
- Bug fixes affecting users
- Breaking changes
- Visual/UX improvements

---

## Pull Request Process

### Before Submitting

1. Run all tests:
   ```powershell
   .\venv\Scripts\Activate.ps1; pytest
   ```

2. Check for linting errors:
   ```powershell
   flake8 app/
   ```

3. Verify no console errors in browser

4. Take screenshots for visual changes

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Style/visual change
- [ ] Refactor
- [ ] Documentation

## Screenshots (if visual change)
| Dark Mode | Light Mode |
|-----------|------------|
| ![dark]() | ![light]() |

## Checklist
- [ ] Tests pass
- [ ] Both themes tested
- [ ] Responsive design verified
- [ ] Accessibility checked
- [ ] CHANGELOG updated (if applicable)
```

### Review Process

1. Submit PR with screenshots
2. Address review feedback
3. Merge after approval

---

## Common Issues

### CSS Not Updating

1. Clear browser cache (Ctrl+Shift+R)
2. Check import in `main.css`
3. Verify file path is correct

### JavaScript Changes Not Working

1. Clear browser cache
2. Check browser console for errors
3. Verify module imports
4. Check if function is exported to `window` (for onclick handlers)

### Theme Colors Wrong

1. Use CSS variables, not hardcoded colors
2. Add overrides in `themes/_light.css` or `themes/_dark.css`
3. Test both themes

---

## Resources

### Documentation

- [CSS Components](./css-components.md)
- [JavaScript Modules](./js-modules.md)
- [Template Macros](./template-macros.md)
- [Style Guide](./frontend-style-guide.md)

### External Resources

- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [BEM Methodology](https://getbem.com/)
- [Playwright Docs](https://playwright.dev/docs/intro)

---

## Questions?

If you have questions:
1. Check existing documentation
2. Review similar existing code
3. Ask in project discussions

---

*Last Updated: January 15, 2026*
