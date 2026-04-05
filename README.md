<div align="center">

# Forum API

**A modern full-stack forum application with hierarchical categories, user authentication, and real-time discussions.**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3-green.svg)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-latest-blue.svg)](https://www.docker.com/)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Configuration](#-configuration)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Authentication** | JWT-based auth with access + refresh tokens |
| 📁 **Hierarchical Branches** | Parent-child category system |
| 💬 **Topics & Replies** | Full CRUD with pagination support |
| 👁️ **Activity Tracking** | View counts and last activity timestamps |
| 👤 **User Profiles** | Username, email, bio, role-based access |
| 🐳 **Docker Ready** | Production & development compose files |
| 🛡️ **Security** | Argon2 password hashing, HTTP-only cookies |

---

## 🛠 Tech Stack

### Backend
- **Python 3.13** - Latest Python with modern features
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - Modern ORM with type safety
- **PostgreSQL 17** - Production-grade relational database
- **Alembic** - Database migrations
- **Pydantic** - Data validation with Python types

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vue Router** - Official router for Vue.js
- **Tailwind CSS 4** - Utility-first CSS framework
- **Vite** - Next-generation build tool
- **TypeScript** - Type-safe JavaScript

### Infrastructure
- **Docker & Docker Compose** - Container orchestration
- **Nginx** - Reverse proxy and load balancing

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Nginx (80)                          │
│                  Reverse Proxy & Load Balancer               │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│   (Vue 3)       │         │   (FastAPI)     │
│   Port: 3000    │         │   Port: 8080    │
└─────────────────┘         └────────┬────────┘
                                     │
                                     ▼
                          ┌─────────────────┐
                          │   PostgreSQL    │
                          │   Port: 5432    │
                          └─────────────────┘
```

### Project Structure

```
forum/
├── backend/
│   ├── src/forum/
│   │   ├── main.py              # Application entry point
│   │   ├── config.py            # Settings & configuration
│   │   ├── database.py          # Database session management
│   │   ├── exceptions.py        # Custom exception handlers
│   │   ├── log.py               # Logging configuration
│   │   └── features/
│   │       ├── user/            # Auth, registration, profiles
│   │       ├── branch/          # Category management
│   │       ├── topic/           # Topic CRUD operations
│   │       └── reply/           # Reply management
├── frontend/
│   └── src/                     # Vue 3 application
├── docker-compose.yml           # Production setup
├── docker-compose.dev.yml       # Development setup
├── docker-compose.test.yml      # Test environment
├── nginx.conf                   # Nginx configuration
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.13+](https://www.python.org/downloads/) (for local development)
- [Node.js 18+](https://nodejs.org/) (for local frontend development)

### Docker (Recommended)

```bash
# Production mode
docker-compose up --build

# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up --build
```

### Local Development

```bash
# Backend
cd backend
uv sync
uv run start

# Frontend (in separate terminal)
cd frontend
npm install
npm run dev
```

### Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| API | http://localhost/api/ |
| Backend (direct) | http://localhost:8080 |
| Frontend (direct) | http://localhost:3000 |

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/users/register` | Register new user | ❌ |
| `POST` | `/api/users/login` | Login (OAuth2) | ❌ |
| `POST` | `/api/users/refresh` | Refresh access token | ✅ |
| `POST` | `/api/users/logout` | Logout user | ✅ |
| `GET` | `/api/users/me` | Get current user | ✅ |
| `GET` | `/api/users/{id}` | Get user by ID | ✅ |

### Branch (Category) Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/branches/` | List all branches | ✅ |
| `GET` | `/api/branches/{id}` | Get branch + topics | ✅ |
| `POST` | `/api/branches/` | Create branch | ✅ |
| `DELETE` | `/api/branches/{id}` | Delete branch | ✅ |

### Topic Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/topics/{id}` | Get topic + replies | ✅ |
| `POST` | `/api/topics/` | Create topic | ✅ |
| `PUT` | `/api/topics/{id}` | Update topic | ✅ |
| `DELETE` | `/api/topics/{id}` | Delete topic | ✅ |

### Reply Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `PUT` | `/api/replies/` | Create reply | ✅ |

---

## 💻 Development

### Running Tests

```bash
# Using test script
./run_tests.sh

# Or directly with pytest
cd backend
uv run pytest

# With coverage
uv run pytest --cov=src/forum
```

### Code Quality

```bash
# Linting with Ruff
uv run ruff check src/

# Type checking with MyPy
uv run mypy src/

# Format code
uv run ruff format src/
```

### Database Migrations

```bash
cd backend
uv run alembic revision --autogenerate -m "Migration message"
uv run alembic upgrade head
```

---

## ⚙️ Configuration

Environment variables (via `.env` or Docker environment):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `SECRET_KEY` | JWT signing secret | - |
| `DEV` | Enable development mode | `false` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_MINUTES` | Refresh token lifetime | `60` |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---
