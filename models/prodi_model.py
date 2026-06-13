# models/prodi_model.py
from sqlalchemy import Column, String
from database import Base

class Prodi(Base):
    __tablename__ = "prodi"
    id = Column(String(10), primary_key=True, index=True)
    nama = Column(String(100))
    fakultas = Column(String(100))