import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import UserContext from "../utils/context";


const Categories = () => {
  const [categories, setCategories] = useState([]);
  const { user } = useContext(UserContext);
  const [newCategoryName, setNewCategoryName] = useState("");

  useEffect(() => {
    const viewCategories = async () => {
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

    viewCategories();
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

  const viewCategory = async (categoryId) => {
    try {
      const response = await api.get(`/categories/${categoryId}`, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const changeVisibility = async (categoryId) => {
    try {
      const response = await api.put(`/categories/${categoryId}/visibility`, {}, {
        headers: {
          Authorization: `Bearer ${user.token}`,
        }
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ border: "5px solid #4CAF50", padding: "20px", margin: "10px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ borderBottom: "2px solid #4CAF50", color: "#333", marginBottom: "20px" }}>Categories</h1>
      {categories.map((category) => (
        <div key={category.id} style={{ margin: "20px 0", padding: "10px", border: "1px solid #4CAF50", borderRadius: "5px", boxShadow: "0 2px 5px rgba(0,0,0,0.15)" }}>
          <h2 style={{ color: "#333", marginBottom: "10px" }}>{category.name}</h2>
          <button style={{ backgroundColor: "#ddd", color: "#333", marginRight: "10px", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onClick={() => viewCategory(category.id)} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>View Category</button>
          <button style={{ backgroundColor: "#ddd", color: "#333", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onClick={() => changeVisibility(category.id)} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>Change Visibility</button>
        </div>
      ))}
      <input type="text" value={newCategoryName} onChange={e => setNewCategoryName(e.target.value)} placeholder="" style={{ margin: "20px 0", padding: "5px", width: "100%", border: "1px solid #ddd", borderRadius: "5px" }} />
      <button style={{ backgroundColor: "#ddd", color: "#333", cursor: "pointer", padding: "5px 10px", border: "none", borderRadius: "5px", transition: "background-color 0.3s ease" }} onClick={createCategory} onMouseOver={(e) => e.target.style.backgroundColor = "#bbb"} onMouseOut={(e) => e.target.style.backgroundColor = "#ddd"}>Create Category</button>
      <div style={{ textAlign: "right" }}>
        <Link to="/user-access" style={{ textDecoration: "none", color: "#4CAF50" }}>Manage User Access</Link>
      </div>
    </div>
  );
};

export default Categories;