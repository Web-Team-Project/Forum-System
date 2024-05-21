import React, { useEffect, useState, useContext } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import UserContext from '../utils/context';


const Category = () => {
  const { id } = useParams();
  const { user } = useContext(UserContext);
  const [category, setCategory] = useState(null);
  const [newTopicTitle, setNewTopicTitle] = useState("");

  useEffect(() => {
    const viewCategory = async () => {
      try {
        const response = await api.get(`/categories/${id}`, {
          headers: {
            Authorization: `Bearer ${user.token}`,
          }
        });
        setCategory(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    viewCategory();
  }, [id, user]);

  const createTopic = async () => {
    try {
      const response = await api.post("/topics/", {
        title: newTopicTitle,
        category_id: id,
      }, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        }
      });
      console.log(response.data);
      setCategory(prevState => ({...prevState, topics: [...prevState.topics, newTopicTitle]}));
      setNewTopicTitle("");
    } catch (error) {
      console.error(error);
    }
  };

  if (!category) {
    return <div></div>;
  }

  return (
    <div style={{ border: "5px solid #4CAF50", padding: "20px", margin: "10px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ borderBottom: "2px solid #4CAF50", color: "#333", marginBottom: "20px" }}>{category.category}</h1>
      <h2>Topics:</h2>
      <ul>
        {category.topics.map((topic, index) => (
          <li key={index} style={{ margin: "20px 0", padding: "10px", border: "1px solid #4CAF50", borderRadius: "5px", boxShadow: "0 2px 5px rgba(0,0,0,0.15)" }}>
            <Link to={`/topics/${topic.id}`}>{topic}</Link>
          </li>
        ))}
      </ul>
      <input type="text" value={newTopicTitle} onChange={e => setNewTopicTitle(e.target.value)} placeholder="" style={{ margin: "20px 0", padding: "5px", width: "100%", border: "1px solid #ddd", borderRadius: "5px" }} />
      <button style={{ backgroundColor: "#ddd", color: "#333", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onClick={createTopic} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>Create Topic</button>
    </div>
  );
};

export default Category;