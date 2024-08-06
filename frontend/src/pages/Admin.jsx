import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import Header from "../components/Header";
import Footer from "../components/Footer";
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  MenuItem,
  Stack,
} from "@mui/material";
import ArrowBack from "@mui/icons-material/ArrowBack";

const Admin = () => {
  const [username, setUsername] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [accessType, setAccessType] = useState("");

  const giveAccess = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.put(
        `/categories/${categoryId}/users/${username}/${accessType}-access`,
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

  const revokeAccess = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.put(
        `/categories/${categoryId}/users/${username}/access/${accessType}`,
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
          Access Management
        </Typography>
        <TextField
          variant="outlined"
          margin="normal"
          fullWidth
          label="User ID"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          variant="outlined"
          margin="normal"
          fullWidth
          label="Category ID"
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
        />
        <TextField
          select
          variant="outlined"
          margin="normal"
          fullWidth
          label="Select Access Type"
          value={accessType}
          onChange={(e) => setAccessType(e.target.value)}
        >
          <MenuItem value="">Select Access Type</MenuItem>
          <MenuItem value="read">Read</MenuItem>
          <MenuItem value="write">Write</MenuItem>
        </TextField>
        <Box sx={{ display: "flex", justifyContent: "space-between" }}>
          <Stack direction="row" spacing={2}>
            <Button variant="outlined" color="primary" onClick={giveAccess}>
              Give Access
            </Button>
            <Button variant="outlined" color="secondary" onClick={revokeAccess}>
              Revoke Access
            </Button>
          </Stack>
        </Box>
        <Box sx={{ textAlign: "right", marginTop: 2 }}>
          <Link to="/categories" style={{ textDecoration: "none" }}>
            <ArrowBack sx={{ marginRight: 1 }} />
            Back to Categories
          </Link>
        </Box>
      </Container>
      <Footer />
    </>
  );
};

export default Admin;
