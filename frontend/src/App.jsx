import { useState, useEffect } from "react";
import api from "./api/client";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const res = await api.get("/auth/me/");
      if (res.data.authenticated) {
        setUser(res.data.user);
      }
    } catch (err) {
      console.error("Auth check failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (username, password) => {
    try {
      const res = await api.post("/auth/login/", { username, password });
      setUser(res.data.user);
      return { success: true };
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.error || "Login failed",
      };
    }
  };

  const handleLogout = async () => {
    await api.post("/auth/logout/");
    setUser(null);
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="app">
      {user ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
