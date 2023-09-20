import pytest
from app.models.owner import Owner


@pytest.fixture
def sample_owner_data():
    return {
        "name": "John",
        "last_name": "Doe",
        "number": "09131234569",
        "meli_code": "1234567890",
        "email": "john@example.com",
        "is_active": True,
    }

class TestOwnerModel:
    def test_create_owner(self, sample_owner_data):
        owner = Owner(**sample_owner_data)
        assert owner.name == "John"
        assert owner.is_active == True

    def test_update_owner(self, sample_owner_data):
        owner = Owner(**sample_owner_data)
        owner.update_owner_data({"name": "Updated Name"})
        assert owner.name == "Updated Name"

    def test_deactivate_owner(self, sample_owner_data):
        owner = Owner(**sample_owner_data)
        owner.deactivate()
        assert owner.is_active == False
