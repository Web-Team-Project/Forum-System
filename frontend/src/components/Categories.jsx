import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import UserContext from "../utils/context";
import { TextField, Button, Container, Typography, Box, Card, CardContent } from "@mui/material";


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

  const lockCategory = async (categoryId) => {
    try {
      const response = await api.put(`/categories/lock/${categoryId}`, {}, {
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
    <Container component="main" maxWidth="md" sx={{ padding: '20px' }}>
      <Typography component="h1" variant="h5">
        Categories
      </Typography>
      {categories.map((category) => (
        <Card key={category.id} sx={{ margin: "20px 0" }}>
          <CardContent>
            <Typography variant="h6">
              {category.name}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
              <Link component={Link} to={`/categories/${category.id}`} underline="none">
                <Button variant="contained" onClick={() => viewCategory(category.id)}>
                  View Category
                </Button>
              </Link>
              <Button variant="contained" onClick={() => changeVisibility(category.id)}>
                Change Visibility
              </Button>
              <Button variant="contained" onClick={() => lockCategory(category.id)}>
                Lock Category
              </Button>
            </Box>
          </CardContent>
        </Card>
      ))}
      <TextField
        variant="outlined"
        margin="normal"
        required
        fullWidth
        id="newCategoryName"
        label="New Category Name"
        name="newCategoryName"
        autoComplete="newCategoryName"
        autoFocus
        value={newCategoryName}
        onChange={e => setNewCategoryName(e.target.value)}
      />
      <Button
        type="button"
        fullWidth
        variant="contained"
        color="primary"
        onClick={createCategory}
      >
        Create Category
      </Button>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
        <Link component={Link} to="/user-access" underline="none">
          <Button variant="contained">
            Manage User Access
          </Button>
        </Link>
        <Link component={Link} to="/messages" underline="none">
          <Button variant="contained">
            Go to Messages
          </Button>
        </Link>
      </Box>
    </Container>
  );
};

export default Categories;
