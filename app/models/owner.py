from pydantic import BaseModel, EmailStr, field_validator, Field
from beanie import Document

from validators.meli_code import MelliCodeValidator
from validators.phone_validator import PhoneNumberValidator


class UserBase(BaseModel):
    name: str
    last_name: str
    number: str
    meli_code: str
    email: EmailStr
    is_active: bool = True

    @field_validator('meli_code')
    def validate_meli_code(cls, value):
        return MelliCodeValidator(value).validate()[0]

    @field_validator("number")
    def validate_number(cls, value):
        phone_validator = PhoneNumberValidator(value)
        validated_number = phone_validator.validator()
        return validated_number


class Owner(Document, UserBase):
    class Settings:
        collection = "owners"


class OwnerUpdate(Owner):
    name: str = Field(None)
    last_name: str = Field(None)
    number: str = Field(None)
    meli_code: str = Field(None)
    email: EmailStr = Field(None)
    is_active: bool = Field(None)