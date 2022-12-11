from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderModel(BaseModel):
    total_price: float = Field(...)
    products: List[str] = Field(...)
    date: datetime = Field(...)
    buyer_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "total_price": 449.90,
                "products": [],
                "date": '2021-11-10T11:15:00+00:00',
                "buyer_id": "638e05540b71cfeb1c5a4892"
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message
    }