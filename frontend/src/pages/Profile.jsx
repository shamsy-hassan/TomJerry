import React, { useState } from 'react';

const Profile = () => {
  const [stats, setStats] = useState(() => {
    const s = localStorage.getItem('tj_stats');
    return s ? JSON.parse(s) : { wins: 0, losses: 0, bestTime: 0, history: [] };
  });

  const clearStats = () => {
    localStorage.removeItem('tj_stats');
    setStats({ wins: 0, losses: 0, bestTime: 0, history: [] });
  };

  return (
    <div style={{ minHeight: '100vh', background: '#222', color: '#fff', padding: 32 }}>
      <h2 style={{ fontSize: 28, fontWeight: 700, marginBottom: 18 }}>Profile (Guest)</h2>
      <div>Total Matches: {stats.wins + stats.losses}</div>
      <div>Best Time: {stats.bestTime}s</div>
      <div>Preferred Character: {localStorage.getItem('lastCharacter') || 'None'}</div>
      <div style={{ marginTop: 18 }}>
        <strong>Recent Games:</strong>
        <ol>
          {stats.history.map((m, i) => (
            <li key={i}>{m.result} as {m.character} ({m.difficulty}) — {m.time}s [{m.date}]</li>
          ))}
        </ol>
      </div>
      <button onClick={clearStats} style={{ marginTop: 18, fontSize: 16, borderRadius: 8, padding: '8px 18px', background: '#f90', color: '#fff', border: 'none', cursor: 'pointer' }}>Clear Local Stats</button>
    </div>
  );
};

export default Profile;
