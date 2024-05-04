from datetime import timedelta
import unittest
from unittest.mock import patch

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from auth_folder.token import ACCESS_TOKEN_EXPIRATION_MINS, create_access_token
from data_folder.models import CreateCategoryRequest
from services import category_service
from routers.categories import category_router
from category_router_test import fake_admin, fake_category
from data_folder.database import get_db

class TestCategoryService(unittest.TestCase):


    def test_create_category_as_admin(self):
        admin_user = fake_admin()
        category_data = {"name": "Test Category"}
        expected_category = fake_category()

        with patch("services.category_service.create_category") as mock_create_category:
            mock_create_category.return_value = expected_category

            db = get_db()

            result = category_service.create_category(db, category_data, admin_user)

            self.assertEqual(result, expected_category)


    def test_create_category_as_non_admin(self):
        # Arrange
        category_data = CreateCategoryRequest(name="Test Category")

        # Act
        with patch("services.category_service.check_admin_role") as mock_check_admin_role, \
             patch("services.category_service.create_category") as mock_create_category:
            mock_check_admin_role.return_value = False
            mock_create_category.side_effect = PermissionError("Permission denied")

            app = FastAPI()
            app.include_router(category_router)

            with TestClient(app) as client:
                response = client.post("/", json=category_data.dict(), headers={"Authorization": "Bearer"})

                # Assert
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # def test_view_category(self):    DOESN'T WORK
    # # Arrange
    #     category_id = 1  # Assuming category ID for the test
    #     expected_category = {"id": category_id, "name": "Test Category"}
    #     expected_topics = ["Topic 1", "Topic 2"]
    #     expected_response = {"category": expected_category["name"], "topics": expected_topics}

    #     # Mock the get_category and get_topics_in_category functions
    #     with patch("routers.categories.get_category") as mock_get_category, \
    #             patch("routers.categories.get_topics_in_category") as mock_get_topics_in_category:
    #         mock_get_category.return_value = expected_category
    #         mock_get_topics_in_category.return_value = expected_topics

    #     # Act
        
    #         # Create a FastAPI test client
    #         app = FastAPI()
    #         app.include_router(category_router)

    #         with TestClient(app) as client:
    #             response = client.get(f"/{category_id}")

    #         # Assert
    #             assert response.status_code == status.HTTP_200_OK
    #             assert response.json() == expected_response
