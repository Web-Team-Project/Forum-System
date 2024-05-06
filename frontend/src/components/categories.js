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
    <div style={{ border: "5px solid green", padding: "20px", margin: "10px" }}>
      <h1 style={{ borderBottom: "2px solid green", color: "black", marginBottom: "20px" }}>Categories</h1>
      {categories.map((category) => (
        <div key={category.id} style={{ margin: "20px 0", padding: "10px", border: "1px solid green", borderRadius: "5px" }}>
          <h2 style={{ color: "black", marginBottom: "10px" }}>{category.name}</h2>
          <button style={{ backgroundColor: "grey", color: "white", marginRight: "10px", cursor: "pointer", padding: "5px 10px" }} onClick={() => viewCategory(category.id)} onMouseOver={(e) => e.target.style.backgroundColor = "darkgrey"} onMouseOut={(e) => e.target.style.backgroundColor = "grey"}>View Category</button>
          <button style={{ backgroundColor: "grey", color: "white", cursor: "pointer", padding: "5px 10px" }} onClick={() => changeVisibility(category.id)} onMouseOver={(e) => e.target.style.backgroundColor = "darkgrey"} onMouseOut={(e) => e.target.style.backgroundColor = "grey"}>Change Visibility</button>
        </div>
      ))}
      <input type="text" value={newCategoryName} onChange={e => setNewCategoryName(e.target.value)} placeholder="" style={{ margin: "20px 0", padding: "5px", width: "100%" }} />
      <button style={{ backgroundColor: "grey", color: "white", cursor: "pointer", padding: "5px 10px" }} onClick={createCategory} onMouseOver={(e) => e.target.style.backgroundColor = "darkgrey"} onMouseOut={(e) => e.target.style.backgroundColor = "grey"}>Create Category</button>
    </div>
  );
};

export default Categories;