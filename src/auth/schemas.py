import datetime
from pydantic import BaseModel

class UserloginDataCreate(BaseModel):
    email:str
    password:str
    login_name:str


