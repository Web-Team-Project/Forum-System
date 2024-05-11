import unittest
from unittest.mock import Mock, patch
from routers import categories as category_router

from data.models import User
from data.roles import Roles

mock_category_service = Mock("services.category_service")
mock_topic_service = Mock("services.topic_service")
mock_user_serivce = Mock("services.user_service")

category_router.category_service = mock_category_service
category_router.topic_service = mock_topic_service
category_router.user_service = mock_user_serivce


def fake_admin():
    admin = Mock()
    admin.role = Roles.admin

def fake_user():
    user = Mock()
    # You can add attributes or methods as needed
    user.role = Roles.user  # Assuming the default role for non-admin users is 'user'
    return user


def fake_category():
    category = Mock()

    return category

def create_test_user(username="user", role="user"):
    user = Mock(spec=User)
    user.username = username
    user.role = role
    # user.access_token = "mock_access_token"  # Adding a mock access token for testing purposes
    return user

class CategoriesRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_category_service.reset_mock()
        mock_topic_service.reset_mock()
        mock_user_serivce.reset_mock()

    def test_get_categories_returnsAllCategoies_whenUserIsAdmin(self):
        with patch("routers.categories.get_categories") as get_categories_func, \
                patch("routers.users.check_admin_role"):
            # Arrange
            test_categories = [fake_category(), fake_category()]
        
            # Configure the mock to return test_categories
            get_categories_func.return_value = test_categories
        
            # Act
            result = category_router.get_categories()
        
            # Assert
            self.assertEqual(test_categories, result)
