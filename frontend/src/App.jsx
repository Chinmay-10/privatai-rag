import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Query from "./pages/Query";
import Documents from "./pages/Documents";
import Audit from "./pages/Audit";

import { isAuthenticated } from "./auth";

function Protected({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route path="/" element={<Protected><Dashboard /></Protected>} />
        <Route path="/upload" element={<Protected><Upload /></Protected>} />
        <Route path="/query" element={<Protected><Query /></Protected>} />
        <Route path="/documents" element={<Protected><Documents /></Protected>} />

        <Route path="/audit" element={<Protected><Audit /></Protected>} />

      </Routes>
    </BrowserRouter>
  );
}
