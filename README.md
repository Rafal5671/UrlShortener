# KRTK

> A modular **URL shortener** built with a **Flask backend** and a vanilla **JavaScript frontend**.
> Clean layered architecture with Application Factory pattern, Blueprint routing, service layer, and SQLite persistence.

---

## Build Status

![Platform](https://img.shields.io/badge/platform-Web%20App-blue)
![Backend](https://img.shields.io/badge/backend-Flask-000000)
![Database](https://img.shields.io/badge/database-SQLite-003B57)
![Language](https://img.shields.io/badge/language-Python%20%2F%20JavaScript-yellow)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![Architecture](https://img.shields.io/badge/architecture-Modular%20Blueprint-informational)

---

## Description

KRTK is a full-stack URL shortener built with a focus on clean, modular Python architecture. It follows the **Application Factory** pattern with Flask Blueprints, a dedicated service layer, and DTO-based serialization — making the codebase easy to extend, test, and maintain.

The frontend is a minimal single-page interface with a dark aesthetic, built in vanilla HTML/CSS/JS. Users paste a long URL, receive a short link, and can copy it to the clipboard in one click. The redirect is handled server-side with a `302` response.

---

## Features

- Shorten any `http://` or `https://` URL
- Returns existing short code if URL was already shortened
- One-click clipboard copy
- `302` redirect from short link to original URL
- Input validation with descriptive error messages
- REST API with JSON responses
- Modular architecture: config, models, schemas, services, blueprints
- Unit tests for service layer
- Integration tests for all API endpoints and redirects

---

## Tech Stack

- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Backend:** Python 3.12, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Testing:** pytest
- **Configuration:** python-dotenv, environment-based config hierarchy

---

## Project Structure

```
urlshortener/
├── run.py                  # Development entrypoint
├── wsgi.py                 # Production entrypoint (Gunicorn)
├── config.py               # DevelopmentConfig / CIConfig / ProductionConfig
├── tests.py                # Unit and integration tests
├── requirements.txt
├── pytest.ini
├── conftest.py
├── .env.example
└── app/
    ├── __init__.py         # Application Factory (create_app)
    ├── extensions.py       # db = SQLAlchemy() — lazy init
    ├── models/
    │   └── url.py          # ShortURL ORM model
    ├── schemas/
    │   └── url_schema.py   # ShortURLResponse DTO
    ├── services/
    │   └── url_service.py  # Business logic, validation, code generation
    ├── api/
    │   ├── routes.py       # POST /api/shorten, GET /api/info/<code>
    │   └── errors.py       # 404 / 405 / 500 error handlers
    ├── web/
    │   └── routes.py       # GET /, GET /<short_code> redirect
    └── templates/
        ├── index.html      # Main UI
        └── 404.html        # Not found page
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Rafal5671/UrlShortener.git
cd UrlShortener
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

The default `.env` uses SQLite — no additional setup required.

### 5. Run the application

```bash
python run.py
```

Open your browser at **http://localhost:5000**

---

## Configuration

All settings are controlled via environment variables defined in `.env`:

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///urls.db` | Database connection string |
| `BASE_URL` | `http://localhost:5000` | Base URL prepended to short codes |
| `SECRET_KEY` | `dev-secret-key` | Flask secret key |
| `FLASK_ENV` | `development` | Environment: `development`, `production` |
| `SHORT_CODE_LENGTH` | `6` | Length of generated short codes |

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Main UI |
| `POST` | `/api/shorten` | Shorten a URL |
| `GET` | `/api/info/<code>` | Get info about a short code |
| `GET` | `/<short_code>` | Redirect to original URL (302) |

### POST /api/shorten

**Request:**
```json
{ "url": "https://your-very-long-url.com/some/deep/path" }
```

**Response `201` (created):**
```json
{
  "id": 1,
  "original_url": "https://your-very-long-url.com/some/deep/path",
  "short_code": "aB3xYz",
  "short_url": "http://localhost:5000/aB3xYz",
  "created_at": "2025-01-01T12:00:00"
}
```

**Response `200`** — returned when the URL was already shortened previously.

**Response `400`** — returned when the URL is empty, missing a scheme, or otherwise invalid.

---

## Running Tests

```bash
pytest tests.py -v
```

Expected output: **17 passed, 0 warnings**

Test coverage includes:

| Class | What is tested |
|---|---|
| `TestURLService` | Validation, deduplication, whitespace stripping, error cases |
| `TestAPIShorten` | 201 / 200 / 400 responses |
| `TestAPIInfo` | 200 / 404 responses |
| `TestRedirect` | 302 redirect, 404 for unknown codes |

---
