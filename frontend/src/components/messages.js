import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import UserContext from "../utils/context";

const Messages = () => {
    const { user } = useContext(UserContext);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [receiverId, setReceiverId] = useState("");
    const [userId, setUserId] = useState("");
    const [users, setUsers] = useState([]);
  
    useEffect(() => {
      const viewMessages = async () => {
        try {
          const response = await api.get("/messages/conversations/", {
            headers: {
              Authorization: `Bearer ${user.token}`,
            },
          });
          setMessages(response.data);

          const uniqueUsers = [...new Set(response.data.map(message => ({id: message.sender_id, name: message.sender})).concat(response.data.map(message => ({id: message.receiver_id, name: message.receiver}))))];
          setUsers(uniqueUsers);
        } catch (error) {
          console.error(error);
        }
      };
  
      const viewConversation = async () => {
        if (userId) {
          try {
            const response = await api.get(`/messages/conversations/${userId}`, {
              headers: {
                Authorization: `Bearer ${user.token}`,
              },
            });
            setMessages(response.data);
          } catch (error) {
            console.error(error);
          }
        }
      };
  
      viewMessages();
      viewConversation();
    }, [user, userId]);

  const sendMessage = async () => {
    try {
      const response = await api.post("/messages", {
        text: newMessage,
        receiver_id: receiverId,
      }, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        },
      });
      console.log(response.data);
      setMessages([...messages, response.data]);
      setNewMessage("");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Messages</h1>
      <select onChange={e => setUserId(e.target.value)}>
        {users.map((user, index) => (
          <option key={index} value={user.id}>{user.name}</option>
        ))}
      </select>
      {messages.map((message, index) => (
        <div key={index}>
          <p><strong>Sender:</strong> {message.sender}</p>
          <p><strong>Receiver:</strong> {message.receiver}</p>
          <p><strong>Sent at:</strong> {message.sent_at}</p>
          <p><strong>Text:</strong> {message.text}</p>
        </div>
      ))}
      <input type="text" value={newMessage} onChange={e => setNewMessage(e.target.value)} placeholder="New Message" />
      <input type="text" value={receiverId} onChange={e => setReceiverId(e.target.value)} placeholder="Receiver ID" />
      <button onClick={sendMessage}>Send Message</button>
      <Link to="/categories">
        <button>Back to Categories</button>
      </Link>
    </div>
  );
};

export default Messages;