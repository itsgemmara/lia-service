from pydantic import BaseModel, EmailStr, field_validator, Field
from beanie import Document
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException


class ProductBase(BaseModel):
    name: str = Field(max_length=255)
    price: float
    description: str = "No description available" 

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 3:
            raise HTTPException(status_code=400, detail="Validation error: The name must be at least 3 characters long")
        return value

    @field_validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise HTTPException(status_code=400, detail="Validation error: The price can't be a negative number")
        return value
    

class Product(Document, ProductBase):
    class Settings:
        collection = "products"  


class ProductUpdate(Product):
    name: str = Field(None)
    price: float = Field(None)
    description: str = Field(None)