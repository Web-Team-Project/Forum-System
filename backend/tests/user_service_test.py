import unittest
from unittest.mock import MagicMock

from data.models import User
from data.roles import Roles
from fastapi import HTTPException, status
from services.user_service import (
    check_admin_role,
    has_write_access,
    privileged_users,
    verify_username,
)
from sqlalchemy.orm import Session


class UserService_Should(unittest.TestCase):
    def test_category_raisesError_whenUserNotFound(self):
        db = MagicMock(spec=Session)
        category_id = 1
        current_user = MagicMock(spec=User)
        db.query().filter().first.return_value = None

        with self.assertRaises(HTTPException) as exc_info:
            privileged_users(db, category_id, current_user)
        self.assertEqual(exc_info.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(exc_info.exception.detail, "Category not found.")

    def test_username_whenUsernameExists(self):
        db = MagicMock(spec=Session)
        username = "test_user"
        db.query().filter().first.return_value = MagicMock(spec=User)
        result = verify_username(db, username)
        self.assertTrue(result)

    def test_username_whenItDoesNotExist(self):
        db = MagicMock(spec=Session)
        username = "non_existent_user"
        db.query().filter().first.return_value = None
        result = verify_username(db, username)
        self.assertFalse(result)

    def test_is_admin_whenRoleIsAdmin(self):
        current_user = MagicMock(spec=User)
        current_user.role = Roles.admin
        self.assertIsNone(check_admin_role(current_user))

    def test_user_raisesError_whenUnauthorized(self):
        with self.assertRaises(HTTPException) as exc_info:
            check_admin_role(None)
        self.assertEqual(exc_info.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            exc_info.exception.detail,
            "The user is not authorized to perform this action.",
        )

    def test_user_raisesError_whenInvalidRole(self):
        current_user = MagicMock(spec=User)
        current_user.role = "invalid_role"
        with self.assertRaises(HTTPException) as exc_info:
            check_admin_role(current_user)
        self.assertEqual(exc_info.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            exc_info.exception.detail,
            "The user is not authorized to perform this action.",
        )

    def test_user_raisesError_whenMissingRole(self):
        current_user = MagicMock(spec=User)
        del current_user.role
        with self.assertRaises(AttributeError):
            check_admin_role(current_user)

    def test_category_raisesError_whenCategoryWithUserNotFound(self):
        db = MagicMock(spec=Session)
        category_id = 1
        user_id = 1
        db.query().filter_by().first.return_value = None
        with self.assertRaises(HTTPException) as exc_info:
            has_write_access(db, category_id, user_id)
            self.assertEqual(exc_info.exception.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(
                exc_info.exception.detail, f"Category with ID {category_id} not found."
            )
