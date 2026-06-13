# controllers/fakultas_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from dependencies import verify_token
from schemas.base_schema import APIResponse
from schemas.fakultas_schema import FakultasCreate, FakultasUpdate
from services.fakultas_service import FakultasService

router = APIRouter(prefix="/fakultas", tags=["Fakultas"])

@router.get("/", status_code=200, response_model=APIResponse[list], description="Mengambil semua daftar fakultas")
def list_fakultas(db: Session = Depends(get_db)):
    service = FakultasService(db)
    data = service.get_all()
    return APIResponse(status="success", message="Berhasil mengambil daftar fakultas", data=data)

@router.get("/{id}", status_code=200, response_model=APIResponse[dict], description="Mengambil detail fakultas berdasarkan ID")
def get_fakultas(id: str, db: Session = Depends(get_db)):
    service = FakultasService(db)
    data = service.get_by_id(id)
    return APIResponse(status="success", message="Berhasil mengambil detail fakultas", data=data)

@router.post("/", status_code=201, response_model=APIResponse[dict], description="Menyimpan data fakultas baru")
def create_fakultas(fak: FakultasCreate, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    service = FakultasService(db)
    data = service.create(fak)
    return APIResponse(status="success", message="Data fakultas berhasil ditambahkan", data=data)

@router.put("/{id}", status_code=200, response_model=APIResponse[dict], description="Mengubah data fakultas")
def update_fakultas(id: str, fak: FakultasUpdate, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    service = FakultasService(db)
    data = service.update(id, fak)
    return APIResponse(status="success", message="Data fakultas berhasil diperbarui", data=data)

@router.delete("/{id}", status_code=200, response_model=APIResponse[None], description="Menghapus data fakultas")
def delete_fakultas(id: str, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    service = FakultasService(db)
    service.delete(id)
    return APIResponse(status="success", message=f"Data dengan ID {id} berhasil dihapus", data=None)