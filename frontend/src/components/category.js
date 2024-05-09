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
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{category.category}</h1>
      <h2>Topics:</h2>
      <ul>
        {category.topics.map((topic, index) => (
          <li key={index}>
            <Link to={`/topics/${topic.id}`}>{topic}</Link>
          </li>
        ))}
      </ul>
      <input type="text" value={newTopicTitle} onChange={e => setNewTopicTitle(e.target.value)} placeholder="New Topic Title" />
      <button onClick={createTopic}>Create Topic</button>
    </div>
  );
};

export default Category;