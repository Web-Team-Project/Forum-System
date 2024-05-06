from unittest.mock import Mock

from data.models import User
from data.roles import Roles


def fake_admin( username = "admin", role = "admin"):
    user = Mock(spec=User)
    user.username = username
    user.id = id
    user.role = role
    # user.access_token = "mock_access_token"
    return user

def fake_user():
    user = Mock()
    # You can add attributes or methods as needed
    user.role = Roles.user  # Assuming the default role for non-admin users is 'user'
    return user

class MockCategory:
    def __init__(self, id, name, is_private=False):
        self.id = id
        self.name = name
        self.is_private = is_private

def fake_category():
    return MockCategory(1, "Test Category")

def create_test_user(username="user", role="user"):
    user = Mock(spec=User)
    user.username = username
    user.role = role
    # user.access_token = "mock_access_token"  # Adding a mock access token for testing purposes
    return user


def create_test_category(name="Test Category", is_private=False):
    return MockCategory(id=1, name=name, is_private=is_private)

