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


        const uniqueUsers = [...new Set(response.data.map(message => message.sender).concat(response.data.map(message => message.receiver)))];
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
    <div style={{ border: "5px solid #4CAF50", padding: "20px", margin: "10px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ borderBottom: "2px solid #4CAF50", color: "#333", marginBottom: "20px" }}>Messages</h1>
      <select onChange={e => setUserId(e.target.value)} style={{ margin: "20px 0", padding: "5px", width: "100%", border: "1px solid #ddd", borderRadius: "5px" }}>
        {users.map((user, index) => (
          <option key={index} value={user}>{user}</option>
        ))}
      </select>
      {messages.map((message, index) => (
        <div key={index} style={{ margin: "20px 0", padding: "10px", border: "1px solid #4CAF50", borderRadius: "5px", boxShadow: "0 2px 5px rgba(0,0,0,0.15)" }}>
          <p><strong>Sender:</strong> {message.sender}</p>
          <p><strong>Receiver:</strong> {message.receiver}</p>
          <p><strong>Sent at:</strong> {message.sent_at}</p>
          <p><strong>Text:</strong> {message.text}</p>
        </div>
      ))}
      <input type="text" value={newMessage} onChange={e => setNewMessage(e.target.value)} placeholder="New Message" style={{ margin: "20px 0", padding: "5px", width: "100%", border: "1px solid #ddd", borderRadius: "5px" }} />
      <input type="text" value={receiverId} onChange={e => setReceiverId(e.target.value)} placeholder="Receiver ID" style={{ margin: "20px 0", padding: "5px", width: "100%", border: "1px solid #ddd", borderRadius: "5px" }} />
      <button onClick={sendMessage} style={{ backgroundColor: "#ddd", color: "#333", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>Send Message</button>
      <div style={{ textAlign: "right" }}>
        <Link to="/categories" style={{ textDecoration: "none", color: "#4CAF50", fontWeight: "bold" }}>Back to Categories</Link>
      </div>
    </div>
  );
};

export default Messages;