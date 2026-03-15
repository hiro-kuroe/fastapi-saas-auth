from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

    except:
        raise HTTPException(status_code=401, detail="invalid token")
    
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    
    return user


def require_role(role: str):

    def role_checker(user: User = Depends(get_current_user)):
         if user.role != role:
             raise HTTPException(status_code=403, detail="permission denied")
         
         return user
    
    return role_checker