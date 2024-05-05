import React, { useState } from "react";
import api from "./api";


const AuthForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

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
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", flexDirection: "column" }}>
      <form style={{ display: "flex", flexDirection: "column", width: "300px", gap: "10px" }}>
        <label style={{ textAlign: "center", fontWeight: "bold" }}>
          Username
          <input type="text" value={username} onChange={handleUsernameChange} style={{ padding: "10px", borderRadius: "5px", border: "1px solid #ccc", width: "100%" }} />
        </label>
        <label style={{ textAlign: "center", fontWeight: "bold" }}>
          Password
          <input type="password" value={password} onChange={handlePasswordChange} style={{ padding: "10px", borderRadius: "5px", border: "1px solid #ccc", width: "100%" }} />
        </label>
        <button type="button" onClick={handleLogin} style={{ padding: "10px", borderRadius: "5px", border: "none", backgroundColor: "#007BFF", color: "white", cursor: "pointer" }}>Login</button>
        <button type="button" onClick={handleRegister} style={{ padding: "10px", borderRadius: "5px", border: "none", backgroundColor: "#28A745", color: "white", cursor: "pointer" }}>Register</button>
      </form>
    </div>
  );
};

export default AuthForm;