from fastapi import FastAPI
from app.api.users import router as users_router

from app.db.base import Base
from app.db.session import engine

import app.models.user

from app.api.users import router as users_router


app = FastAPI(
    title="FastAPI SaaS Auth API",
    description="JWT authentication and role-based access control example",
    version="1.0.0",
    openapi_tags=[
        {"name": "01_auth", "description": "Authentication"},
        {"name": "02_me", "description": "Current user"},
        {"name": "03_admin", "description": "Admin operations"},
    ],
)

Base.metadata.create_all(bind=engine)

app.include_router(users_router)

@app.get("/")
def root():
    return{"message": "SaaS Auth API"}