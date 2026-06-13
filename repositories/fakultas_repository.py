# repositories/fakultas_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import text

class FakultasRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        query = text("SELECT * FROM fakultas")
        return self.db.execute(query).mappings().fetchall()

    def get_by_id(self, fid: str):
        query = text("SELECT * FROM fakultas WHERE id=:fid")
        return self.db.execute(query, {"fid": fid}).mappings().fetchone()

    def create(self, fid: str, fnama: str):
        query = text("INSERT INTO fakultas VALUES (:fid, :fnama)")
        self.db.execute(query, {"fid": fid, "fnama": fnama})
        self.db.commit()

    def update(self, fid: str, fnama: str):
        query = text("UPDATE fakultas SET nama=:fnama WHERE id=:fid")
        result = self.db.execute(query, {"fid": fid, "fnama": fnama})
        self.db.commit()
        return result.rowcount

    def delete(self, fid: str):
        query = text("DELETE FROM fakultas WHERE id=:fid")
        result = self.db.execute(query, {"fid": fid})
        self.db.commit()
        return result.rowcount