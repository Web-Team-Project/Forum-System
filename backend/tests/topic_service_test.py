import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from data.models import User
from services.topic_service import create_topic


class TopicService_Should(unittest.TestCase):


    @patch("services.topic_service.has_write_access")
    @patch("services.topic_service.Session")
    def test_create_topic_whenCreatedSuccessfully(self, mock_session, mock_has_write_access):
        mock_user = User(id=1, role="user")
        mock_topic_request = MagicMock(category_id=1, title="Test Topic")
        mock_db = mock_session()

        result = create_topic(mock_db, mock_topic_request, mock_user)
        self.assertIsNotNone(result)
        mock_has_write_access.assert_called_with(mock_db, 1, 1)
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()


    @patch("services.topic_service.get_current_user")
    @patch("services.topic_service.Session")
    def test_create_topic_raisesError_whenNoAccess(self, mock_session, mock_get_current_user):
        mock_user = User(id=2, role="user")
        mock_topic_request = MagicMock(category_id=1, title="Test Topic")
        mock_db = mock_session()
        mock_get_current_user.return_value = mock_user
        mock_db.add.side_effect = HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        with self.assertRaises(HTTPException):
            create_topic(mock_db, mock_topic_request, mock_user)