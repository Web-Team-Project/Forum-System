import unittest
from unittest.mock import MagicMock, Mock, patch

from data.models import Category, Topic, User
from data.roles import Roles
from fastapi import HTTPException, status
from services import category_service as service


class CategoryService_Should(unittest.TestCase):
    @patch("services.category_service.get_current_user")
    @patch("services.category_service.Session")
    def test_get_category_whenValidParams(self, mock_session, mock_get_current_user):
        mock_user = User(id=1, role=Roles.admin)
        mock_get_current_user.return_value = mock_user
        mock_db = mock_session()
        mock_category = Category(id=1, name="Test Category", is_private=False)
        mock_db.query().filter().first.return_value = mock_category

        category_id = 1
        result = service.get_category(mock_db, category_id)
        self.assertEqual(result, mock_category)
        mock_db.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as cm:
            service.get_category(mock_db, category_id)
        self.assertEqual(cm.exception.status_code, status.HTTP_404_NOT_FOUND)

    @patch("services.category_service.get_current_user")
    @patch("services.category_service.Session")
    def test_get_categories_whenValidParams(self, mock_session, mock_get_current_user):
        mock_user = User(id=1, role=Roles.admin)
        mock_get_current_user.return_value = mock_user
        mock_db = mock_session()
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [
            Category(id=1, name="Test Category1", is_private=False),
            Category(id=2, name="Test Category2", is_private=False),
        ]
        mock_db.query = Mock(return_value=mock_query)
        result = service.get_categories(mock_db, current_user=mock_user)
        result_dicts = [
            {k: getattr(cat, k) for k in cat.__dict__ if not k.startswith("_")}
            for cat in result
        ]
        expected_dicts = [
            {"id": 1, "name": "Test Category1", "is_private": False},
            {"id": 2, "name": "Test Category2", "is_private": False},
        ]
        self.assertEqual(result_dicts, expected_dicts)

    def test_toggle_category_whenWorksCorrectly(self):
        mock_db = MagicMock()
        mock_current_user = MagicMock(role=Roles.admin)
        category_id = 1
        mock_category = Category(id=category_id, name="Test Category", is_private=False)
        with patch("services.category_service.get_category") as mock_get_category:
            mock_get_category.return_value = mock_category
            service.toggle_category_visibility(
                category_id, db=mock_db, current_user=mock_current_user
            )
            mock_get_category.assert_called_once_with(
                mock_db, category_id, mock_current_user
            )
            mock_db.commit.assert_called_once()
            expected_is_private_after = not mock_category.is_private
            self.assertNotEqual(mock_category.is_private, expected_is_private_after)

    def test_get_topics_in_category_whenSuccessful(self):
        mock_db = MagicMock()
        category_id = 1
        mock_topics = [
            Topic(id=1, title="Topic 1", category_id=category_id),
            Topic(id=2, title="Topic 2", category_id=category_id),
        ]

        mock_db.query().filter().offset().limit().all.return_value = mock_topics
        topics = service.get_topics_in_category(mock_db, category_id)
        mock_db.query().filter().offset().limit().all.assert_called_once()
        self.assertEqual(topics, mock_topics)

    def test_get_topics_in_category_raisesError_whenNoTopicsFound(self):
        mock_db = MagicMock()
        category_id = 1
        mock_db.query().filter().offset().limit().all.return_value = []
        with self.assertRaises(HTTPException) as context:
            service.get_topics_in_category(mock_db, category_id)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "No topics found in the category.")

    def test_check_if_private_public_category_whenWorksCorrectly(self):
        mock_category = MagicMock(is_private=False)
        with self.assertRaises(HTTPException) as context:
            service.check_if_private(mock_category)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "The category is public.")

    def test_read_access_whenUserIsAdmin(self):
        mock_current_user = MagicMock(role=Roles.admin)
        MagicMock(is_private=False)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        result = service.read_access(
            mock_db, category_id, user_id, current_user=mock_current_user
        )
        self.assertEqual(result["message"], "Read permission has been granted.")

    def test_read_access_private_category_with_access_whenGivenCorrectly(self):
        mock_current_user = MagicMock(role=Roles.user)
        MagicMock(is_private=True)
        mock_access_record = MagicMock(read_access=True)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        mock_db.query().filter_by().first.return_value = mock_access_record
        with patch("services.category_service.check_admin_role"):
            result = service.read_access(
                mock_db, category_id, user_id, current_user=mock_current_user
            )
        self.assertEqual(result["message"], "Read permission has been granted.")

    def test_read_access_private_category_raisesError_whenNoAccessGiven(self):
        mock_current_user = MagicMock(role=Roles.user)
        MagicMock(is_private=True)
        mock_access_record = MagicMock(read_access=False)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        mock_db.query().filter_by().first.return_value = mock_access_record
        with self.assertRaises(HTTPException) as context:
            service.read_access(
                mock_db, category_id, user_id, current_user=mock_current_user
            )
        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            context.exception.detail,
            "The user is not authorized to perform this action.",
        )

    def test_read_access_public_category_whenGivenCorrectly(self):
        mock_current_user = MagicMock(role=Roles.admin)
        MagicMock(is_private=False)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        with patch("services.category_service.check_admin_role"):
            result = service.read_access(
                mock_db, category_id, user_id, current_user=mock_current_user
            )
        result = service.read_access(
            mock_db, category_id, user_id, current_user=mock_current_user
        )
        self.assertEqual(result["message"], "Read permission has been granted.")

    def test_write_access_whenUserIsAdmin(self):
        mock_current_user = MagicMock(role=Roles.admin)
        MagicMock(is_private=True)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        mock_db.query().filter_by().first.return_value = None
        result = service.write_access(
            mock_db, category_id, user_id, current_user=mock_current_user
        )
        self.assertEqual(result["message"], "Write permission has been granted.")

    def test_write_access_raisesError_whenNoAccessGiven(self):
        mock_current_user = MagicMock(role=Roles.user)
        MagicMock(is_private=True)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        mock_access_record = MagicMock(read_access=True, write_access=False)
        mock_db.query().filter_by().first.return_value = mock_access_record
        with self.assertRaises(HTTPException) as context:
            service.write_access(
                mock_db, category_id, user_id, current_user=mock_current_user
            )
        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            context.exception.detail,
            "The user is not authorized to perform this action.",
        )

    def test_write_access_whenGivenPermission(self):
        mock_current_user = MagicMock(role=Roles.admin)
        MagicMock(is_private=True)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        with patch("services.category_service.check_admin_role"):
            result = service.read_access(
                mock_db, category_id, user_id, current_user=mock_current_user
            )
        mock_access_record = MagicMock(read_access=True, write_access=True)
        mock_db.query().filter_by().first.return_value = mock_access_record
        result = service.write_access(
            mock_db, category_id, user_id, current_user=mock_current_user
        )
        self.assertEqual(result["message"], "Write permission has been granted.")

    def test_revoke_user_access_whenReadIsRevoked(self):
        mock_current_user = MagicMock(role=Roles.admin)
        mock_access_record = MagicMock(read_access=True, write_access=False)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        access_type = "read"
        mock_db.query().filter_by().first.return_value = mock_access_record
        result = service.revoke_user_access(
            mock_db, category_id, user_id, access_type, current_user=mock_current_user
        )
        self.assertEqual(
            result["message"], f"The user's {access_type} access has been revoked."
        )

    def test_revoke_user_access_whenWriteIsRevoked(self):
        mock_current_user = MagicMock(role=Roles.admin)
        mock_access_record = MagicMock(read_access=True, write_access=True)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        access_type = "write"
        mock_db.query().filter_by().first.return_value = mock_access_record
        result = service.revoke_user_access(
            mock_db, category_id, user_id, access_type, current_user=mock_current_user
        )
        self.assertEqual(
            result["message"], f"The user's {access_type} access has been revoked."
        )

    def test_revoke_user_access_raisesError_whenUserNoPermissions(self):
        mock_current_user = MagicMock(role=Roles.admin)
        mock_access_record = MagicMock(read_access=False, write_access=False)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        access_type = "read"
        mock_db.query().filter_by().first.return_value = mock_access_record
        with self.assertRaises(HTTPException) as context:
            service.revoke_user_access(
                mock_db,
                category_id,
                user_id,
                access_type,
                current_user=mock_current_user,
            )
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            context.exception.detail, "The user does not have any permissions."
        )

    def test_revoke_user_access_raisesError_whenInvalidAccessType(self):
        mock_current_user = MagicMock(role=Roles.admin)
        mock_access_record = MagicMock(read_access=True, write_access=False)
        mock_db = MagicMock()
        category_id = 1
        user_id = 1
        access_type = "invalid"
        mock_db.query().filter_by().first.return_value = mock_access_record
        with self.assertRaises(HTTPException) as context:
            service.revoke_user_access(
                mock_db,
                category_id,
                user_id,
                access_type,
                current_user=mock_current_user,
            )
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "Invalid access type.")

    def test_lock_category_whenItWorksCorrectly(self):
        mock_current_user = MagicMock(role=Roles.admin)
        mock_db = MagicMock()
        category_id = 1
        mock_category = Category(id=category_id, name="Test Category", is_locked=False)
        mock_db.query(Category).get.return_value = mock_category
        result = service.lock_category_for_users(
            category_id, mock_current_user, mock_db
        )
        self.assertTrue(mock_category.is_locked)
        mock_db.commit.assert_called_once()
        self.assertEqual(result["message"], "Category has been locked.")
