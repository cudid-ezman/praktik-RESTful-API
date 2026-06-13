from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine, Base
from models import prodi_model, fakultas_model, user_model

# Import semua controller
from controllers import prodi_controller, fakultas_controller, auth_controller

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

# ==========================================
# REGISTRASI ROUTER LAYERED ARCHITECTURE
# ==========================================
app.include_router(auth_controller.router)
app.include_router(prodi_controller.router)
app.include_router(fakultas_controller.router)