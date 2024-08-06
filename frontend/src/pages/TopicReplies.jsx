import React, { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import api from "../api";
import {
  Container,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Stack,
  IconButton,
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";
import ArrowBack from "@mui/icons-material/ArrowBack";
import ThumbUp from "@mui/icons-material/ThumbUp";
import ThumbDown from "@mui/icons-material/ThumbDown";

const TopicReplies = () => {
  const { topicId } = useParams();
  const navigate = useNavigate();
  const [replies, setReplies] = useState([]);
  const [newReply, setNewReply] = useState("");
  const [bestReplyId, setBestReplyId] = useState(null);

  useEffect(() => {
    const viewReplies = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(`/topics/${topicId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const fetchedReplies = response.data.replies.map((reply) => ({
          ...reply,
          upvotes: reply.upvotes || 0,
          downvotes: reply.downvotes || 0,
        }));
        setReplies(fetchedReplies);
        setBestReplyId(response.data.topic.best_reply_id);
      } catch (error) {
        console.error(error);
      }
    };

    viewReplies();
  }, [topicId]);

  const handleReplySubmit = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.post(
        "/replies/",
        { content: newReply, topic_id: topicId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setReplies([...replies, { ...response.data, upvotes: 0, downvotes: 0 }]);
      setNewReply("");
    } catch (error) {
      console.error(error);
    }
  };

  const handleVote = async (replyId, voteType) => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.post(
        `/replies/${replyId}/vote`,
        { vote_type: voteType === "upvote" ? 1 : -1 },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const updatedReplies = replies.map((reply) =>
        reply.id === replyId
          ? {
              ...reply,
              upvotes:
                voteType === "upvote" ? reply.upvotes + 1 : reply.upvotes,
              downvotes:
                voteType === "downvote" ? reply.downvotes + 1 : reply.downvotes,
            }
          : reply
      );
      setReplies(updatedReplies);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSetBestReply = async (replyId) => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.post(
        `/replies/${replyId}/best-reply?topic_id=${topicId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setBestReplyId(replyId);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleGoBack = (e) => {
    e.preventDefault();
    navigate(-1);
  };

  return (
    <>
      <Header />
      <Container component="main" maxWidth="md" sx={{ padding: "20px" }}>
        <Typography component="h1" variant="h5">
          Replies for Topic {topicId}
        </Typography>
        {replies.map((reply) => (
          <Card key={reply.id} sx={{ margin: "20px 0" }}>
            <CardContent>
              <Typography variant="body1">{reply.content}</Typography>
              <Typography variant="body2">
                Upvotes: {reply.upvotes} | Downvotes: {reply.downvotes}
              </Typography>
              {bestReplyId === reply.id && (
                <Typography variant="body2" color="primary">
                  Best Reply
                </Typography>
              )}
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "10px",
                }}
              >
                <Stack direction="row" spacing={2}>
                  <IconButton
                    color="primary"
                    onClick={() => handleVote(reply.id, "upvote")}
                  >
                    <ThumbUp />
                  </IconButton>
                  <IconButton
                    color="secondary"
                    onClick={() => handleVote(reply.id, "downvote")}
                  >
                    <ThumbDown />
                  </IconButton>
                  <Button
                    variant="outlined"
                    onClick={() => handleSetBestReply(reply.id)}
                  >
                    Set as Best Reply
                  </Button>
                </Stack>
              </Box>
            </CardContent>
          </Card>
        ))}
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="newReply"
          label="New Reply"
          name="newReply"
          autoComplete="newReply"
          autoFocus
          value={newReply}
          onChange={(e) => setNewReply(e.target.value)}
          multiline
          rows={4}
        />
        <Button
          type="button"
          fullWidth
          variant="contained"
          color="primary"
          onClick={handleReplySubmit}
        >
          Add Reply
        </Button>
        <Box sx={{ textAlign: "right", marginTop: 2 }}>
          <Link
            to="#"
            onClick={handleGoBack}
            style={{ textDecoration: "none" }}
          >
            <ArrowBack sx={{ marginRight: 1 }} />
            Back to Topics
          </Link>
        </Box>
      </Container>
      <Footer />
    </>
  );
};

export default TopicReplies;
