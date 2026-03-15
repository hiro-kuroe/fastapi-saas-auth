from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, LoginRequest, Token, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token

from app.dependencies.auth import require_role, get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/users", response_model=UserOut, tags=["01_auth"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/token", response_model=Token, tags=["01_auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserOut, tags=["02_me"])
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserOut, tags=["02_me"])
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.username = user_update.username
    current_user.email = user_update.email

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/users", response_model=List[UserOut], tags=["03_admin"])
def get_users(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin"))
):
    users = db.query(User).all()
    return users


@router.put("/users/{user_id}", response_model=UserOut, tags=["03_admin"])
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = user_update.username
    user.email = user_update.email
    user.role = user_update.role

    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}", tags=["03_admin"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()

    return {"message": "user deleted"}


@router.get("/admin-only")
def admin_only(user: User = Depends(require_role("admin"))):
    return {"message": "admin access granted"}


