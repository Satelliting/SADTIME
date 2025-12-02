import { useState, useEffect } from "react";
import api from "../api/client";

function Dashboard({ user, onLogout }) {
  const [summary, setSummary] = useState(null);

  const fetchSummary = async () => {
    try {
      const res = await api.get("/analytics/summary/");
      setSummary(res.data);
    } catch (err) {
      console.error("Failed to fetch summary:", err);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  return (
    <div className="dashboard">
      <header>
        <h1>SADTIME Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user.username}</span>
          <button onClick={onLogout}>Logout</button>
        </div>
      </header>

      <main>
        {summary ? (
          <div className="stats">
            <div className="stat-card">
              <h3>Total Events</h3>
              <p>{summary.total_events}</p>
            </div>
            <div className="stat-card">
              <h3>Last 24h</h3>
              <p>{summary.events_last_24h}</p>
            </div>
            <div className="stat-card">
              <h3>Last 7 Days</h3>
              <p>{summary.events_last_7d}</p>
            </div>
            <div className="stat-card">
              <h3>Indicators</h3>
              <p>{summary.total_indicators}</p>
            </div>
            <div className="stat-card">
              <h3>Techniques Used</h3>
              <p>{summary.total_techniques_used}</p>
            </div>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </main>
    </div>
  );
}

export default Dashboard;
