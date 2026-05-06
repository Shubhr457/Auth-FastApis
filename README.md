# JWT Auth Service

A production-ready authentication REST API built with **FastAPI**, **MongoDB** (Motor + Beanie), and **JWT** (access + refresh token flow).

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | MongoDB (via Motor async driver) |
| ODM | Beanie |
| Auth | python-jose (JWT / HS256) |
| Hashing | passlib + bcrypt |
| Config | pydantic-settings |

## Features

- User registration with bcrypt password hashing
- Login returns short-lived **access token** (15 min) + long-lived **refresh token** (7 days)
- Refresh endpoint to get a new access token without re-logging in
- Protected `/me` route using reusable `get_current_user` dependency
- Refresh token stored in MongoDB — supports server-side revocation
- Auto-generated Swagger UI at `/docs`

## Project Structure

```
app/
├── main.py             # FastAPI app entry, lifespan DB init
├── config.py           # Settings loaded from .env
├── database.py         # Motor + Beanie initialisation
├── dependencies.py     # get_current_user dependency
├── models/
│   └── user.py         # Beanie User document
├── schemas/
│   ├── user.py         # Register / Login / UserResponse schemas
│   └── token.py        # Token response schemas
├── routers/
│   └── auth.py         # /auth/* routes
└── services/
    ├── auth_service.py  # Register, login, refresh business logic
    └── token_service.py # JWT create / decode helpers
```

## Setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/Shubhr457/Auth-FastApis.git
cd Auth-FastApis
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY`:

```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=auth_db
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Start MongoDB

Make sure MongoDB is running locally (or update `MONGO_URI` to point to Atlas):

```bash
mongod
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

API will be live at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create a new account |
| POST | `/auth/login` | No | Login, get token pair |
| POST | `/auth/refresh` | No | Get new access token |
| GET | `/auth/me` | Bearer token | Get current user profile |
| GET | `/health` | No | Health check |

---

## Example Usage

### Register

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret123"}'
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Get current user

```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <access_token>"
```

### Refresh access token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```
