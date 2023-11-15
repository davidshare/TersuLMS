from fastapi import APIRouter, Depends
from .controller import AuthController
from  .schemas import UserLoginCreate
from .dependencies import AuthDependencies

router = APIRouter()

@router.post("/")
def create(user_data: UserLoginCreate = Depends(AuthDependencies.password_length_validator)):
    return AuthController.create(user_data)