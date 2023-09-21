import pytest
from pydantic import ValidationError
from fastapi import  HTTPException

from app.main import app
from app.models.product import ProductBase


class TestProductModel:
    @pytest.fixture
    def valid_product_data(self):
        return {
            "name": "Valid Product",
            "price": 19.99,
            "description": "A valid product for testing.",
        }

    def test_valid_product(self, valid_product_data):
        # Create an instance of ProductBase with valid data
        product = ProductBase(**valid_product_data)
        assert product.name == valid_product_data["name"]
        assert product.price == valid_product_data["price"]
        assert product.description == valid_product_data["description"]

    def test_invalid_name(self):
        with pytest.raises(HTTPException) as exc_info:
            # Attempt to create an instance of ProductBase with an invalid name
            invalid_product_data = {
                "name": "A",  # Name is too short
                "price": 19.99,
                "description": "An invalid product with a short name.",
            }
            ProductBase(**invalid_product_data)

        assert "The name must be at least 3 characters long" in str(exc_info.value)

    def test_negative_price(self):
        with pytest.raises(HTTPException) as exc_info:
            # Attempt to create an instance of ProductBase with a negative price
            invalid_product_data = {
                "name": "Invalid Product",
                "price": -5,  # Price is negative
                "description": "An invalid product with a negative price.",
            }
            ProductBase(**invalid_product_data)

        assert "The price can't be a negative number" in str(exc_info.value)
