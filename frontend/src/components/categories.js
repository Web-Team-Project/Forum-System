import React, { useState, useEffect, useContext } from "react";
import api from "../api";
import UserContext from "../utils/context";

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const { user } = useContext(UserContext);
  const [newCategoryName, setNewCategoryName] = useState("");

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await api.get("/categories/", {
          headers: {
            Authorization: `Bearer ${user.token}`,
          }
        });
        setCategories(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchCategories();
  }, [user]);

  const createCategory = async () => {
    try {
      const response = await api.post("/categories/", {
        name: newCategoryName,
      }, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        }
      });
      console.log(response.data);
      setCategories([...categories, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Categories</h1>
      {categories.map((category) => (
        <div key={category.id}>
          <h2>{category.name}</h2>
        </div>
      ))}
      <input type="text" value={newCategoryName} onChange={e => setNewCategoryName(e.target.value)} placeholder="New Category Name" />
      <button onClick={createCategory}>Create Category</button>
    </div>
  );
};

export default Categories;