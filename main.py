from fastapi import FastAPI, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, get_db, Base  
from models import Prodi, Fakultas, User
from schemas import FakultasCreate, FakultasUpdate, UserAuth
from dependencies import verify_token
import os
from dotenv import load_dotenv
import jwt
import datetime
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from fastapi.middleware.cors import CORSMiddleware
from controllers import prodi_controller

load_dotenv()

app = FastAPI(title="Praktikum Web API", version="1.0.0")

Base.metadata.create_all(bind=engine) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,                  
    allow_methods=["*"],                     
    allow_headers=["*"],                     
)

# Konfigurasi Keamanan
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_rahasia_default")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "rahasia_refresh")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

pwd_context = PasswordHash([BcryptHasher()])

# ==========================================
# REGISTRASI ROUTER LAYERED ARCHITECTURE
# ==========================================
app.include_router(prodi_controller.router)


# =================
# ENDPOINT FAKULTAS
# =================

@app.get("/fakultas", status_code=200, description="Mengambil semua daftar fakultas")
@app.get("/fakultas/", status_code=200, description="Mengambil semua daftar fakultas")
def list_fakultas(db: Session = Depends(get_db)):
    query = text("SELECT * FROM fakultas")
    data_fakultas = db.execute(query).mappings().fetchall()
    return {"total": len(data_fakultas), "data": [dict(item) for item in data_fakultas]}

@app.get("/fakultas/{id}", status_code=200, description="Mengambil detail fakultas berdasarkan ID")
def get_fakultas(id: str, db: Session = Depends(get_db)):
    query = text("SELECT * FROM fakultas WHERE id = :fid")
    result = db.execute(query, {"fid": id}).mappings().fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
    return {"data": dict(result)}

@app.post("/fakultas", status_code=201, description="Menyimpan data fakultas baru")
@app.post("/fakultas/", status_code=201, description="Menyimpan data fakultas baru")
def create_fakultas(fak: FakultasCreate, db: Session = Depends(get_db)):
    try:
        query = text("INSERT INTO fakultas VALUES (:fid, :fnama)")
        db.execute(query, {"fid": fak.id, "fnama": fak.nama})
        db.commit()
        return {
            "message": "Data berhasil disimpan",
            "data": {"id": fak.id, "nama": fak.nama}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/fakultas/{id}", status_code=200, description="Mengubah data fakultas")
def update_fakultas(id: str, fak: FakultasUpdate, db: Session = Depends(get_db)):
    try:
        query = text("UPDATE fakultas SET nama = :fnama WHERE id = :fid")
        result = db.execute(query, {"fid": id, "fnama": fak.nama})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
        return {
            "message": "Data berhasil diperbarui",
            "data": {"id": id, "nama": fak.nama}
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/fakultas/{id}", status_code=200, description="Menghapus data dari tabel fakultas")
def delete_fakultas(id: str, db: Session = Depends(get_db)):
    try:
        query = text("DELETE FROM fakultas WHERE id = :fid")
        result = db.execute(query, {"fid": id})
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
        return {"message": f"Data dengan ID {id} berhasil dihapus"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ======================
# ENDPOINT AUTH & PROFIL 
# ======================

@app.post("/register", status_code=201, tags=["Auth"])
def register_user(user_data: UserAuth, db: Session = Depends(get_db)):
    try:
        query_cek = text("SELECT id FROM users WHERE username=:u")
        cek_user = db.execute(query_cek, {"u": user_data.username}).fetchone()
        if cek_user:
            raise HTTPException(status_code=400, detail="Username sudah terdaftar")
            
        hashed_pw = pwd_context.hash(user_data.password)
        
        query_insert = text("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)")
        db.execute(query_insert, {"u": user_data.username, "p": hashed_pw, "r": "admin"})
        db.commit()
        return {"message": "Registrasi berhasil, silakan login"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", tags=["Auth"])
def login_user(user_data: UserAuth, response: Response, db: Session = Depends(get_db)):
    query_user = text("SELECT * FROM users WHERE username=:u")
    user = db.execute(query_user, {"u": user_data.username}).mappings().fetchone()
    
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
    
    # PERBAIKAN: samesite menjadi lax dan secure menjadi False untuk localhost HTTP
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="lax", secure=False, path="/",)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60, samesite="lax", secure=False, path="/",)
    
    return {"message": "Login berhasil, token telah diset."}

@app.post("/refresh", tags=["Auth"])
def refresh_access_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token tidak ditemukan. Silakan login kembali.")
        
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        
        query_user = text("SELECT * FROM users WHERE username=:u")
        user = db.execute(query_user, {"u": username}).mappings().fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="User tidak ditemukan.")
            
        new_access_payload = {
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm=ALGORITHM)
        
        # PERBAIKAN: samesite menjadi lax dan secure menjadi False
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60, samesite="lax", secure=False, path="/",)
        return {"message": "Access token berhasil diperbarui."}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token kedaluwarsa. Silakan login kembali.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token tidak valid.")

@app.get("/profil", tags=["Protected"])
def profil_user(user_info: dict = Depends(verify_token)):
    return {
        "message": "Selamat datang di area rahasia",
        "data_login": user_info
    }

@app.post("/logout", tags=["Auth"])
def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout berhasil, cookie telah dihapus."}