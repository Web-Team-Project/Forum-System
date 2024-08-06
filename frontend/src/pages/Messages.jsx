import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import Header from "../components/Header";
import Footer from "../components/Footer";
import {
  Container,
  Typography,
  Select,
  MenuItem,
  TextField,
  Button,
  Card,
  CardContent,
  Box,
  Stack,
} from "@mui/material";
import ArrowBack from "@mui/icons-material/ArrowBack";

const Messages = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [receiverId, setReceiverId] = useState("");
  const [userId, setUserId] = useState("");
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const viewMessages = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get("/messages/conversations/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setMessages(response.data);

        const uniqueUsers = [
          ...new Set(
            response.data
              .map((message) => message.sender)
              .concat(response.data.map((message) => message.receiver))
          ),
        ];
        setUsers(uniqueUsers);
      } catch (error) {
        console.error(error);
      }
    };

    viewMessages();
  }, []);

  const sendMessage = async () => {
    const token = localStorage.getItem("token");
    if (!newMessage || !receiverId) {
      console.error("Message text and receiver ID are required.");
      return;
    }
    try {
      const response = await api.post(
        "/messages/",
        { text: newMessage, receiver_id: receiverId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      console.log(response.data);
      setNewMessage("");
      setReceiverId("");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Header />
      <Container component="main" maxWidth="md" sx={{ padding: "20px" }}>
        <Typography component="h1" variant="h5">
          Messages
        </Typography>
        <Select
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          fullWidth
          variant="outlined"
          margin="dense"
        >
          <MenuItem value="">All Users</MenuItem>
          {users.map((user, index) => (
            <MenuItem key={index} value={user}>
              {user}
            </MenuItem>
          ))}
        </Select>
        {messages
          .filter(
            (message) =>
              !userId ||
              message.sender === userId ||
              message.receiver === userId
          )
          .map((message, index) => (
            <Card key={index} variant="outlined" sx={{ marginBottom: 2 }}>
              <CardContent>
                <Typography variant="body1">
                  <strong>Sender:</strong> {message.sender}
                </Typography>
                <Typography variant="body1">
                  <strong>Receiver:</strong> {message.receiver}
                </Typography>
                <Typography variant="body1">
                  <strong>Sent at:</strong> {message.sent_at}
                </Typography>
                <Typography variant="body1">
                  <strong>Text:</strong> {message.text}
                </Typography>
              </CardContent>
            </Card>
          ))}
        <TextField
          label="New Message"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          fullWidth
          variant="outlined"
          margin="normal"
        />
        <TextField
          label="Receiver ID"
          value={receiverId}
          onChange={(e) => setReceiverId(e.target.value)}
          fullWidth
          variant="outlined"
          margin="normal"
        />
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <Stack direction="row" spacing={2}>
            <Button
              onClick={sendMessage}
              variant="outlined"
              color="primary"
              sx={{ marginTop: 2 }}
            >
              Send Message
            </Button>
          </Stack>
        </Box>
        <Box sx={{ textAlign: "right", marginTop: 2 }}>
          <Link to="/categories" style={{ textDecoration: "none" }}>
            <ArrowBack sx={{ marginRight: 1 }} />
            Back to Categories
          </Link>
        </Box>
      </Container>
      <Footer />
    </>
  );
};

export default Messages;
