from pydantic import BaseModel, Field
from typing import Optional, List


class ProductModel(BaseModel):
    name: str = Field(...)
    title: str = Field(default=None)
    color: str = Field(...)
    price: float = Field(...)
    tags: List[str] = Field(default=None)
    seller_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "T-shirt",
                "title": "100'%' cotton",
                "color": "Black",
                "price": 115.80,
                "tags": ["Clothes"],
                "seller_id": "638e05540b71cfeb1c5a4892",
            }
        }


class UpdateProductModel(BaseModel):
    name: Optional[str]
    title: Optional[str]
    color: Optional[str]
    price: Optional[float]
    tags: Optional[List[str]]


    class Config:
        schema_extra = {
            "example": {
                "name": "Coat",
                "title": "Polyaster Coat by Vans",
                "color": "Black",
                "price": 315,
                "tags": ["Women", "Winter"]
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message
    }