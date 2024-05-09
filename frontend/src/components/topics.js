import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import UserContext from "../utils/context";

const Topics = () => {
  const [topics, setTopics] = useState([]);
  const { user } = useContext(UserContext);
  const [newTopicName, setNewTopicName] = useState("");

  useEffect(() => {
    const viewTopics = async () => {
      try {
        const response = await api.get("/topics/", {
          headers: {
            Authorization: `Bearer ${user.token}`,
          }
        });
        setTopics(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    viewTopics();
  }, [user]);

  const createTopic = async () => {
    try {
      const response = await api.post("/topics/", {
        name: newTopicName,
      }, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        }
      });
      console.log(response.data);
      setTopics([...topics, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ border: "5px solid #4CAF50", padding: "20px", margin: "10px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ borderBottom: "2px solid #4CAF50", color: "#333", marginBottom: "20px" }}>Topics</h1>
      {topics.map((topic) => (
        <div key={topic.id} style={{ margin: "20px 0", padding: "10px", border: "1px solid #4CAF50", borderRadius: "5px", boxShadow: "0 2px 5px rgba(0,0,0,0.15)" }}>
          <h2 style={{ color: "#333", marginBottom: "10px" }}>{topic.name}</h2>
          <Link to={`/topics/${topic.id}`} style={{ textDecoration: "none", color: "#4CAF50", marginRight: "10px" }}>
            <button style={{ backgroundColor: "#ddd", color: "#333", marginRight: "10px", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>View Topic</button>
          </Link>
        </div>
      ))}
      <input type="text" value={newTopicName} onChange={e => setNewTopicName(e.target.value)} placeholder="" style={{ margin: "20px 0", padding: "5px", width: "100%", border: "1px solid #ddd", borderRadius: "5px" }} />
      <button style={{ backgroundColor: "#ddd", color: "#333", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onClick={createTopic} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>Create Topic</button>
    </div>
  );
};

export default Topics;