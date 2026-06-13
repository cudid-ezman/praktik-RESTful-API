from fastapi import Request, HTTPException
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_rahasia_default")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# DEPENDENCY PROTEKSI
def verify_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, 
                            detail="Akses ditolak. Access Token tidak ditemukan.")
    try:
        decoded_data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, 
                            detail="Access Token kedaluwarsa. Silakan gunakan endpoint /refresh.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Access Token tidak valid.")