import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import UserContext from '../utils/context';


const Category = () => {
  const { id } = useParams();
  const { user } = useContext(UserContext);
  const [category, setCategory] = useState(null);

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

  if (!category) {
    return
  }

  return (
    <div>
      <h1>{category.name}</h1>
      <h2>Topics:</h2>
      <ul>
        {category.topics.map((topic, index) => (
          <li key={index}>{topic}</li>
        ))}
      </ul>
    </div>
  );
};

export default Category;