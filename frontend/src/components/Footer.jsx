import React from "react";
import { Container, Box, Typography } from "@mui/material";

const Footer = () => {
  return (
    <Box sx={{ bgcolor: "primary.main", color: "white", mt: 5, py: 3 }}>
      <Container maxWidth="md">
        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Typography variant="body1">
            Forum System {/* Placeholder for the forum system name or other links. */}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
