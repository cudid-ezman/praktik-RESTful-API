# schemas/prodi_schema.py
from pydantic import BaseModel

class ProdiCreate(BaseModel):
    id: str
    nama: str
    fakultas: str

class ProdiUpdate(BaseModel):
    nama: str
    fakultas: str