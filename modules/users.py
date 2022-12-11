from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class UserModel(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    city: str = Field(...)
    address: str = Field(...)
    phone: str = Field(...)
    status: str = Field(default="buyer")
    orders: List[str] = Field(default=None)


    class Config:
        schema_extra = {
            "example": {
                "email": "israel@gmail.com",
                "first_name": "Israel",
                "last_name": "Israeli",
                "city": "Tel Aviv",
                "address": "Ha Yarkon 118",
                "phone": "0524446689",
                "status": "buyer",
                "orders": []
            }
        }


class UpdateUserModel(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    city: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    status: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "email": "israeli@gmail.com",
                "first_name": "Israel",
                "last_name": "Israeli",
                "city": "Jaffo",
                "address": "Rabeno Yeruham",
                "phone": "0526860098",
                "status": "seller",
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message
    }