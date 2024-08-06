import React from "react";
import { AppBar, Toolbar, Box, Typography } from "@mui/material";

const Footer = () => {
  return (
    <AppBar position="static" component="footer" sx={{ mt: "auto" }}>
      <Toolbar>
        <Box sx={{ flexGrow: 1 }} />
        <Typography variant="body1" sx={{ color: "inherit" }}>
          {" "}
          {/* Placeholder for the forum system name or other links. */}
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Footer;
