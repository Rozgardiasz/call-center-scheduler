import jwt
from datetime import datetime, timedelta
from typing import Dict
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from models import Employee
from database import SessionLocal

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def create_jwt_token(data: Dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expiration = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expiration})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request, db: Session) -> Employee:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        token = auth_header.split(" ")[1]  
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    try:
        payload = decode_jwt_token(token)
        user = db.query(Employee).filter(Employee.id == payload.get("user_id")).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_active_admin(request: Request, db: Session) -> Employee:
    user = get_current_user(request, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user
