import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

const Admin = () => {
  const [username, setUsername] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [accessType, setAccessType] = useState("");

  const giveReadAccess = async () => {
    const token = localStorage.getItem("token");
    try {
      await api.put(
        `/categories/${categoryId}/users/${username}/read-access`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
    } catch (error) {
      console.error(error);
    }
  };

  const giveWriteAccess = async () => {
    const token = localStorage.getItem("token");
    try {
      await api.put(
        `/categories/${categoryId}/users/${username}/write-access`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
    } catch (error) {
      console.error(error);
    }
  };

  const revokeAccess = async () => {
    const token = localStorage.getItem("token");
    try {
      await api.delete(`/categories/${categoryId}/users/${username}/access`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div
      style={{
        border: "5px solid #4CAF50",
        padding: "20px",
        margin: "10px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1
        style={{
          borderBottom: "2px solid #4CAF50",
          color: "#333",
          marginBottom: "20px",
        }}
      >
        User Access Management
      </h1>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="User ID"
        style={{
          margin: "10px 0",
          padding: "5px",
          width: "100%",
          border: "1px solid #ddd",
          borderRadius: "5px",
        }}
      />
      <input
        type="text"
        value={categoryId}
        onChange={(e) => setCategoryId(e.target.value)}
        placeholder="Category ID"
        style={{
          margin: "10px 0",
          padding: "5px",
          width: "100%",
          border: "1px solid #ddd",
          borderRadius: "5px",
        }}
      />
      <select
        value={accessType}
        onChange={(e) => setAccessType(e.target.value)}
        style={{
          margin: "10px 0",
          padding: "5px",
          width: "100%",
          border: "1px solid #ddd",
          borderRadius: "5px",
        }}
      >
        <option value="">Select Access Type</option>
        <option value="read">Read</option>
        <option value="write">Write</option>
      </select>
      <button
        style={{
          backgroundColor: "#ddd",
          color: "#333",
          marginRight: "10px",
          cursor: "pointer",
          padding: "5px 10px",
          border: "none",
          borderRadius: "5px",
          transition: "background-color 0.3s ease",
        }}
        onClick={giveReadAccess}
        onMouseOver={(e) => (e.target.style.backgroundColor = "#bbb")}
        onMouseOut={(e) => (e.target.style.backgroundColor = "#ddd")}
      >
        Give Read Access
      </button>
      <button
        style={{
          backgroundColor: "#ddd",
          color: "#333",
          marginRight: "10px",
          cursor: "pointer",
          padding: "5px 10px",
          border: "none",
          borderRadius: "5px",
          transition: "background-color 0.3s ease",
        }}
        onClick={giveWriteAccess}
        onMouseOver={(e) => (e.target.style.backgroundColor = "#bbb")}
        onMouseOut={(e) => (e.target.style.backgroundColor = "#ddd")}
      >
        Give Write Access
      </button>
      <button
        style={{
          backgroundColor: "#ddd",
          color: "#333",
          marginRight: "10px",
          cursor: "pointer",
          padding: "5px 10px",
          border: "none",
          borderRadius: "5px",
          transition: "background-color 0.3s ease",
        }}
        onClick={revokeAccess}
        onMouseOver={(e) => (e.target.style.backgroundColor = "#bbb")}
        onMouseOut={(e) => (e.target.style.backgroundColor = "#ddd")}
      >
        Revoke Access
      </button>
      <div style={{ textAlign: "right" }}>
        <Link
          to="/categories"
          style={{
            textDecoration: "none",
            color: "#4CAF50",
            fontWeight: "bold",
          }}
        >
          Back to Categories
        </Link>
      </div>
    </div>
  );
};

export default Admin;
