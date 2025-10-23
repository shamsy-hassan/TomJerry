import React, { useContext, useState } from 'react';
import { GameContext } from '../context/GameContext';

const ScoreBoard = () => {
  const { score, bestTime, player, gameState } = useContext(GameContext);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [shareImg, setShareImg] = useState(null);

  const handleShare = () => {
    // Compose a small image summary using canvas
    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 120;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#222';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 22px Inter';
    ctx.fillText(`Score: ${score}`, 20, 40);
    ctx.font = '16px Inter';
    ctx.fillText(`Best Time: ${bestTime}s`, 20, 70);
    ctx.fillText(`Catches: ${player?.catches || 0}`, 20, 100);
    setShareImg(canvas.toDataURL());
  };

  return (
    <div style={{ position: 'absolute', top: 16, left: 16, zIndex: 20, background: '#222a', borderRadius: 8, padding: '10px 18px', color: '#fff', fontSize: 16, boxShadow: '0 1px 8px #0003' }}>
      <div>Score: <span style={{ fontWeight: 700 }}>{score}</span></div>
      <div>Best Time: <span style={{ fontWeight: 700 }}>{bestTime}s</span></div>
      <div>Catches: <span style={{ fontWeight: 700 }}>{player?.catches || 0}</span></div>
      <button onClick={() => setShowLeaderboard(true)} style={{ marginTop: 8, fontSize: 15, borderRadius: 6, padding: '4px 12px', background: '#f90', color: '#fff', border: 'none', cursor: 'pointer' }}>Leaderboard</button>
      <button onClick={handleShare} style={{ marginLeft: 8, fontSize: 15, borderRadius: 6, padding: '4px 12px', background: '#888', color: '#fff', border: 'none', cursor: 'pointer' }}>Share Result</button>
      {shareImg && <img src={shareImg} alt="Share" style={{ marginTop: 8, width: 160, borderRadius: 6 }} />}
      {/* Leaderboard modal can be rendered here if showLeaderboard */}
    </div>
  );
};

export default ScoreBoard;
