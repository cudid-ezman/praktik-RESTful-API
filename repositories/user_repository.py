# repositories/user_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import text

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        query = text("SELECT * FROM users WHERE username=:u")
        return self.db.execute(query, {"u": username}).mappings().fetchone()

    def create_user(self, username: str, hashed_password: str, role: str = "admin"):
        query = text("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)")
        self.db.execute(query, {"u": username, "p": hashed_password, "r": role})
        self.db.commit()