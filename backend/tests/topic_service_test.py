import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from data.models import Topic, User
from services.topic_service import create_topic, get_topics


class TestTopicService(unittest.TestCase):

    @patch("services.topic_service.has_write_access")
    @patch("services.topic_service.Session")
    def test_create_topic(self, mock_session, mock_has_write_access):
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
    def test_create_topic_no_access(self, mock_session, mock_get_current_user):
        mock_user = User(id=2, role="user")
        mock_topic_request = MagicMock(category_id=1, title="Test Topic")
        mock_db = mock_session()
        mock_get_current_user.return_value = mock_user
        mock_db.add.side_effect = HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        with self.assertRaises(HTTPException):
            create_topic(mock_db, mock_topic_request, mock_user)

    # @patch("services.topic_service.get_current_user")
    # @patch("services.topic_service.Session")
    # def test_get_topic(self, mock_session, mock_get_current_user):
    #     mock_user = User(id=1, role="admin")
    #     mock_get_current_user.return_value = mock_user
    #     mock_db = mock_session()
    #
    #     mock_query = MagicMock()
    #     mock_db.query.return_value = mock_query
    #     mock_query.all.return_value = [Topic(id=1, title="Sport Cars")]
    #
    #     result = get_topics(mock_db, 0, 100, None, None, mock_user)
    #
    #     self.assertEqual(len(result), 1)
    #     self.assertEqual(result[0].title, "Sport Cars")
