from datetime import timedelta
import unittest
from unittest.mock import MagicMock, patch

from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from auth.token import ACCESS_TOKEN_EXPIRATION_MINS, create_access_token, get_current_user
from data.models import CreateCategoryRequest
from services import category_service
from routers.categories import category_router, create_new_category
from category_router_test import create_test_category, create_test_user, fake_admin, fake_category, fake_user
from data.database import get_db

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



    def test_get_category(self):
    # Arrange
        category_data = CreateCategoryRequest(name="Test Category")
        expected_category = fake_category() 
        admin_user = fake_admin() 

        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value

        def get_category_side_effect(db, category_id, current_user):
            if category_id == expected_category.id: 
                return expected_category
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Category not found.")

    # Act
        with patch("services.category_service.check_admin_role") as mock_check_admin_role, \
                patch("services.category_service.get_category") as mock_get_category:
            mock_check_admin_role.return_value = False  

            mock_get_category.side_effect = get_category_side_effect

            result = category_service.get_category(mock_session, 1, admin_user) 

    # Assert
        self.assertEqual(result, expected_category)


    def test_get_categories_as_user(self):
        # Test getting categories as a regular user

        # Create a FastAPI application instance
        app = FastAPI()
        app.include_router(category_router)

        # Mock the session and other dependencies
        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
    
        # Create a mock user object with an access_token attribute
        normal_user = MagicMock()
        normal_user.access_token = "fake_access_token"
    
        # Override the get_current_user dependency to return the mock user object
        mock_session.dependency_overrides[get_current_user] = lambda: normal_user

        # Use the TestClient with the FastAPI application instance
        with TestClient(app) as client:
            # Make the request with the user's access token
            response = client.get("/categories", headers={"Authorization": f"Bearer {normal_user.access_token}"})

            # Assert that the response status code is HTTP 401 UNAUTHORIZED
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            categories = response.json()
            # Assert that only 1 category is returned
            self.assertEqual(len(categories), 1)


    def test_get_categories_as_admin(self):
        # Test getting categories as an admin user Doesnt work because of the access_tokens
    
        app = FastAPI()
        app.include_router(category_router)
    
        mock_session = MagicMock()
        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_session.dependency_overrides[get_current_user] = fake_admin

    
        with TestClient(app) as client:
            admin = create_test_user(username="admin", role="admin")
            admin.access_token = "Must be a valid token!!!"
        
            category_ids = [create_test_category(name=f"Category {i}").id for i in range(10)]
        
            
            response = client.get("/categories")
                                #   headers={"Authorization": f"Bearer {admin.access_token}"})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            categories = response.json()
            self.assertEqual(len(categories), 10)


    def test_get_categories_with_search(self):
        app = FastAPI()
        app.include_router(category_router)

        with patch("services.category_service.check_admin_role") as mock_check_admin_role:
            mock_check_admin_role.return_value = True

        with TestClient(app) as client:
            category1 = create_test_category(name="Apple")
            category2 = create_test_category(name="Banana")
            category3 = create_test_category(name="Orange")

            response = client.get("/categories?search=a", headers={"Authorization": "Bearer fake_token"})

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            categories = response.json()
            self.assertEqual(len(categories), 1)  # Apple
