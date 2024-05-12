import unittest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from data.models import User
from data.roles import Roles
from unittest.mock import MagicMock
from services.user_service import privileged_users, verify_username, check_admin_role, has_write_access


class UserService_Should(unittest.TestCase):


    def test_category_not_found(self):
        # Arrange
        db = MagicMock(spec=Session)
        category_id = 1
        current_user = MagicMock(spec=User)
        db.query().filter().first.return_value = None
        
        # Act and Assert
        with self.assertRaises(HTTPException) as exc_info:
            privileged_users(db, category_id, current_user)
        self.assertEqual(exc_info.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(exc_info.exception.detail, "Category not found.")


    def test_username_exists(self):
        # Arrange
        db = MagicMock(spec=Session)
        username = "test_user"
        db.query().filter().first.return_value = MagicMock(spec=User)
        
        # Act
        result = verify_username(db, username)
        
        # Assert
        self.assertTrue(result)


    def test_username_does_not_exist(self):
        # Arrange
        db = MagicMock(spec=Session)
        username = "non_existent_user"
        db.query().filter().first.return_value = None 
        
        # Act
        result = verify_username(db, username)
        
        # Assert
        self.assertFalse(result)


    def test_is_admin(self):
        # Arrange
        current_user = MagicMock(spec=User)
        current_user.role = Roles.admin
        
        # Act and Assert
        self.assertIsNone(check_admin_role(current_user))


    def test_with_none_user(self):
        # Act and Assert
        with self.assertRaises(HTTPException) as exc_info:
            check_admin_role(None)
        self.assertEqual(exc_info.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(exc_info.exception.detail, "The user is not authorized to perform this action.")


    def test_with_invalid_user_role(self):
        # Arrange
        current_user = MagicMock(spec=User)
        current_user.role = "invalid_role" 
        
        # Act and Assert
        with self.assertRaises(HTTPException) as exc_info:
            check_admin_role(current_user)
        self.assertEqual(exc_info.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(exc_info.exception.detail, "The user is not authorized to perform this action.")


    def test_with_missing_user_role(self):
        # Arrange
        current_user = MagicMock(spec=User)
        del current_user.role
        
        # Act and Assert
        with self.assertRaises(AttributeError):
            check_admin_role(current_user)


    def test_category_not_found(self):
        # Arrange
        db = MagicMock(spec=Session)
        category_id = 1
        user_id = 1
        db.query().filter_by().first.return_value = None
        
        # Act and Assert
        with self.assertRaises(HTTPException) as exc_info:
            has_write_access(db, category_id, user_id)
            self.assertEqual(exc_info.exception.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(exc_info.exception.detail, f"Category with ID {category_id} not found.")
