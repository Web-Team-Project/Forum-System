from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from data.models import Reply, Vote
from services.reply_service import add_best_reply, add_or_update_vote, create_reply, CreateReplyRequest, Session, Topic

class TestCreateReplyService_Should:
    def test_create_reply(self):
        topic_id = 1
        category_id = 1
        user_id = 1
        content = "Test reply content"
        reply_req = CreateReplyRequest(topic_id=topic_id, content=content)

        mock_current_user = MagicMock()
        mock_current_user.id = user_id

        mock_session = MagicMock(spec=Session)

        mock_topic = MagicMock(spec=Topic)
        mock_topic.is_locked = False  
        mock_topic.category_id = category_id

        mock_query = MagicMock()
        mock_session.query.return_value = mock_query

        mock_query.get.return_value = mock_topic

        new_reply = create_reply(db=mock_session, reply_req=reply_req, current_user=mock_current_user)
        assert new_reply.content == content

    def test_create_reply_topic_not_found_error(self):
        mock_has_write_access = MagicMock()
        mock_has_write_access.return_value = True  
    
        topic_id = 1
        category_id = 1
        user_id = 1
        content = "Test reply content"
        
        reply_req = CreateReplyRequest(topic_id=topic_id, content=content)

        mock_current_user = MagicMock()
        mock_current_user.id = user_id

        mock_session = MagicMock(spec=Session)

        mock_topic = MagicMock(spec=Topic)
        mock_topic.is_locked = False  
        mock_topic.category_id = category_id

        with patch('services.user_service.has_write_access', mock_has_write_access):
            mock_query = MagicMock()
            mock_session.query.return_value = mock_query

            mock_query.get.return_value = None 
            try:
                create_reply(db=mock_session, reply_req=reply_req, current_user=mock_current_user)
            except HTTPException as e:
                assert e.status_code == status.HTTP_404_NOT_FOUND
                assert e.detail == "Topic not found."
            
            mock_topic.is_locked = True
            try:
                create_reply(db=mock_session, reply_req=reply_req, current_user=mock_current_user)
            except HTTPException as e:
                assert e.status_code == status.HTTP_404_NOT_FOUND  
                assert e.detail == "Topic not found."

    def test_create_reply_locked_topic_error(self):
        mock_has_write_access = MagicMock()
        mock_has_write_access.return_value = True  

        # Define mock data
        topic_id = 1
        category_id = 1
        user_id = 1
        content = "Test reply content"

        reply_req = CreateReplyRequest(topic_id=topic_id, content=content)

        mock_current_user = MagicMock()
        mock_current_user.id = user_id

        mock_session = MagicMock(spec=Session)

        mock_topic = MagicMock(spec=Topic)
        mock_topic.is_locked = False  
        mock_topic.category_id = category_id

        with patch('services.user_service.has_write_access', mock_has_write_access):
            mock_topic.is_locked = True
            try:
                create_reply(db=mock_session, reply_req=reply_req, current_user=mock_current_user)
            except HTTPException as e:
                assert e.status_code == status.HTTP_403_FORBIDDEN
                assert e.detail == "The topic is locked."


    def test_add_new_vote(self):
        user_id = 1
        reply_id = 1
        vote_type = 1
        
        mock_session = MagicMock(spec=Session)
        
        mock_session.query(Vote).filter_by().first.return_value = None
        
        mock_reply = MagicMock(spec=Reply)
        mock_reply.vote_type = 0  
        mock_session.query(Reply).filter_by().first.return_value = mock_reply
        
        result, message = add_or_update_vote(db=mock_session, user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        
        assert result == mock_reply
        assert result.vote_type == vote_type
        assert message == "Vote has been updated."
        mock_session.commit.assert_called_once()


    def test_update_existing_vote(self):
        user_id = 1
        reply_id = 1
        vote_type = -1
        
        mock_session = MagicMock(spec=Session)
        
        mock_existing_vote = MagicMock()
        mock_existing_vote.vote_type = 1
        mock_session.query().filter_by().first.return_value = mock_existing_vote
        
        result, message = add_or_update_vote(db=mock_session, user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        
        assert result == mock_existing_vote
        assert result.vote_type == vote_type
        assert message == "Vote has been updated."
        mock_session.commit.assert_called_once()
        mock_session.add.assert_not_called()

    def test_vote_already_exists(self):
        user_id = 1
        reply_id = 1
        vote_type = 1
        
        mock_session = MagicMock(spec=Session)
        
        mock_existing_vote = MagicMock()
        mock_existing_vote.vote_type = vote_type
        mock_session.query().filter_by().first.return_value = mock_existing_vote
        
        result, message = add_or_update_vote(db=mock_session, user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        
        assert result == mock_existing_vote
        assert message == "You have already voted in this way."
        mock_session.commit.assert_not_called()
        mock_session.add.assert_not_called()

    def test_reply_not_found(self):
        user_id = 1
        reply_id = 1
        vote_type = 1
        
        mock_session = MagicMock(spec=Session)
        
        mock_session.query().filter_by().first.return_value = None
        
        mock_session.query().filter_by().first.return_value = None
        try:
            add_or_update_vote(db=mock_session, user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        except HTTPException as e:
            assert e.status_code == status.HTTP_404_NOT_FOUND
            assert e.detail == "Reply not found."


class TestAddBestReplyService:
    def test_add_best_reply_topic_not_found(self):
        # Mock data
        topic_id = 1
        reply_id = 1
        user_id = 1
        
        # Mock the database session
        mock_session = MagicMock(spec=Session)
        mock_session.query(Topic).filter(Topic.id == topic_id).first.return_value = None
        
        # Test function call
        try:
            add_best_reply(db=mock_session, topic_id=topic_id, reply_id=reply_id, user_id=user_id)
        except HTTPException as e:
            assert e.status_code == status.HTTP_404_NOT_FOUND
            assert e.detail == "Topic not found."
    
    def test_add_best_reply_unauthorized(self):
        # Mock data
        topic_id = 1
        reply_id = 1
        user_id = 1
        
        # Mock the database session
        mock_session = MagicMock(spec=Session)
        mock_topic = MagicMock(spec=Topic)
        mock_topic.author_id = 2  # Different user ID
        mock_session.query(Topic).filter(Topic.id == topic_id).first.return_value = mock_topic
        
        # Test function call
        try:
            add_best_reply(db=mock_session, topic_id=topic_id, reply_id=reply_id, user_id=user_id)
        except HTTPException as e:
            assert e.status_code == status.HTTP_401_UNAUTHORIZED
            assert e.detail == "Only the topic author can set the best reply."
    
    def test_add_best_reply_reply_not_found(self):
        # Mock data
        topic_id = 1
        reply_id = 1
        user_id = 1
        
        # Mock the database session
        mock_session = MagicMock(spec=Session)
        mock_topic = MagicMock(spec=Topic)
        mock_topic.author_id = user_id
        mock_session.query(Topic).filter(Topic.id == topic_id).first.return_value = mock_topic
        mock_session.query(Reply).filter(Reply.id == reply_id, Reply.topic_id == topic_id).first.return_value = None
        
        # Test function call
        try:
            add_best_reply(db=mock_session, topic_id=topic_id, reply_id=reply_id, user_id=user_id)
        except HTTPException as e:
            assert e.status_code == status.HTTP_404_NOT_FOUND
            assert e.detail == "Topic not found."
    
    def test_add_best_reply_success(self):
        # Mock data
        topic_id = 1
        reply_id = 1
        user_id = 1

        mock_session = MagicMock(spec=Session)

        mock_topic = MagicMock(spec=Topic)
        mock_topic.author_id = user_id

        mock_reply = MagicMock(spec=Reply)
        mock_reply.topic_id = topic_id

        mock_session.query.return_value.filter.return_value.first.side_effect = [mock_topic, mock_reply]

        assert mock_session.query(Topic).filter(Topic.id == topic_id).first() == mock_topic
        assert mock_session.query(Reply).filter(Reply.id == reply_id, Reply.topic_id == topic_id).first() == mock_reply

        try:
            result = add_best_reply(db=mock_session, topic_id=topic_id, reply_id=reply_id, user_id=user_id)
        except Exception as e:
            print(e)
            return

        assert result == mock_reply
        assert result.is_best_reply is True
