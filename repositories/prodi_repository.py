# repositories/prodi_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import text

class ProdiRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_prodi(self):
        query = text("SELECT * FROM prodi")
        return [dict(item) for item in self.db.execute(query).mappings().fetchall()]

    def get_prodi_by_id(self, pid: str):
        query = text("SELECT * FROM prodi WHERE id=:pid")
        result = self.db.execute(query, {"pid": pid}).mappings().fetchone()
        return dict(result) if result else None

    def create_prodi(self, pid: str, pnama: str, pfakultas: str):
        query = text("INSERT INTO prodi VALUES (:pid, :pnama, :pfakultas)")
        self.db.execute(query, {"pid": pid, "pnama": pnama, "pfakultas": pfakultas})
        self.db.commit()

    def update_prodi(self, pid: str, pnama: str, pfakultas: str):
        query = text("UPDATE prodi SET nama=:pnama, fakultas=:pfakultas WHERE id=:pid")
        result = self.db.execute(query, {
            "pid": pid, "pnama": pnama, "pfakultas": pfakultas
        })
        self.db.commit()
        return result.rowcount

    def delete_prodi(self, pid: str):
        query = text("DELETE FROM prodi WHERE id=:pid")
        result = self.db.execute(query, {"pid": pid})
        self.db.commit()
        return result.rowcount