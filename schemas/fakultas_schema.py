from pydantic import BaseModel


class FakultasCreate(BaseModel):
    id: str
    nama: str


class FakultasUpdate(BaseModel):
    nama: str