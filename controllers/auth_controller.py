# controllers/auth_controller.py
import os
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session

from database import get_db
from dependencies import verify_token
from schemas.base_schema import APIResponse
from schemas.user_schema import UserAuth
from services.auth_service import AuthService

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Kita tidak menggunakan prefix agar endpoint tetap /login, bukan /auth/login
router = APIRouter(tags=["Auth & Profil"])

@router.post("/register", status_code=201, response_model=APIResponse[dict])
def register_user(user_data: UserAuth, db: Session = Depends(get_db)):
    service = AuthService(db)
    data = service.register(user_data)
    return APIResponse(status="success", message="Registrasi berhasil, silakan login", data=data)

@router.post("/login", response_model=APIResponse[None])
def login_user(user_data: UserAuth, response: Response, db: Session = Depends(get_db)):
    service = AuthService(db)
    tokens = service.login(user_data)
    
    # Set Cookie
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="lax", secure=False, path="/")
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60, samesite="lax", secure=False, path="/")
    
    return APIResponse(status="success", message="Login berhasil, token telah diset.", data=None)

@router.post("/refresh", response_model=APIResponse[None])
def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token_cookie = request.cookies.get("refresh_token")
    service = AuthService(db)
    tokens = service.refresh(refresh_token_cookie)
    
    # Update Access Token Cookie
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="lax", secure=False, path="/")
    
    return APIResponse(status="success", message="Access token berhasil diperbarui.", data=None)

@router.get("/profil", response_model=APIResponse[dict], tags=["Protected"])
def profil_user(user_info: dict = Depends(verify_token)):
    return APIResponse(status="success", message="Selamat datang di area rahasia", data=user_info)

@router.post("/logout", response_model=APIResponse[None])
def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return APIResponse(status="success", message="Logout berhasil, cookie telah dihapus.", data=None)