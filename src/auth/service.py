from fastapi import Depends
from sqlalchemy.orm import Session
from .models import UserLogin
from .schemas import UserLoginCreate
from ..config.database import get_db

class AuthService:

    @staticmethod
    def create(user_data: UserLoginCreate, db: Session = Depends(get_db)):
        user = UserLogin(**user_data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
