import React, { useState, useEffect, useContext } from "react";
import api from "../api";
import UserContext from "../utils/context";


const Categories = () => {
  const [categories, setCategories] = useState([]);
  const { user } = useContext(UserContext);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get("/categories", {
          headers: {
            Authorization: `Bearer ${user.token}`
          }
        });
        setCategories(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchCategories();
  }, [user]);

  return (
    <div>
      <h1>Categories</h1>
      {categories.map((category) => (
        <div key={category.id}>
          <h2>{category.name}</h2>
        </div>
      ))}
    </div>
  );
};

export default Categories;