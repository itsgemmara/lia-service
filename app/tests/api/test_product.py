import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from fastapi import  HTTPException

from app.main import app
from app.models.product import ProductBase

sample_product_data = {
    "name": "Sample Product",
    "price": 10.99,
    "description": "A sample product for testing.",
}


@pytest.fixture(scope='session')
def client():
    with TestClient(app) as _client:
        yield _client


class TestGetProductDetailAPI:

    @pytest.fixture(scope='function')
    def created_product(self, client):
        response = client.post("/products", json=sample_product_data)
        product = response.json()
        yield product

        product_id = product.get("_id", None)
        if product_id:
            client.delete(f"/products/{product_id}")

    def test_get_product_detail(self, client, created_product):
        product = created_product
        product_id = product.get("_id", None)
        assert product_id is not None
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["name"] == sample_product_data["name"]
        assert response.json()["price"] == sample_product_data["price"]
        assert response.json()["description"] == sample_product_data["description"]

    def test_get_product_detail_not_found(self, client: TestClient):
        non_existent_id = "650ba5aeceaf5cb3a53ca28c"
        response = client.get(f"/products/{non_existent_id}")
        assert response.status_code == 404
        error_response = response.json()
        assert "detail" in error_response
        assert error_response["detail"] == "Product not found"
        assert response.headers["content-type"] == "application/json"

    def test_get_product_detail_invalid_id(self, client: TestClient):
        invalid_id = "invalid_id"
        response = client.get(f"/products/{invalid_id}")
        assert response.status_code == 400
        error_response = response.json()
        assert "detail" in error_response
        assert error_response["detail"] == "Invalid product_id"
        assert response.headers["content-type"] == "application/json"


class TestFetchProductsAPI:

    @pytest.fixture(scope='function')
    def created_products(self, client):
        created_product_ids = []

        for _ in range(2):
            response = client.post("/products", json=sample_product_data)
            product = response.json()
            created_product_ids.append(product["_id"])

        yield created_product_ids

        for product_id in created_product_ids:
            if product_id:
                client.delete(f"/products/{product_id}")

    def test_fetch_products(self, client, created_products):
        response = client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) >= 2


class TestDeleteProductAPI:

    @pytest.fixture(scope='function')
    def created_product(self, client):
        response = client.post("/products", json=sample_product_data)
        product = response.json()
        yield product

        product_id = product.get("_id", None)
        if product_id:
            client.delete(f"/products/{product_id}")

    def test_delete_product(self, client, created_product):
        product = created_product
        product_id = product.get("_id", None)
        assert product_id is not None
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        response = client.get(f"/products/{product_id}")
        assert response.status_code == 404

    def test_delete_non_existent_product(self, client):
        non_existent_id = "650ba5aeceaf5cb3a53ca28c"
        response = client.delete(f"/products/{non_existent_id}")
        assert response.status_code == 404

    def test_delete_product_with_invalid_id(self, client):
        invalid_id = "invalid_id_format"
        response = client.delete(f"/products/{invalid_id}")
        assert response.status_code == 400

    def test_delete_product_without_id(self, client):
        response = client.delete("/products/")
        assert response.status_code == 405 


class TestCreateProductAPI:

    def test_create_product(self, client):
        response = client.post("/products", json=sample_product_data)
        assert response.status_code == 201  
        created_product = response.json()
        assert created_product["name"] == sample_product_data["name"]
        assert created_product["price"] == sample_product_data["price"]
        assert created_product["description"] == sample_product_data["description"]

    def test_create_product_invalid_data(self, client):
        invalid_data = {
            "name": "",  # Invalid name
            "price": -1,   # Invalid price
            "description": "A sample product for testing.",
        }
        response = client.post("/products", json=invalid_data)
        assert response.status_code == 400  


class TestUpdateProductAPI:

    @pytest.fixture(scope='function')
    def created_product(self, client):
        response = client.post("/products", json=sample_product_data)
        created_product = response.json()
        yield created_product
        product_id = created_product.get("_id")
        if product_id:
            client.delete(f"/products/{product_id}")

    def test_update_product(self, client, created_product):
        updated_data = {
            "name": "Updated Product Name",
            "price": 19.99,
            "description": "Updated description.",
        }
        response = client.put(f"/products/{created_product['_id']}", json=updated_data)
        assert response.status_code == 200  
        updated_product = response.json()
        assert updated_product["name"] == updated_data["name"]
        assert updated_product["price"] == updated_data["price"]
        assert updated_product["description"] == updated_data["description"]

    def test_update_non_existent_product(self, client):
        non_existent_id = "650ba5aeceaf5cb3a53ca28c"
        updated_data = {
            "name": "Updated Product Name",
            "price": 19.99,
            "description": "Updated description.",
        }
        response = client.put(f"/products/{non_existent_id}", json=updated_data)
        assert response.status_code == 404  

    def test_update_product_invalid_data(self, client, created_product):
        # Test updating a product with invalid data
        invalid_data = {
            "name": "",  # Invalid: Empty name
            "price": -5,  # Invalid: Negative price
            "description": "Updated description.",
        }
        response = client.put(f"/products/{created_product['_id']}", json=invalid_data)
        assert response.status_code == 400  

    def test_update_product_without_data(self, client, created_product):
        response = client.put(f"/products/{created_product['_id']}", json={})
        assert response.status_code == 200
