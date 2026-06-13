# services/auth_service.py
import os
import jwt
import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from repositories.user_repository import UserRepository
from schemas.user_schema import UserAuth

# Konfigurasi dari Environment
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_rahasia_default")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "rahasia_refresh")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

pwd_context = PasswordHash([BcryptHasher()])

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, user_data: UserAuth):
        existing_user = self.repo.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username sudah terdaftar")
        
        hashed_pw = pwd_context.hash(user_data.password)
        try:
            self.repo.create_user(user_data.username, hashed_pw)
            return {"username": user_data.username, "role": "admin"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def login(self, user_data: UserAuth):
        user = self.repo.get_user_by_username(user_data.username)
        if not user or not pwd_context.verify(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Username atau password salah")
        
        access_payload = {
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        
        refresh_payload = {
            "username": user["username"],
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }
        refresh_token = jwt.encode(refresh_payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def refresh(self, refresh_token: str):
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token tidak ditemukan. Silakan login kembali.")
        try:
            payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("username")
            
            user = self.repo.get_user_by_username(username)
            if not user:
                raise HTTPException(status_code=401, detail="User tidak ditemukan.")
                
            new_access_payload = {
                "username": user["username"],
                "role": user["role"],
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            }
            new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": new_access_token}
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token kedaluwarsa. Silakan login kembali.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Refresh token tidak valid.")