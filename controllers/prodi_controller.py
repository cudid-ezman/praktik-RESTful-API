# controllers/prodi_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import dependencies
from database import get_db
from dependencies import verify_token
from schemas.base_schema import APIResponse
from schemas.prodi_schema import ProdiCreate, ProdiUpdate
from services.prodi_service import ProdiService

# Inisialisasi router khusus Prodi
router = APIRouter(prefix="/prodi", tags=["Program Studi"])

# Endpoint GET tidak kita beri proteksi agar semua orang bisa melihat data
@router.get("", status_code=200, response_model=APIResponse[list], description="Menampilkan data prodi")
@router.get("/", status_code=200, response_model=APIResponse[list], description="Menampilkan data prodi")
def list_prodi(db: Session = Depends(get_db)):
    service = ProdiService(db)
    data = service.get_all()
    return APIResponse(
        status="success",
        message="Berhasil mengambil daftar prodi",
        data=data
    )

# Endpoint POST, PUT, DELETE kita proteksi dengan Depends(verify_token)
@router.post("", status_code=201, response_model=APIResponse[dict], description="Menambahkan data prodi baru")
@router.post("/", status_code=201, response_model=APIResponse[dict], description="Menambahkan data prodi baru")
def create_prodi(pro: ProdiCreate, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    service = ProdiService(db)
    data = service.create(pro)
    return APIResponse(
        status="success",
        message="Data prodi berhasil ditambahkan",
        data=data
    )

@router.get("/{prodi_id}", status_code=200, response_model=APIResponse[dict], description="Mengambil detail data prodi")
def get_prodi(prodi_id: str, db: Session = Depends(get_db)):
    service = ProdiService(db)
    data = service.get_by_id(prodi_id)
    if not data:
        raise HTTPException(status_code=404, detail="Prodi tidak ditemukan")
    return APIResponse(
        status="success",
        message="Berhasil mengambil detail prodi",
        data=data
    )

@router.put("/{prodi_id}", status_code=200, response_model=APIResponse[dict], description="Memperbarui data prodi")
def update_prodi(prodi_id: str, pro: ProdiUpdate, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    service = ProdiService(db)
    data = service.update(prodi_id, pro)
    return APIResponse(
        status="success",
        message="Data prodi berhasil diperbarui",
        data=data
    )

@router.delete("/{prodi_id}", status_code=200, response_model=APIResponse[None], description="Menghapus data prodi")
def delete_prodi(prodi_id: str, db: Session = Depends(get_db), user_info: dict = Depends(verify_token)):
    service = ProdiService(db)
    service.delete(prodi_id)
    return APIResponse(
        status="success",
        message=f"Data prodi dengan ID {prodi_id} berhasil dihapus",
        data=None
    )