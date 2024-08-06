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
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";
import ArrowBack from "@mui/icons-material/ArrowBack";

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
        setReplies(response.data.replies);
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
                  <Button
                    variant="outlined"
                    onClick={() => handleVote(reply.id, "upvote")}
                  >
                    Upvote
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={() => handleVote(reply.id, "downvote")}
                  >
                    Downvote
                  </Button>
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
