# models/fakultas_model.py
from sqlalchemy import Column, String
from database import Base

class Fakultas(Base):
    __tablename__ = "fakultas"
    id = Column(String(10), primary_key=True, index=True)
    nama = Column(String(100))