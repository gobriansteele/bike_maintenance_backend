import bcrypt
import jwt

from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from core.models import crud


class LoginService:
    def __init__(self, db: Session):
        self.db = db

        self.SECRET_KEY = "79be86ca44bbbb18a4b371c61788d7f1af28aff300a2ff4149d40211c3149220"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.crud = crud

    def authenticate_user(self, username: str, password: str):
        user = crud.get_user_by_email(self.db, email=username)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        return self.create_access_token(data={"sub": user.email, "id": user.id})

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


    @staticmethod
    def verify_password(plain_password, hashed_password):
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password)

    @staticmethod
    def hash_password(password):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password

    @staticmethod
    def get_password_hash(password):
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        string_password = hashed_password.decode('utf8')
        return string_password


