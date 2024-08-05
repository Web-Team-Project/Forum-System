import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";
import {
  TextField,
  Button,
  Container,
  Typography,
  Box,
  Card,
  CardContent,
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [newCategoryName, setNewCategoryName] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const viewCategories = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get("/categories/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setCategories(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    viewCategories();
  }, []);

  const createCategory = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.post(
        "/categories/",
        { name: newCategoryName },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(response.data);
      setCategories([...categories, response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  const viewCategory = (categoryId) => {
    navigate(`/categories/${categoryId}/topics`);
  };

  const changeVisibility = async (categoryId) => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.put(
        `/categories/${categoryId}/visibility`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const lockCategory = async (categoryId) => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.put(
        `/categories/lock/${categoryId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Header />
      <Container component="main" maxWidth="md" sx={{ padding: "20px" }}>
        <Typography component="h1" variant="h5">
          Categories
        </Typography>
        {categories.map((category) => (
          <Card key={category.id} sx={{ margin: "20px 0" }}>
            <CardContent>
              <Typography variant="h6">{category.name}</Typography>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "10px",
                }}
              >
                <Button
                  variant="contained"
                  onClick={() => viewCategory(category.id)}
                >
                  View Category
                </Button>
                <Button
                  variant="contained"
                  onClick={() => changeVisibility(category.id)}
                >
                  Change Visibility
                </Button>
                <Button
                  variant="contained"
                  onClick={() => lockCategory(category.id)}
                >
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
          onChange={(e) => setNewCategoryName(e.target.value)}
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
      </Container>
      <Footer />
    </>
  );
};

export default Categories;
