import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import {
  TextField,
  Button,
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Stack,
  Modal,
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [privilegedUsers, setPrivilegedUsers] = useState([]);
  const [open, setOpen] = useState(false);
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
      setCategories((prevCategories) =>
        prevCategories.map((category) =>
          category.id === categoryId
            ? { ...category, private: !category.private }
            : category
        )
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
      setCategories((prevCategories) =>
        prevCategories.map((category) =>
          category.id === categoryId ? { ...category, locked: true } : category
        )
      );
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const viewPrivilegedUsers = async (categoryId) => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.get(
        `/categories/privileged-users/${categoryId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      console.log(response.data);
      setPrivilegedUsers(response.data.privileged_users || []);
    } catch (error) {
      console.error(error);
    }
  };

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

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
              <Typography variant="h6">
                {category.name}
                {category.private && (
                  <Typography variant="body2" color="primary" component="span">
                    {" "}
                    (Private)
                  </Typography>
                )}
              </Typography>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginTop: "10px",
                }}
              >
                <Stack direction="row" spacing={2}>
                  <Button
                    variant="outlined"
                    onClick={() => viewCategory(category.id)}
                  >
                    View Category
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={() => changeVisibility(category.id)}
                  >
                    Change Visibility
                  </Button>
                  <Button
                    variant="outlined"
                    color="secondary"
                    onClick={() => lockCategory(category.id)}
                    disabled={category.locked}
                  >
                    {category.locked ? "Locked" : "Lock Category"}
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={() => {
                      viewPrivilegedUsers(category.id);
                      handleOpen();
                    }}
                  >
                    View Privileged Users
                  </Button>
                </Stack>
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

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <Box sx={{ ...modalStyle }}>
          <Typography id="modal-title" variant="h6" component="h2">
            Privileged Users
          </Typography>
          <Box id="modal-description" sx={{ mt: 2 }}>
            {Array.isArray(privilegedUsers) && privilegedUsers.length > 0 ? (
              privilegedUsers.map((user) => (
                <div key={user.id}>
                  {user.username} - Read Access:{" "}
                  {user.access_level.read_access ? "Yes" : "No"}, Write Access:{" "}
                  {user.access_level.write_access ? "Yes" : "No"}
                </div>
              ))
            ) : (
              <div>No privileged users found.</div>
            )}
          </Box>
        </Box>
      </Modal>
    </>
  );
};

const modalStyle = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default Categories;
