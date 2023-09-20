from pydantic import BaseModel, EmailStr, field_validator, Field
from beanie import Document
from pydantic import ValidationError


class ProductBase(BaseModel):
    name: str = Field(max_length=255)
    price: float
    description: str

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValidationError("The name must be at least 3 characters long")

    @field_validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValidationError("The price can't be a negative number")


class Product(Document, ProductBase):
    class Settings:
        collection = "owners"
