import React, { useState, useContext } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import UserContext from "../utils/context";
import { TextField, Button, Container, Typography, Box } from "@mui/material";

const AuthForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext);

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post("/auth/token", {
        username: username,
        password: password,
      }, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        transformRequest: [(data) => {
          let payload = "";
          Object.keys(data).forEach(k => payload += `${encodeURIComponent(k)}=${encodeURIComponent(data[k])}&`);
          return payload;
        }]
      });
      console.log(response.data);
      const newUser = { username: username, userId: response.data.userId, token: response.data.access_token, role: response.data.role};
      setUser(newUser);
      localStorage.setItem("user", JSON.stringify(newUser));
      navigate("/categories");
    } catch (error) {
      console.error(error);
    }
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post("/auth/", {
        username: username,
        password: password,
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
    >
      <Container component="main" maxWidth="xs">
        <form noValidate>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            autoComplete="username"
            autoFocus
            value={username}
            onChange={handleUsernameChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={handlePasswordChange}
          />
          <Button
            type="button"
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleLogin}
          >
            Sign In
          </Button>
          <Button
            type="button"
            fullWidth
            variant="contained"
            color="secondary"
            onClick={handleRegister}
          >
            Sign Up
          </Button>
        </form>
      </Container>
    </Box>
  );
};

export default AuthForm;
