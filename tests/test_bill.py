from uuid import uuid7

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from bill_splitter_api.bill.schemas import CreateBillResponse
from bill_splitter_api.models import Bill


class TestCreateBillSuccess:
    def test_create_bill_returns_201_and_creates_db_entry(
        self,
        client: TestClient,
        session: Session,
    ):
        # Arrange
        bill_data = {
            "name": "Dinner Bill",
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": 25.00,
                    "participants": [{"id": str(uuid7()), "text": "Alice"}],
                },
                {
                    "name": "Drinks",
                    "amount": 15.00,
                    "participants": [
                        {"id": str(uuid7()), "text": "Alice"},
                        {"id": str(uuid7()), "text": "Bob"},
                    ],
                },
            ],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

        response = CreateBillResponse.model_validate(response.json())
        assert response.name == "Dinner Bill"
        assert len(response.bill_items) == 2

        bill = session.scalars(select(Bill).where(Bill.id == response.id)).first()
        assert bill is not None
        assert bill.name == response.name
        assert len(bill.bill_items) == len(response.bill_items)


class TestCreateBillValidationErrors:
    def test_create_bill_missing_name_returns_422(self, client: TestClient):
        # Arrange
        bill_data = {
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": 25.50,
                    "participants": [{"id": str(uuid7()), "text": "Alice"}],
                },
            ],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_bill_empty_name_returns_422(self, client: TestClient):
        # Arrange
        bill_data = {
            "name": "",
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": 25.50,
                    "participants": [{"id": str(uuid7()), "text": "Alice"}],
                },
            ],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_bill_empty_items_returns_422(self, client: TestClient):
        # Arrange
        bill_data = {
            "name": "Empty Bill",
            "bill_items": [],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_bill_item_invalid_amount_returns_422(self, client: TestClient):
        # Arrange
        bill_data = {
            "name": "Invalid Bill",
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": -5.00,
                    "participants": [{"id": str(uuid7()), "text": "Alice"}],
                },
            ],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_bill_item_zero_amount_returns_422(
        self, client: TestClient, auth_token: str
    ):
        # Arrange
        bill_data = {
            "name": "Invalid Bill",
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": 0,
                    "participants": [{"id": str(uuid7()), "text": "Alice"}],
                },
            ],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_bill_item_no_participants_returns_422(self, client: TestClient):
        # Arrange
        bill_data = {
            "name": "Invalid Bill",
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": 25.50,
                    "participants": [],
                },
            ],
        }

        # Act
        response = client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestCreateBillUnauthorized:
    def test_create_bill_without_auth_returns_401(
        self, unauthenticated_client: TestClient
    ):
        # Arrange
        bill_data = {
            "name": "Dinner Bill",
            "bill_items": [
                {
                    "name": "Pizza",
                    "amount": 25.50,
                    "participants": [{"id": str(uuid7()), "text": "Alice"}],
                },
            ],
        }

        # Act
        response = unauthenticated_client.post("/bills", json=bill_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
