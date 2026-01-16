# Skill: Frontend Testing

> **Scope:** Testing strategies, tools, and patterns for frontend code in Flask/Jinja2 web applications, including visual testing with Chrome DevTools.

---

## 1. Frontend Testing Pyramid

```
        /\
       /  \     E2E Tests (Playwright, Cypress)
      /    \    - Full user flows
     /------\   - Critical paths only
    /        \  
   / Visual   \ Visual Regression
  /  Tests     \ - Screenshot comparison
 /--------------\ - Layout verification
/                \
/ Integration     \ Integration Tests
/   Tests          \ - API endpoints
/------------------\ - Form submissions
/                    \
/ Component Tests     \ Component/Unit Tests
/   (JavaScript)       \ - Individual functions
/------------------------\ - Module behavior
```

### Testing Distribution

| Test Type | Coverage | Speed | Cost |
|-----------|----------|-------|------|
| Unit/Component | 60-70% | Fast | Low |
| Integration | 20-30% | Medium | Medium |
| Visual | 5-10% | Medium | Medium |
| E2E | 5-10% | Slow | High |

---

## 2. JavaScript Unit Testing

### Test Setup with Jest

```javascript
// jest.config.js
module.exports = {
    testEnvironment: 'jsdom',
    moduleFileExtensions: ['js', 'mjs'],
    testMatch: ['**/tests/**/*.test.js'],
    setupFilesAfterEnv: ['./tests/setup.js'],
    collectCoverageFrom: [
        'static/js/modules/**/*.js',
        '!static/js/modules/**/*.test.js'
    ],
    coverageThreshold: {
        global: {
            branches: 80,
            functions: 80,
            lines: 80,
            statements: 80
        }
    }
};
```

```javascript
// tests/setup.js
import '@testing-library/jest-dom';

// Mock fetch
global.fetch = jest.fn();

// Mock localStorage
const localStorageMock = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    removeItem: jest.fn(),
    clear: jest.fn()
};
global.localStorage = localStorageMock;

// Reset mocks before each test
beforeEach(() => {
    jest.clearAllMocks();
    document.body.innerHTML = '';
});
```

### Testing Utility Functions

```javascript
// static/js/modules/utils/formatters.test.js

import { formatCurrency, formatDate, formatDisplayDate } from './formatters.js';

describe('formatCurrency', () => {
    test('formats positive numbers correctly', () => {
        expect(formatCurrency(1500)).toBe('$1.500,00');
        expect(formatCurrency(0)).toBe('$0,00');
        expect(formatCurrency(99.99)).toBe('$99,99');
    });
    
    test('handles negative numbers', () => {
        expect(formatCurrency(-500)).toBe('-$500,00');
    });
    
    test('handles null/undefined', () => {
        expect(formatCurrency(null)).toBe('$0,00');
        expect(formatCurrency(undefined)).toBe('$0,00');
    });
});

describe('formatDisplayDate', () => {
    test('formats ISO date to Spanish format', () => {
        expect(formatDisplayDate('2024-01-15')).toBe('Lunes 15/01/2024');
        expect(formatDisplayDate('2024-12-25')).toBe('Miércoles 25/12/2024');
    });
    
    test('handles invalid dates', () => {
        expect(formatDisplayDate('invalid')).toBe('Fecha inválida');
        expect(formatDisplayDate('')).toBe('Fecha inválida');
    });
});
```

### Testing API Functions

```javascript
// static/js/modules/api/patients.test.js

import { fetchPatients, createPatient, deletePatient } from './patients.js';

describe('Patient API', () => {
    beforeEach(() => {
        global.fetch = jest.fn();
    });
    
    describe('fetchPatients', () => {
        test('fetches patients successfully', async () => {
            const mockPatients = [
                { id: 1, name: 'Juan Pérez' },
                { id: 2, name: 'María García' }
            ];
            
            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ patients: mockPatients })
            });
            
            const result = await fetchPatients();
            
            expect(fetch).toHaveBeenCalledWith('/api/v1/patients?page=1&per_page=20');
            expect(result.patients).toEqual(mockPatients);
        });
        
        test('handles fetch errors', async () => {
            fetch.mockResolvedValueOnce({
                ok: false,
                status: 500
            });
            
            await expect(fetchPatients()).rejects.toThrow('Failed to fetch patients');
        });
        
        test('handles network errors', async () => {
            fetch.mockRejectedValueOnce(new Error('Network error'));
            
            await expect(fetchPatients()).rejects.toThrow('Network error');
        });
    });
    
    describe('createPatient', () => {
        test('sends correct data', async () => {
            const patientData = { name: 'Test Patient', phone: '123456789' };
            
            fetch.mockResolvedValueOnce({
                ok: true,
                json: () => Promise.resolve({ id: 1, ...patientData })
            });
            
            await createPatient(patientData);
            
            expect(fetch).toHaveBeenCalledWith('/api/v1/patients', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(patientData)
            });
        });
    });
});
```

