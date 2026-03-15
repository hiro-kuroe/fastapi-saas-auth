# FastAPI SaaS Auth API

JWT authentication and role-based access control example built with FastAPI.

## Features

- User registration
- JWT login authentication
- Current user endpoint
- Role-based access control (admin)
- User management CRUD
- OpenAPI / Swagger documentation

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- SQLite

## Installation

```bash
git clone https://github.com/hiro-kuroe/fastapi-saas-auth
cd fastapi-saas-auth
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Server starts at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

## Authentication Flow

1. Create user

```
POST /users
```

## Example User JSON

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "test1234"
}
```

2. Login

```
POST /token
```

3. Click Authorize in Swagger.

4. After authorization, protected endpoints can be executed.

## API Endpoints

### Auth

```
POST /users      Create user
POST /token      Login
```

### Current User

```
GET   /me      Get current user
PATCH /me      Update current user
```

### Admin

```
GET    /users            List users
PUT    /users/{user_id}  Update user
DELETE /users/{user_id}  Delete user
```

Admin endpoints require a user with role `admin`.



## License

MIT