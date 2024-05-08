import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import UserContext from '../utils/context';


const Category = () => {
  const { id } = useParams();
  const { user } = useContext(UserContext);
  const [category, setCategory] = useState(null);

  useEffect(() => {
    const fetchCategory = async () => {
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

    fetchCategory();
  }, [id, user]);

  if (!category) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{category.name}</h1>
    </div>
  );
};

export default Category;