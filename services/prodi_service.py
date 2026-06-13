# services/prodi_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.prodi_repository import ProdiRepository
from schemas.prodi_schema import ProdiCreate, ProdiUpdate

class ProdiService:
    def __init__(self, db: Session):
        # Inisialisasi repository di dalam service
        self.repo = ProdiRepository(db)

    def get_all(self):
        # Langsung kembalikan data mentah
        return self.repo.get_all_prodi()

    def get_by_id(self, prodi_id: str):
        return self.repo.get_prodi_by_id(prodi_id)

    def create(self, pro: ProdiCreate):
        # Logika Bisnis: Cek apakah ID Prodi sudah ada
        existing_prodi = self.repo.get_prodi_by_id(pro.id)
        if existing_prodi:
            raise HTTPException(status_code=400, detail="ID Prodi sudah terdaftar")
        
        try:
            self.repo.create_prodi(pro.id, pro.nama, pro.fakultas)
            return pro.model_dump() # Kembalikan data yang baru disimpan
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, prodi_id: str, pro: ProdiUpdate):
        rowcount = self.repo.update_prodi(prodi_id, pro.nama, pro.fakultas)
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Prodi tidak ditemukan")
        return {"id": prodi_id, "nama": pro.nama, "fakultas": pro.fakultas}

    def delete(self, prodi_id: str):
        rowcount = self.repo.delete_prodi(prodi_id)
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Prodi tidak ditemukan")
        return None