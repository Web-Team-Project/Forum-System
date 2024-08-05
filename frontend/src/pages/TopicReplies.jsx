import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import {
  Container,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  Box,
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";

const TopicReplies = () => {
  const { topicId } = useParams();
  const [replies, setReplies] = useState([]);
  const [newReply, setNewReply] = useState("");

  useEffect(() => {
    const viewReplies = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(`/topics/${topicId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setReplies(response.data.replies);
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
      setReplies([...replies, response.data]);
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
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
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
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "10px",
                }}
              >
                <Button
                  variant="contained"
                  onClick={() => handleVote(reply.id, "upvote")}
                >
                  Upvote
                </Button>
                <Button
                  variant="contained"
                  onClick={() => handleVote(reply.id, "downvote")}
                >
                  Downvote
                </Button>
                <Button
                  variant="contained"
                  onClick={() => handleSetBestReply(reply.id)}
                >
                  Set as Best Reply
                </Button>
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
      </Container>
      <Footer />
    </>
  );
};

export default TopicReplies;
