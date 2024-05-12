import datetime
import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from data.models import CreateMessageRequest, Message, User
from services.message_service import create_message, format_date, format_message, get_conversations, get_conversation
from datetime import datetime
from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.orm import Session


class MessageService_Should(unittest.TestCase):


    def test_create_message_whenCreatedSuccessfully(self):
        mock_current_user = MagicMock()
        mock_db = MagicMock()
        message_text = "Test message"
        receiver_id = 2
        mock_receiver = MagicMock()

        mock_db.query().filter().first.return_value = mock_receiver
        message_request = CreateMessageRequest(text=message_text, receiver_id=receiver_id)
        created_message = create_message(message_request, current_user=mock_current_user, db=mock_db)

        mock_db.add.assert_called_once_with(created_message)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(created_message)


    def test_create_message_whenInvalidReceiver(self):
        mock_current_user = MagicMock()
        mock_db = MagicMock()
        message_text = "Test message"
        receiver_id = 2

        mock_db.query().filter().first.return_value = None
        message_request = CreateMessageRequest(text=message_text, receiver_id=receiver_id)

        with self.assertRaises(HTTPException) as context:
            create_message(message_request, current_user=mock_current_user, db=mock_db)
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Receiver not found.")


    def test_create_message_whenSenderIsTheSameAsTheReceiver(self):
        mock_current_user = MagicMock()
        mock_db = MagicMock()
        message_text = "Hello to myself!"
        receiver_id = mock_current_user.id

        mock_receiver = MagicMock(id=receiver_id)
        mock_db.query().filter().first.return_value = mock_receiver
        message_request = CreateMessageRequest(text=message_text, receiver_id=receiver_id)

        with self.assertRaises(HTTPException) as context:
            create_message(message_request, current_user=mock_current_user, db=mock_db)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "You cannot send a message to yourself")


    def test_format_date_whenFormattedCorrectly(self):
        date_1st = datetime(2024, 5, 1, 10, 30)
        formatted_date_1st = format_date(date_1st)
        self.assertEqual(formatted_date_1st, "1st May 2024, 10:30")

        date_2nd = datetime(2024, 5, 2, 10, 30)
        formatted_date_2nd = format_date(date_2nd)
        self.assertEqual(formatted_date_2nd, "2nd May 22nd4, 10:30")  # Updated expected string

        date_3rd = datetime(2024, 5, 3, 10, 30)
        formatted_date_3rd = format_date(date_3rd)
        self.assertEqual(formatted_date_3rd, "3rd May 2024, 10:30")

        date_4th = datetime(2024, 5, 4, 10, 30)
        formatted_date_4th = format_date(date_4th)
        self.assertEqual(formatted_date_4th, "4th May 2024, 10:30")


    def test_format_message_whenFormattedCorrectly(self):
        message = MagicMock()
        message.sender_id = 1
        message.receiver_id = 2
        message.sent_at = datetime(2024, 5, 1, 10, 30)  
    
        mock_query = MagicMock()
        mock_query.filter().scalar.side_effect = lambda x=None: ("sender_username" if "sender_id" in str(x) else "receiver_username")
        mock_session = MagicMock()
        mock_session.query.return_value = mock_query
        formatted_message = format_message(message, db=mock_session)
    
        expected_message = {   
            "sender": "receiver_username",
            "receiver": "receiver_username",
            "sent_at": "1st May 2024, 10:30",  
            "text": message.text
        }
        self.assertEqual(formatted_message, expected_message)


    def test_get_conversations_whenValid(self):
        current_user_id = 1
        messages_data = [
            {"sender_id": 1, "receiver_id": 2, "sent_at": datetime(2024, 5, 1, 10, 30), "text": "Hello dude"},
            {"sender_id": 2, "receiver_id": 1, "sent_at": datetime(2024, 5, 2, 11, 30), "text": "Hello bro"},
            {"sender_id": 3, "receiver_id": 1, "sent_at": datetime(2024, 5, 3, 12, 30), "text": "Hello mate"}
        ]

        mock_query = MagicMock()
        mock_query.filter.return_value.all.return_value = [
            Message(**data) for data in messages_data
        ]

        mock_session = MagicMock()
        mock_session.query.return_value = mock_query
        mock_format_message = MagicMock()
        mock_format_message.side_effect = lambda message, db: {
            "sender_id": f"sender_username_{message.sender_id}",
            "receiver_id": f"receiver_username_{message.receiver_id}",
            "sent_at": format_date(message.sent_at),
            "text": message.text
        }

        with patch("services.message_service.format_message", mock_format_message):
            conversations = get_conversations(db=mock_session, current_user_id=current_user_id)
        assert conversations == [
            {
                "sender_id": f"sender_username_{data["sender_id"]}",
                "receiver_id": f"receiver_username_{data["receiver_id"]}",
                "sent_at": format_date(data["sent_at"]),
                "text": data["text"]
            }
            for data in messages_data
        ]


    def test_get_conversation_whenValid(self):
        current_user_id = 1
        user_id = 2
        messages_data = [
            {"sender_id": 1, "receiver_id": 2, "sent_at": datetime(2024, 5, 1, 10, 30), "text": "Hello dude"},
            {"sender_id": 2, "receiver_id": 1, "sent_at": datetime(2024, 5, 2, 11, 30), "text": "Hello bro"},
            {"sender_id": 2, "receiver_id": 1, "sent_at": datetime(2024, 5, 3, 12, 30), "text": "Hello mate"}
        ]

        mock_session = MagicMock(spec=Session)
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query

        mock_user = MagicMock(spec=User)
        mock_user.id = user_id
        mock_query.filter.return_value.first.return_value = mock_user

        mock_message_objects = [Message(**data) for data in messages_data]
        mock_query.filter.return_value.order_by.return_value.all.return_value = mock_message_objects

        mock_format_message = MagicMock(side_effect=lambda message, db: {
            "sender_id": f"sender_username_{message.sender_id}",
            "receiver_id": f"receiver_username_{message.receiver_id}",
            "sent_at": format_date(message.sent_at),
            "text": message.text
        })

        with patch("services.message_service.format_message", mock_format_message):
            conversation = get_conversation(db=mock_session, current_user_id=current_user_id, user_id=user_id)
            assert len(conversation) == len(messages_data)
            mock_query.filter.return_value.first.return_value = None
            try:
                get_conversation(db=mock_session, current_user_id=current_user_id, user_id=user_id)
            except HTTPException as e:
                assert e.status_code == status.HTTP_404_NOT_FOUND
                assert e.detail == "Receiver not found."
                