### Testing DOM Manipulation

```javascript
// static/js/modules/ui/toast.test.js

import { showToast, hideToast, initToasts } from './toast.js';

describe('Toast Notifications', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="toast-container" aria-live="polite"></div>
        `;
        initToasts();
    });
    
    test('shows toast with message', () => {
        showToast('Test message', 'success');
        
        const toast = document.querySelector('.toast');
        expect(toast).toBeInTheDocument();
        expect(toast).toHaveTextContent('Test message');
        expect(toast).toHaveClass('toast--success');
    });
    
    test('toast has correct ARIA attributes', () => {
        showToast('Accessible message', 'info');
        
        const toast = document.querySelector('.toast');
        expect(toast).toHaveAttribute('role', 'status');
        expect(toast).toHaveAttribute('aria-live', 'polite');
    });
    
    test('auto-hides toast after timeout', () => {
        jest.useFakeTimers();
        
        showToast('Auto-hide test', 'info', { duration: 3000 });
        
        expect(document.querySelector('.toast')).toBeInTheDocument();
        
        jest.advanceTimersByTime(3000);
        
        expect(document.querySelector('.toast')).not.toBeInTheDocument();
        
        jest.useRealTimers();
    });
    
    test('can manually dismiss toast', () => {
        showToast('Dismissable', 'info');
        
        const closeBtn = document.querySelector('.toast__close');
        closeBtn.click();
        
        expect(document.querySelector('.toast')).not.toBeInTheDocument();
    });
});
```

---

## 3. Visual Testing with Chrome DevTools MCP

### Basic Visual Verification

```python
# Use Chrome DevTools MCP for visual testing

# 1. Navigate to page
# mcp_chrome-devtoo_new_page → http://localhost:5000/

# 2. Take screenshot
# mcp_chrome-devtoo_take_screenshot

# 3. Get page snapshot for element verification
# mcp_chrome-devtoo_take_page_content_snapshot
```

### Theme Testing Workflow

```markdown
## Visual Testing Checklist

