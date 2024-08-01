import React from "react";
import { AppBar, Toolbar, Box } from "@mui/material";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <AppBar position="sticky">
      <Toolbar>
        <Box sx={{ flexGrow: 1 }} />
        <Link to="/admin" style={{ color: "inherit", textDecoration: "inherit" }}>
          {" "}
          {/* Link to the admin panel.  Add more links as well. */}
          <h6>Admin Panel</h6>
        </Link>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
