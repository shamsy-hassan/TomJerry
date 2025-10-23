import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #222 60%, #3a2d1a 100%)' }}>
      <h1 style={{ color: '#fff', fontWeight: 700, fontSize: 40, marginBottom: 10, letterSpacing: 2 }}>Welcome to Tom & Jerry Chase!</h1>
      <div style={{ display: 'flex', alignItems: 'center', gap: 32, marginBottom: 18 }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ width: 80, height: 80, background: '#444', borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 6, boxShadow: '0 2px 8px #0005', fontSize: 40 }}>🐱</div>
          <div style={{ color: '#fff', fontWeight: 600 }}>Tom</div>
        </div>
        <span style={{ color: '#fff', fontSize: 28, fontWeight: 700 }}>VS</span>
        <div style={{ textAlign: 'center' }}>
          <div style={{ width: 80, height: 80, background: '#444', borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: 6, boxShadow: '0 2px 8px #0005', fontSize: 40 }}>🐭</div>
          <div style={{ color: '#fff', fontWeight: 600 }}>Jerry</div>
        </div>
      </div>
      <button onClick={() => navigate('/game')} style={{ fontSize: 24, borderRadius: 14, padding: '18px 44px', background: '#f90', color: '#fff', fontWeight: 700, border: 'none', boxShadow: '0 2px 12px #0004', cursor: 'pointer', marginBottom: 18, letterSpacing: 1 }}>Start Chase</button>
      <div style={{ color: '#eee', fontSize: 18, marginBottom: 18, maxWidth: 420, textAlign: 'center', lineHeight: 1.5 }}>
        Choose your character, jump into a lively cartoon world, and chase or escape! <br />
        <span style={{ color: '#ffd700' }}>Tip:</span> Use arrow keys or touch controls. Powerups and traps await!
      </div>
      <div style={{ display: 'flex', gap: 18 }}>
        <button onClick={() => navigate('/leaderboard')} style={{ fontSize: 16, borderRadius: 8, padding: '8px 18px', background: '#888', color: '#fff', border: 'none', cursor: 'pointer' }}>Leaderboard</button>
        <button onClick={() => navigate('/settings')} style={{ fontSize: 16, borderRadius: 8, padding: '8px 18px', background: '#888', color: '#fff', border: 'none', cursor: 'pointer' }}>Settings</button>
      </div>
      <div style={{ color: '#aaa', fontSize: 14, marginTop: 28, textAlign: 'center' }}>
        No login needed. Play solo or multiplayer. Offline support included!
      </div>
    </div>
  );
};

export default Home;