### Dark Mode (Default)
1. Navigate: `mcp_chrome-devtoo_new_page` → `http://localhost:5000/login`
2. Screenshot: `mcp_chrome-devtoo_take_screenshot`
3. Verify:
   - Background is dark (#1a1d1f)
   - Text is light (#e5e5e5)
   - Buttons are visible
   - Form fields have proper contrast

### Light Mode
4. Get snapshot: `mcp_chrome-devtoo_take_page_content_snapshot`
5. Find theme toggle button UID
6. Click: `mcp_chrome-devtoo_click` with toggle UID
7. Screenshot: `mcp_chrome-devtoo_take_screenshot`
8. Verify:
   - Background is light (#F5F3EF)
   - Text is dark (#3F4A49)
   - All elements visible

### Responsive Testing
9. Resize: `mcp_chrome-devtoo_resize_page` → 375x667 (mobile)
10. Screenshot: `mcp_chrome-devtoo_take_screenshot`
11. Verify mobile layout

12. Resize: `mcp_chrome-devtoo_resize_page` → 768x1024 (tablet)
13. Screenshot: `mcp_chrome-devtoo_take_screenshot`
14. Verify tablet layout
```

### Form Validation Testing

```markdown
## Form Testing with Chrome DevTools

### Test Empty Form Submission
1. Navigate to form page
2. Get snapshot to find submit button
3. Click submit without filling fields
4. Take screenshot - verify error messages

### Test Invalid Input
1. Fill form with invalid data:
   - `mcp_chrome-devtoo_fill` email field with "invalid"
   - `mcp_chrome-devtoo_fill` phone with "abc"
2. Submit form
3. Screenshot - verify validation errors

### Test Valid Submission
1. Fill form correctly:
   - `mcp_chrome-devtoo_fill` name with "Juan Pérez"
   - `mcp_chrome-devtoo_fill` email with "juan@example.com"
2. Submit
3. Verify success message or redirect
```

---

## 4. Integration Testing

### Flask Test Client for Forms

```python
# tests/integration/test_form_submission.py

import pytest
from flask import url_for


class TestPatientForm:
    """Test patient form submission and validation."""
    
    def test_create_patient_valid_data(self, client, auth):
        """Test creating a patient with valid data."""
        auth.login()
        
        response = client.post(
            url_for('patients.create'),
            data={
                'name': 'Test Patient',
                'phone': '1234567890',
                'email': 'test@example.com',
                'notes': 'Test notes'
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert 'Paciente creado exitosamente' in response.data.decode()
    
    def test_create_patient_missing_name(self, client, auth):
        """Test validation error for missing name."""
        auth.login()
        
        response = client.post(
            url_for('patients.create'),
            data={
                'name': '',  # Empty name
                'phone': '1234567890'
            }
        )
        
        assert response.status_code == 200
        assert 'El nombre es requerido' in response.data.decode()
    
    def test_create_patient_invalid_email(self, client, auth):
        """Test validation error for invalid email."""
        auth.login()
        
        response = client.post(
            url_for('patients.create'),
            data={
                'name': 'Test Patient',
                'email': 'not-an-email'
            }
        )
        
        assert response.status_code == 200
        assert 'Email inválido' in response.data.decode()
    
    def test_create_patient_unauthenticated(self, client):
        """Test redirect to login for unauthenticated users."""
        response = client.post(
            url_for('patients.create'),
            data={'name': 'Test'}
        )
        
        assert response.status_code == 302
        assert '/login' in response.location


class TestSessionForm:
    """Test session form submission."""
    
    def test_create_session_valid(self, client, auth, test_patient):
        """Test creating a therapy session."""
        auth.login()
        
        response = client.post(
            url_for('sessions.create', patient_id=test_patient.id),
            data={
                'session_date': '2024-01-15',
                'session_type': 'individual',
                'price': '5000',
                'paid': 'y',
                'notes': 'Session notes'
            },
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert 'Sesión registrada' in response.data.decode()
    
    def test_create_session_future_date(self, client, auth, test_patient):
        """Test validation for future session dates."""
        auth.login()
        
        response = client.post(
            url_for('sessions.create', patient_id=test_patient.id),
            data={
                'session_date': '2030-01-15',  # Future date
                'price': '5000'
            }
        )
        
        assert 'La fecha no puede ser futura' in response.data.decode()
```

### API Integration Tests

```python
# tests/integration/test_api.py

import pytest
import json


class TestPatientAPI:
    """Test patient API endpoints."""
    
    def test_get_patients_list(self, client, auth, test_patients):
        """Test fetching paginated patient list."""
        auth.login()
        
        response = client.get('/api/v1/patients?page=1&per_page=10')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'patients' in data
        assert 'total' in data
        assert len(data['patients']) <= 10
    
    def test_get_patient_detail(self, client, auth, test_patient):
        """Test fetching single patient."""
        auth.login()
        
        response = client.get(f'/api/v1/patients/{test_patient.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == test_patient.name
    
    def test_get_patient_not_found(self, client, auth):
        """Test 404 for non-existent patient."""
        auth.login()
        
        response = client.get('/api/v1/patients/99999')
        
        assert response.status_code == 404
    
    def test_get_patient_unauthorized(self, client, auth, other_user_patient):
        """Test cannot access other user's patient."""
        auth.login()
        
        response = client.get(f'/api/v1/patients/{other_user_patient.id}')
        
        assert response.status_code == 404
    
    def test_create_patient_api(self, client, auth):
        """Test creating patient via API."""
        auth.login()
        
        response = client.post(
            '/api/v1/patients',
            data=json.dumps({'name': 'API Patient', 'phone': '123456'}),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'API Patient'
        assert 'id' in data
    
    def test_update_patient_api(self, client, auth, test_patient):
        """Test updating patient via API."""
        auth.login()
        
        response = client.put(
            f'/api/v1/patients/{test_patient.id}',
            data=json.dumps({'name': 'Updated Name'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Name'
    
    def test_delete_patient_api(self, client, auth, test_patient):
        """Test soft-deleting patient via API."""
        auth.login()
        
        response = client.delete(f'/api/v1/patients/{test_patient.id}')
        
        assert response.status_code == 200
        
        # Verify soft delete
        response = client.get(f'/api/v1/patients/{test_patient.id}')
        assert response.status_code == 404
```

---

## 5. Accessibility Testing

### Automated Accessibility Tests

```javascript
// tests/accessibility/axe.test.js

import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
    beforeEach(async () => {
        // Load page HTML
        const response = await fetch('http://localhost:5000/patients');
        const html = await response.text();
        document.body.innerHTML = html;
    });
    
    test('patient list has no accessibility violations', async () => {
        const results = await axe(document.body);
        expect(results).toHaveNoViolations();
    });
    
    test('forms have proper labels', async () => {
        const results = await axe(document.body, {
            rules: {
                'label': { enabled: true },
                'form-field-multiple-labels': { enabled: true }
            }
        });
        expect(results).toHaveNoViolations();
    });
    
    test('color contrast meets WCAG AA', async () => {
        const results = await axe(document.body, {
            rules: {
                'color-contrast': { enabled: true }
            }
        });
        expect(results).toHaveNoViolations();
    });
});
```

### Manual Accessibility Checklist

```markdown
## Manual Accessibility Testing

### Keyboard Navigation
- [ ] All interactive elements focusable with Tab
- [ ] Focus order logical (left-to-right, top-to-bottom)
- [ ] Focus indicator visible (2px+ outline)
- [ ] Escape closes modals/dropdowns
- [ ] Enter/Space activates buttons

### Screen Reader
- [ ] Page has descriptive <title>
- [ ] Headings follow hierarchy (h1 → h2 → h3)
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Error messages announced
- [ ] Dynamic content uses aria-live

### Visual
- [ ] Text contrast ≥4.5:1 (normal), ≥3:1 (large)
- [ ] Not relying on color alone
- [ ] Touch targets ≥44x44px
- [ ] Zoom to 200% doesn't break layout
```

---

## 6. Performance Testing

### Lighthouse CI

```javascript
// lighthouserc.js

module.exports = {
    ci: {
        collect: {
            url: [
                'http://localhost:5000/',
                'http://localhost:5000/login',
                'http://localhost:5000/patients'
            ],
            numberOfRuns: 3
        },
        assert: {
            assertions: {
                'categories:performance': ['warn', { minScore: 0.9 }],
                'categories:accessibility': ['error', { minScore: 0.95 }],
                'categories:best-practices': ['warn', { minScore: 0.9 }],
                'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
                'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
                'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
                'total-blocking-time': ['warn', { maxNumericValue: 300 }]
            }
        },
        upload: {
            target: 'temporary-public-storage'
        }
    }
};
```

### Performance Budget Tests

```javascript
// tests/performance/budget.test.js

describe('Performance Budget', () => {
    test('main.js bundle size within budget', async () => {
        const fs = require('fs');
        const path = require('path');
        
        const mainJs = fs.readFileSync(
            path.join(__dirname, '../../static/dist/main.min.js')
        );
        
        const sizeKB = mainJs.length / 1024;
        expect(sizeKB).toBeLessThan(100); // 100KB budget
    });
    
    test('main.css size within budget', async () => {
        const fs = require('fs');
        const path = require('path');
        
        const mainCss = fs.readFileSync(
            path.join(__dirname, '../../static/dist/main.min.css')
        );
        
        const sizeKB = mainCss.length / 1024;
        expect(sizeKB).toBeLessThan(50); // 50KB budget
    });
});
```

---

## 7. Test Fixtures and Helpers

### Pytest Fixtures

```python
# tests/conftest.py

import pytest
from app import create_app, db
from app.models import User, Person, TherapySession


@pytest.fixture
def app():
    """Create test application."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth(client):
    """Authentication helper."""
    class AuthActions:
        def login(self, email='test@example.com', password='test123'):
            return client.post('/login', data={
                'email': email,
                'password': password
            }, follow_redirects=True)
        
        def logout(self):
            return client.get('/logout', follow_redirects=True)
    
    return AuthActions()


@pytest.fixture
def test_user(app):
    """Create test user."""
    with app.app_context():
        user = User(email='test@example.com', name='Test User')
        user.set_password('test123')
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_patient(app, test_user):
    """Create test patient."""
    with app.app_context():
        patient = Person(
            name='Test Patient',
            user_id=test_user.id
        )
        db.session.add(patient)
        db.session.commit()
        return patient


@pytest.fixture
def test_patients(app, test_user):
    """Create multiple test patients."""
    with app.app_context():
        patients = []
        for i in range(10):
            patient = Person(
                name=f'Patient {i}',
                user_id=test_user.id
            )
            db.session.add(patient)
            patients.append(patient)
        db.session.commit()
        return patients
```

### JavaScript Test Helpers

```javascript
// tests/helpers/dom.js

/**
 * Create a DOM element for testing
 * @param {string} html - HTML string
 * @returns {HTMLElement}
 */
export function createElement(html) {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstChild;
}

/**
 * Wait for DOM updates
 * @returns {Promise<void>}
 */
export function nextTick() {
    return new Promise(resolve => requestAnimationFrame(resolve));
}

/**
 * Simulate user click
 * @param {HTMLElement} element
 */
export function click(element) {
    element.dispatchEvent(new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
    }));
}

/**
 * Simulate typing in an input
 * @param {HTMLInputElement} input
 * @param {string} value
 */
export function type(input, value) {
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
}

/**
 * Wait for element to appear
 * @param {string} selector
 * @param {number} timeout
 * @returns {Promise<HTMLElement>}
 */
export async function waitFor(selector, timeout = 1000) {
    const start = Date.now();
    
    while (Date.now() - start < timeout) {
        const element = document.querySelector(selector);
        if (element) return element;
        await new Promise(r => setTimeout(r, 50));
    }
    
    throw new Error(`Element ${selector} not found within ${timeout}ms`);
}
```

---

## 8. Testing Commands

### Package.json Scripts

```json
{
    "scripts": {
        "test": "jest",
        "test:watch": "jest --watch",
        "test:coverage": "jest --coverage",
        "test:accessibility": "jest tests/accessibility/",
        "test:performance": "lhci autorun",
        "test:visual": "echo 'Use Chrome DevTools MCP for visual testing'"
    }
}
```

### Running Tests

```powershell
# Run all Python tests
.\venv\Scripts\Activate.ps1; pytest

# Run specific test file
.\venv\Scripts\Activate.ps1; pytest tests/integration/test_form_submission.py

# Run with coverage
.\venv\Scripts\Activate.ps1; pytest --cov=app --cov-report=html

# Run JavaScript tests
npm test

# Run with coverage
npm run test:coverage

# Run Lighthouse CI
npm run test:performance
```

---

## 9. Testing Checklist

### Unit Tests
- [ ] Utility functions tested
- [ ] API client functions tested
- [ ] DOM manipulation tested
- [ ] Edge cases covered
- [ ] Error handling tested

### Integration Tests
- [ ] Form submissions tested
- [ ] API endpoints tested
- [ ] Authentication flows tested
- [ ] Authorization tested
- [ ] Validation errors tested

### Visual Tests
- [ ] Both themes verified (dark/light)
- [ ] Responsive layouts verified
- [ ] Forms display correctly
- [ ] Error states visible
- [ ] Loading states visible

### Accessibility Tests
- [ ] axe-core passes
- [ ] Keyboard navigation works
- [ ] Screen reader tested
- [ ] Color contrast verified
- [ ] Focus indicators visible

### Performance Tests
- [ ] Bundle sizes within budget
- [ ] Lighthouse scores pass thresholds
- [ ] Core Web Vitals pass
- [ ] No memory leaks

---

## Related Skills

- [WCAG Accessibility](skill-wcag-accessibility.md)
- [Core Web Vitals](skill-core-web-vitals.md)
- [JavaScript Modules](skill-javascript-modules.md)
- [Error Handling](skill-error-handling.md)
