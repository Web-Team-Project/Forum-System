import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import {
  Container,
  Typography,
  Card,
  CardContent,
  Button,
} from "@mui/material";
import Header from "../components/Header";
import Footer from "../components/Footer";

const CategoryTopics = () => {
  const { categoryId } = useParams();
  const [topics, setTopics] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTopics = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(`/topics/category/${categoryId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTopics(response.data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchTopics();
  }, [categoryId]);

  const viewTopic = (topicId) => {
    navigate(`/topics/${topicId}/replies`);
  };

  return (
    <>
      <Header />
      <Container component="main" maxWidth="md" sx={{ padding: "20px" }}>
        <Typography component="h1" variant="h5">
          Topics in Category {categoryId}
        </Typography>
        {topics.map((topic) => (
          <Card key={topic.id} sx={{ margin: "20px 0" }}>
            <CardContent>
              <Typography variant="h6">{topic.title}</Typography>
              <Button variant="contained" onClick={() => viewTopic(topic.id)}>
                View Topic
              </Button>
            </CardContent>
          </Card>
        ))}
      </Container>
      <Footer />
    </>
  );
};

export default CategoryTopics;