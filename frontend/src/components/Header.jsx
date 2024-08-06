import React from "react";
import { AppBar, Toolbar, Box, IconButton } from "@mui/material";
import { Link } from "react-router-dom";
import { useTheme } from "@mui/material/styles";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { ColorModeContext } from "./ToggleColorMode";
import logo from "../logo.png";

const Header = () => {
  const theme = useTheme();
  const colorMode = React.useContext(ColorModeContext);

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Box
          component="img"
          src={logo}
          alt="Logo"
          sx={{ height: 60, width: 80, marginRight: 2 }}
        />
        <Box sx={{ flexGrow: 1 }} />
        <Link
          to="/messages"
          style={{
            color: "inherit",
            textDecoration: "inherit",
            marginRight: 20,
          }}
        >
          <h6>Messages</h6>
        </Link>
        <Link
          to="/admin"
          style={{ color: "inherit", textDecoration: "inherit" }}
        >
          <h6>Admin Panel</h6>
        </Link>
        <IconButton
          sx={{ ml: 1 }}
          onClick={colorMode.toggleColorMode}
          color="inherit"
        >
          {theme.palette.mode === "dark" ? (
            <Brightness7Icon />
          ) : (
            <Brightness4Icon />
          )}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
