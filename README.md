# FastAPI Document Management API

## Overview
This project is a backend API built with **FastAPI**. It provides endpoints for:
- User authentication
- Document creation, retrieval, and management
- Custom fields and statuses
- History tracking for document changes

The API is self-documented with Swagger UI at `/docs` and ReDoc at `/redoc`.

---

## Project Structure

```
app/
 ├── main.py                # Entry point of the FastAPI app
 ├── api/                   # API route definitions
 ├── core/                  # Config, database, security, logging
 ├── repositories/          # Data access layer
 ├── services/              # Business logic layer
 ├── schemas/               # Pydantic models for validation/serialization
 └── utils/                 # Exceptions, helpers
```

---

## Features
- Token-based authentication (JWT)
- User management (signup, login, roles)
- Document CRUD operations
- Document types, statuses, and custom fields
- History tracking for changes

---

## Installation

### Requirements
- Python 3.9+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Setup

1. Clone the repository and navigate to the project root.
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env` (example below).

```env
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

5. Run the server:

```bash
uvicorn app.main:app --reload
```

Access Swagger UI at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Usage Examples

### Authentication
1. Register a new user via `/api/user/signup`.
2. Log in at `/api/user/auth/login` to receive a JWT token.
3. Authorize in Swagger UI using the token.

### Documents
- Create a document via `/api/document/documents/`.
- Fetch all documents via `/api/document/documents/`.
- Retrieve history of a document via `/api/document/histories/`.

---

## Architecture

```
[Client / Docs UI]
        ↓
[FastAPI Routes] → [Services] → [Repositories] → [Database]
        ↓
    [Schemas for validation]
```

- **Routes**: Handle requests and responses.
- **Services**: Contain core business logic.
- **Repositories**: Communicate with the database.
- **Schemas**: Enforce data validation and structure.
- **Core**: Configuration, database connection, security.

---

## Testing

Run tests using:

```bash
pytest
```

---

## License
This project is licensed under the MIT License.
