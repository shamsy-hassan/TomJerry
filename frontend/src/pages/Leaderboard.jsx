import React, { useEffect, useState } from 'react';
import api from '../utils/api';

const Leaderboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [offline, setOffline] = useState(false);

  const fetchLeaderboard = async () => {
    setLoading(true);
    try {
      const res = await api.getLeaderboard({ limit: 20 });
      setData(res || []);
      setOffline(false);
    } catch {
      setOffline(true);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  return (
    <div style={{ minHeight: '100vh', background: '#222', color: '#fff', padding: 32 }}>
      <h2 style={{ fontSize: 28, fontWeight: 700, marginBottom: 18 }}>Leaderboard</h2>
      <button onClick={fetchLeaderboard} style={{ fontSize: 16, borderRadius: 8, padding: '8px 18px', background: '#f90', color: '#fff', border: 'none', cursor: 'pointer', marginBottom: 18 }}>Refresh</button>
      {offline && <div style={{ color: '#f00', marginBottom: 12 }}>Offline or network error.</div>}
      <table style={{ width: '100%', background: '#333', borderRadius: 8, overflow: 'hidden' }}>
        <thead>
          <tr style={{ background: '#444' }}>
            <th style={{ padding: 8 }}>Player</th>
            <th style={{ padding: 8 }}>Time</th>
            <th style={{ padding: 8 }}>Catches</th>
            <th style={{ padding: 8 }}>Date</th>
          </tr>
        </thead>
        <tbody>
          {loading ? Array.from({ length: 8 }).map((_, i) => (
            <tr key={i}><td colSpan={4} style={{ padding: 8, background: '#222' }}>Loading...</td></tr>
          )) : data.map((row, i) => (
            <tr key={i} style={{ background: i % 2 ? '#222' : '#333' }}>
              <td style={{ padding: 8 }}>{row.player}</td>
              <td style={{ padding: 8 }}>{row.time}s</td>
              <td style={{ padding: 8 }}>{row.catches}</td>
              <td style={{ padding: 8 }}>{row.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
