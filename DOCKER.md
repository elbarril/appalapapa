# Docker Setup & Management Guide

This guide documents the Docker configuration for the Therapy Session Management application.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running the Application](#running-the-application)
4. [Database Management](#database-management)
5. [Common Commands](#common-commands)
6. [Troubleshooting](#troubleshooting)
7. [Architecture Overview](#architecture-overview)

---

## Prerequisites

### Required Software
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Download: https://www.docker.com/products/docker-desktop
  - Verify installation: `docker --version`
  - Verify running: `docker info`

### Verify Docker is Running
```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Check Docker is running (should show system info)
docker info
```

---

## Initial Setup

### 1. Environment Variables

The `.env` file must contain these Docker-related variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_CONFIG=development

# Database (SQLite for dev, can use PostgreSQL)
DATABASE_URL=sqlite:////app/instance/database.db

# PostgreSQL (available if you switch to PostgreSQL)
POSTGRES_USER=therapy_user
POSTGRES_PASSWORD=therapy_pass
POSTGRES_DB=therapy_db

# pgAdmin (optional database UI)
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin

# Email whitelist for registration (comma-separated)
ALLOWED_EMAILS=test@example.com,your-email@example.com
```

### 2. Docker Compose Configuration

The `docker-compose.yml` defines three services:

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `web` | Custom (Dockerfile) | 5000 | Flask application |
| `db` | postgres:15-alpine | 5432 | PostgreSQL database |
| `redis` | redis:7-alpine | 6379 | Caching/sessions |

### 3. First-Time Build

```powershell
# Build and start all containers
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

### 4. Initialize Database

After containers are running, initialize the database:

```powershell
# Create database tables
docker-compose exec web flask db-utils init

# Seed with test data (optional)
docker-compose exec web flask db-utils seed
```

**Test Credentials (after seeding):**
- Email: `test@example.com`
- Password: `test123`
- Role: Admin

---

## Running the Application

### Start Containers

```powershell
# Start in foreground (see logs)
docker-compose up

# Start in background (detached)
docker-compose up -d

# Start and rebuild if Dockerfile changed
docker-compose up --build -d
```

### Access the Application

| Service | URL | Notes |
|---------|-----|-------|
| Flask App | http://localhost:5000 | Main application |
| PostgreSQL | localhost:5432 | Database (if using) |
| Redis | localhost:6379 | Cache |

### Stop Containers

```powershell
# Stop all containers (preserves data)
docker-compose stop

# Stop and remove containers (preserves volumes)
docker-compose down

# Stop, remove containers AND delete volumes (DELETES DATA!)
docker-compose down -v
```

---

## Database Management

### Using SQLite (Default for Development)

The SQLite database is stored in a Docker volume at `/app/instance/database.db`.

```powershell
# Initialize tables
docker-compose exec web flask db-utils init

# Seed test data
docker-compose exec web flask db-utils seed

# Backup database
docker-compose exec web flask db-utils backup
```

### Using PostgreSQL (Production)

To switch to PostgreSQL, update `DATABASE_URL` in `.env`:

```env
DATABASE_URL=postgresql://therapy_user:therapy_pass@db:5432/therapy_db
```

Then restart containers:
```powershell
docker-compose down
docker-compose up -d
docker-compose exec web flask db-utils init
```

### Database Migrations

```powershell
# Create a new migration
docker-compose exec web flask db migrate -m "Description of changes"

# Apply migrations
docker-compose exec web flask db upgrade

# Rollback last migration
docker-compose exec web flask db downgrade
```

---

## Common Commands

### Container Management

```powershell
# View running containers
docker-compose ps

# View all containers (including stopped)
docker ps -a

# Restart a specific service
docker-compose restart web

# Restart all services
docker-compose restart
```

### Logs

```powershell
# View all logs
docker-compose logs

# View logs for specific service
docker-compose logs web

# Follow logs in real-time
docker-compose logs -f web

# View last 100 lines
docker-compose logs --tail=100 web
```

### Execute Commands in Container

```powershell
# Open a shell inside the container
docker-compose exec web bash

# Run a Flask CLI command
docker-compose exec web flask <command>

# Run Python inside container
docker-compose exec web python -c "print('Hello')"

# Check Python environment
docker-compose exec web pip list
```

### User Management

```powershell
# List all users
docker-compose exec web flask user list

# Create a new user
docker-compose exec web flask user create email@example.com

# Change user role (admin/therapist/viewer)
docker-compose exec web flask user set-role email@example.com admin
```

### Cleanup

```powershell
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes (CAUTION: may delete data)
docker volume prune

# Remove everything unused
docker system prune -a
```

---

## Troubleshooting

### Problem: "Cannot connect to Docker daemon"

**Solution:** Docker Desktop is not running. Start Docker Desktop and wait for it to fully load.

```powershell
# Check if Docker is running
docker info
```

### Problem: Port 5000 already in use

**Solution:** Another application is using port 5000. Either stop that application or change the port in `docker-compose.yml`:

```yaml
ports:
  - "5001:5000"  # Use 5001 on host
```

### Problem: Database file permission error

**Solution:** Fix permissions inside the container:

```powershell
docker-compose exec web chmod 777 /app/instance
docker-compose exec web flask db-utils init
```

### Problem: Changes not reflected

**Solution:** The code is volume-mounted, but sometimes you need to restart:

```powershell
# Restart the web container
docker-compose restart web

# Or rebuild if dependencies changed
docker-compose up --build -d
```

### Problem: CSRF Token Missing (403 Error)

**Cause:** VS Code Simple Browser doesn't handle cookies/sessions properly.

**Solution:** Use a real browser (Chrome, Firefox, Edge) to access the application at http://localhost:5000.

### Problem: Container won't start

**Solution:** Check the logs for errors:

```powershell
docker-compose logs web
```

Common causes:
- Missing environment variables in `.env`
- Syntax error in Python code
- Missing dependencies

### Problem: Database tables don't exist

**Solution:** Initialize the database:

```powershell
docker-compose exec web flask db-utils init
```

---

## Architecture Overview

### Docker Compose Services

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                                                          │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│  │   therapy   │   │  therapy    │   │   therapy   │   │
│  │    -web     │   │    -db      │   │   -redis    │   │
│  │             │   │             │   │             │   │
│  │  Flask App  │   │ PostgreSQL  │   │    Redis    │   │
│  │  Port 5000  │   │  Port 5432  │   │  Port 6379  │   │
│  └──────┬──────┘   └─────────────┘   └─────────────┘   │
│         │                                               │
└─────────┼───────────────────────────────────────────────┘
          │
          ▼
    http://localhost:5000
```

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `.` (project root) | `/app` | Source code (hot reload) |
| `db-data` volume | `/app/instance` | SQLite database |
| `postgres-data` volume | `/var/lib/postgresql/data` | PostgreSQL data |

### Environment Differences

| Aspect | Local Flask | Docker |
|--------|-------------|--------|
| Python | System/venv | Container (3.11-slim) |
| Database | Local SQLite | Container SQLite/PostgreSQL |
| URL | http://localhost:5000 | http://localhost:5000 |
| Hot Reload | ✅ Yes | ✅ Yes (volume mounted) |
| Dependencies | requirements.txt | Built into image |

---

## Quick Reference Card

```powershell
# === DAILY WORKFLOW ===

# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web

# Stop everything
docker-compose down


# === DATABASE ===

# Initialize
docker-compose exec web flask db-utils init

# Seed test data
docker-compose exec web flask db-utils seed

# Backup
docker-compose exec web flask db-utils backup


# === TROUBLESHOOTING ===

# Restart app
docker-compose restart web

# Rebuild everything
docker-compose up --build -d

# Shell access
docker-compose exec web bash

# Check container logs
docker-compose logs --tail=50 web
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)

---

*Last updated: January 2026*
