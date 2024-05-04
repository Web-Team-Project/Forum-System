from unittest.mock import Mock

from data_folder.models import User
from data_folder.roles import Roles

def fake_category():
    return {"id": 1, "name": "Test Category"}

def fake_admin():
    return {"username": "admin", "id": 1}

def fake_user():
    user = Mock()
    # You can add attributes or methods as needed
    user.role = Roles.user  # Assuming the default role for non-admin users is 'user'
    return user
