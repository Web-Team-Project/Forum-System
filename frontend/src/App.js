import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import AuthForm from "./components/AuthForm";
import Categories from "./pages/Categories";
import CategoryTopics from "./pages/CategoryTopics";
import TopicReplies from "./pages/TopicReplies";
import ProtectedRoute from "./components/ProtectedRoute";
import Admin from "./pages/Admin";
import Messages from "./pages/Messages";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthForm />} />
        <Route
          path="/categories"
          element={
            <ProtectedRoute>
              <Categories />
            </ProtectedRoute>
          }
        />
        <Route
          path="/categories/:categoryId/topics"
          element={
            <ProtectedRoute>
              <CategoryTopics />
            </ProtectedRoute>
          }
        />
        <Route
          path="/topics/:topicId/replies"
          element={
            <ProtectedRoute>
              <TopicReplies />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <Admin />
            </ProtectedRoute>
          }
        />
        <Route
          path="/messages"
          element={
            <ProtectedRoute>
              <Messages />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
