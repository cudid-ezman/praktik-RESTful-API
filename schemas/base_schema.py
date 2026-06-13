# schemas/base_schema.py
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

# T adalah tipe data generik yang akan diisi dengan schema entitas secara dinamis
# (misal: dict, list, schema Prodi)
T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: Optional[T] = None