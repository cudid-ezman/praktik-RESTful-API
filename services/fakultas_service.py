# services/fakultas_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.fakultas_repository import FakultasRepository
from schemas.fakultas_schema import FakultasCreate, FakultasUpdate

class FakultasService:
    def __init__(self, db: Session):
        self.repo = FakultasRepository(db)

    def get_all(self):
        data = self.repo.get_all()
        # Konversi setiap baris RowMapping menjadi dictionary
        return [dict(item) for item in data]

    def get_by_id(self, fid: str):
        data = self.repo.get_by_id(fid)
        if not data:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
        # Konversi objek RowMapping menjadi dictionary
        return dict(data)

    def create(self, fak: FakultasCreate):
        existing = self.repo.get_by_id(fak.id)
        if existing:
            raise HTTPException(status_code=400, detail="ID Fakultas sudah terdaftar")
        
        try:
            self.repo.create(fak.id, fak.nama)
            return fak.model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, fid: str, fak: FakultasUpdate):
        rowcount = self.repo.update(fid, fak.nama)
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
        return {"id": fid, "nama": fak.nama}

    def delete(self, fid: str):
        rowcount = self.repo.delete(fid)
        if rowcount == 0:
            raise HTTPException(status_code=404, detail="Fakultas tidak ditemukan")
        return None