from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Extra, EmailStr
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                'username': "bhargav",
                'email': "bhargav@gmail.com",
                'password': "bhargav2800",
                'is_staff': False,
                "is_active": True
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                'quantity': 2,
                'pizza_size': "LARGE"
            }
        }
        # extra = Extra.allow  # Allow extra fields when parsing


class FormDataModel(BaseModel):
    name: str = Form(...)
    email: EmailStr = Form(...)
    phone_number: str = Form(...)