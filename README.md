# Therapy Session Management Application

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)
[![CI/CD](https://github.com/YOUR_USERNAME/appalapapa/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/appalapapa/actions)
[![codecov](https://codecov.io/gh/YOUR_USERNAME/appalapapa/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/appalapapa)

> A professional Flask-based web application for managing therapy sessions with patient tracking, payment management, and comprehensive audit logging.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Development Setup](#-development-setup)
- [Running Tests](#-running-tests)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Docker Deployment](#-docker-deployment)
- [Production Deployment](#-production-deployment)
- [CLI Commands](#-cli-commands)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)

---

## ✨ Features

### Core Functionality
- 👤 **Patient Management**: Add, edit, and soft-delete patient records
- 📅 **Session Tracking**: Record therapy sessions with dates and pricing
- 💰 **Payment Status**: Toggle between pending/paid with instant updates
- 📊 **Dashboard**: Filter and view sessions by status (all/pending/paid)
- 🎠 **Session Cards Slider**: Navigate sessions with Bootstrap 5 Carousel cards
- 📈 **Statistics API**: Get financial summaries and session counts
- ⚡ **AJAX Operations**: Edit, delete, and toggle without page refresh

### Security & Privacy
- 🔐 **Secure Authentication**: Password hashing with Werkzeug
- 🛡️ **CSRF Protection**: All forms protected against cross-site attacks
- 🚦 **Rate Limiting**: Protection against brute force attacks
- 👥 **Role-Based Access**: Admin, Therapist, and Viewer roles
- 📝 **Audit Logging**: Track all data changes with user attribution
- 🗑️ **Soft Delete**: Recover accidentally deleted records

### Technical Excellence
- 🏭 **Factory Pattern**: Modular application architecture
- 🧩 **Blueprints**: Organized route separation
- 📦 **Service Layer**: Clean business logic separation
- 🔄 **Database Migrations**: Version-controlled schema changes
- 🧪 **Comprehensive Tests**: Unit and integration testing
- 🐳 **Docker Ready**: Production-ready containerization
- 🚀 **CI/CD Pipeline**: Automated testing and deployment

---

## 🛠 Technology Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python 3.10+, Flask 3.0+ |
| **Database** | SQLite (dev), PostgreSQL (prod), SQLAlchemy ORM |
| **Forms** | Flask-WTF, WTForms |
| **Auth** | Flask-Login, Werkzeug Security |
| **Security** | Flask-Limiter, CSRF Protection |
| **Frontend** | Jinja2, Bootstrap 5 |
| **Testing** | pytest, pytest-cov, pytest-flask |
| **DevOps** | Docker, GitHub Actions |
| **Monitoring** | Sentry (production) |

---

## 📁 Project Structure

```
appalapapa/
├── app/                          # Application package
│   ├── __init__.py              # App factory
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Flask extensions
│   ├── api/                     # REST API v1
│   │   └── v1/
│   │       └── resources.py
│   ├── cli/                     # CLI commands
│   │   ├── db_commands.py
│   │   └── user_commands.py
│   ├── middleware/              # Request/response middleware
│   │   ├── error_handlers.py
│   │   └── security.py
│   ├── models/                  # SQLAlchemy models
│   │   ├── mixins.py
│   │   ├── user.py
│   │   ├── person.py
│   │   ├── session.py
│   │   └── audit_log.py
│   ├── routes/                  # View blueprints
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── patients.py
│   │   └── sessions.py
│   ├── services/                # Business logic
│   │   ├── auth_service.py
│   │   ├── patient_service.py
│   │   ├── session_service.py
│   │   └── audit_service.py
│   ├── utils/                   # Utilities
│   │   ├── constants.py
│   │   ├── formatters.py
│   │   └── decorators.py
│   └── validators/              # Form validators
│       └── forms.py
├── tests/                       # Test suite
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_validators.py
│   └── integration/
│       ├── test_auth_routes.py
│       ├── test_patient_routes.py
│       └── test_session_routes.py
├── migrations/                  # Alembic migrations
├── requirements/                # Dependency files
│   ├── base.txt
│   ├── dev.txt
│   ├── test.txt
│   └── prod.txt
├── templates/                   # Jinja2 templates (organized by module)
│   ├── base.html               # Base template with navigation
│   ├── auth/                   # Authentication templates
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── reset_password.html
│   │   └── change_password.html
│   ├── patients/               # Patient management templates
│   │   ├── list.html           # Main dashboard
│   │   ├── form_person.html
│   │   └── delete_person.html
│   ├── sessions/               # Session management templates
│   │   ├── form_session.html
│   │   └── form_edit.html
│   └── errors/                 # Error pages
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
├── static/                      # Static assets (CSS, JS)
│   ├── css/
│   │   └── bootstrap.min.css
│   └── js/
│       ├── bootstrap.bundle.min.js
│       └── api.js              # JavaScript API client
├── .github/                     # GitHub configs
│   ├── instructions/
│   └── workflows/
├── run.py                       # Development entry point
├── wsgi.py                      # Production WSGI entry
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/appalapapa.git
cd appalapapa
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements/dev.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# Edit .env with your settings (especially SECRET_KEY)
```

### 5. Initialize Database
```bash
flask db init-db
flask user create admin@example.com --role admin
```

### 6. Run Development Server
```bash
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 💻 Development Setup

### Complete Development Environment

```bash
# 1. Clone and enter project
git clone https://github.com/YOUR_USERNAME/appalapapa.git
cd appalapapa

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install all development dependencies
pip install -r requirements/dev.txt

# 4. Copy and configure environment
copy .env.example .env
# Edit .env file with your SECRET_KEY

# 5. Initialize the database
flask db init-db

# 6. Create admin user
flask user create admin@example.com --password YourSecurePass123 --role admin

# 7. (Optional) Seed sample data
flask db seed

# 8. Run the development server
python run.py
```

### Using Docker for Development

```bash
# Build and run all services
docker-compose up

# Run with database tools (pgAdmin)
docker-compose --profile tools up

# Access the application at http://localhost:5000
# Access pgAdmin at http://localhost:5050
```

---

## 🧪 Running Tests

### Prerequisites
Make sure you have the test dependencies installed:
```bash
pip install -r requirements/test.txt
```

### Run All Tests with venv Activation

```bash
# Windows Command Prompt
venv\Scripts\activate
pytest

# Windows PowerShell
.\venv\Scripts\Activate.ps1
pytest

# macOS/Linux
source venv/bin/activate
pytest
```

### Test Commands

```bash
# Run all tests with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/unit/test_models.py -v

# Run specific test class
pytest tests/unit/test_models.py::TestUserModel -v

# Run specific test function
pytest tests/unit/test_models.py::TestUserModel::test_password_hashing -v

# Run tests matching a pattern
pytest -k "password" -v

# Run with detailed failure info
pytest --tb=long

# Run and stop at first failure
pytest -x

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

### Test Coverage Goals
- **Unit Tests**: Models, Services, Validators
- **Integration Tests**: All route endpoints
- **Current Status**: 104 tests passing ✅
- **Target Coverage**: >80%

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# =============================================================================
# Flask Configuration
# =============================================================================
FLASK_CONFIG=development          # development, testing, production
FLASK_DEBUG=True                  # Enable debug mode (dev only)
SECRET_KEY=your-super-secret-key  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"

# =============================================================================
# Database Configuration
# =============================================================================
DATABASE_URL=sqlite:///instance/database.db  # Dev: SQLite
# DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Prod: PostgreSQL

# =============================================================================
# Security Configuration
# =============================================================================
ALLOWED_EMAILS=                   # Comma-separated whitelist (empty = allow all)
SESSION_LIFETIME_DAYS=30          # Session duration

# =============================================================================
# Rate Limiting
# =============================================================================
RATELIMIT_DEFAULT=200 per hour    # Default rate limit
RATELIMIT_STORAGE_URL=memory://   # Use redis:// for production

# =============================================================================
# Error Monitoring (Production)
# =============================================================================
SENTRY_DSN=                       # Sentry DSN for error tracking
```

### Generating a Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📡 API Documentation

### Base URL
```
/api/v1/
```

### Authentication
All API endpoints require session authentication.

### Endpoints

#### Health Check
```http
GET /api/v1/health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Patients

```http
GET /api/v1/patients              # List all patients
GET /api/v1/patients/{id}         # Get patient details
POST /api/v1/patients             # Create patient
PUT /api/v1/patients/{id}         # Update patient
DELETE /api/v1/patients/{id}      # Delete patient (soft)
```

#### Sessions

```http
GET /api/v1/patients/{id}/sessions  # List patient sessions
GET /api/v1/sessions/{id}             # Get session details
POST /api/v1/sessions               # Create session
PUT /api/v1/sessions/{id}           # Update session
DELETE /api/v1/sessions/{id}        # Delete session (soft)
POST /api/v1/sessions/{id}/toggle   # Toggle payment status
```

#### Statistics

```http
GET /api/v1/stats                   # Get financial summary
```

Response:
```json
{
  "total_patients": 25,
  "total_sessions": 150,
  "pending_total": 5000.00,
  "paid_total": 12500.00,
  "grand_total": 17500.00
}
```

---

## 🐳 Docker Deployment

### Development with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

### Production with Docker

```bash
# Build production image
docker build -t therapy-app:latest --target production .

# Run with production compose
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Docker Commands

```bash
# Rebuild after code changes
docker-compose up --build

# Run migrations
docker-compose exec web flask db upgrade

# Create admin user
docker-compose exec web flask user create admin@example.com --role admin

# Access container shell
docker-compose exec web /bin/sh

# View PostgreSQL logs
docker-compose logs -f db
```

---

## 🚀 Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install production dependencies
pip install -r requirements/prod.txt

# Run with Gunicorn
gunicorn wsgi:app \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2 \
  --worker-class gthread \
  --access-logfile - \
  --error-logfile -
```

### Environment Setup for Production

1. Set `FLASK_CONFIG=production`
2. Use PostgreSQL: `DATABASE_URL=postgresql://...`
3. Configure Sentry: `SENTRY_DSN=https://...`
4. Use Redis for rate limiting: `RATELIMIT_STORAGE_URL=redis://...`
5. Set a strong `SECRET_KEY`
6. Disable `FLASK_DEBUG`

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 🔧 CLI Commands

### Database Commands

```bash
# Initialize database with tables
flask db init-db

# Drop all tables (dangerous!)
flask db drop-db --confirm

# Seed sample data
flask db seed

# Backup database
flask db backup --output backup.sql

# Cleanup old audit logs
flask db cleanup-audit --days 90
```

### User Management

```bash
# Create new user
flask user create email@example.com --password Pass123 --role admin

# List all users
flask user list

# Change user role
flask user set-role email@example.com therapist

# Reset password
flask user reset-password email@example.com

# Activate/deactivate user
flask user activate email@example.com
flask user deactivate email@example.com
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Code Style
- Follow PEP 8
- Use Black for formatting
- Use isort for import sorting
- Write tests for new features

```bash
# Format code
black app/ tests/
isort app/ tests/

# Lint code
flake8 app/ tests/
```

---

## 🔒 Security

### Reporting Vulnerabilities
Please report security vulnerabilities privately to [your-email@example.com].

### Security Features
- ✅ Password hashing with Werkzeug
- ✅ CSRF protection on all forms
- ✅ Rate limiting on authentication
- ✅ SQL injection prevention (ORM)
- ✅ XSS prevention (Jinja2 auto-escaping)
- ✅ Security headers middleware
- ✅ Audit logging for compliance

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [pytest](https://pytest.org/) - Testing framework

---

**Made with ❤️ for better therapy session management**
