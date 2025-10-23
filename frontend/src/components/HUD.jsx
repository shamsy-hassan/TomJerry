import React, { useContext } from 'react';
import { GameContext } from '../context/GameContext';

const HUD = () => {
  const { timeLeft, player, opponent, gameState } = useContext(GameContext);
  const distance = player && opponent ? Math.sqrt((player.x - opponent.x) ** 2 + (player.y - opponent.y) ** 2) : 0;

  return (
    <div aria-label="Game HUD" style={{
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      pointerEvents: 'none'
    }}>
      <div style={{ fontSize: 32, fontWeight: 'bold', color: '#fff', textShadow: '0 0 8px #000', marginTop: 12 }}>
        {timeLeft}s
      </div>
      <div style={{ width: 180, height: 18, background: '#222', borderRadius: 9, margin: '12px 0', overflow: 'hidden' }}>
        <div style={{ width: `${Math.max(0, Math.min(100, (timeLeft / 30) * 100))}%`, height: 18, background: '#f90', borderRadius: 9, transition: 'width 0.4s' }} />
      </div>
      <div style={{ fontSize: 15, color: '#fff', marginBottom: 8 }}>
        Distance: {distance.toFixed(1)}m
      </div>
      {/* Powerup icons and pause menu toggle can be added here */}
      {gameState === 'paused' && (
        <div style={{ fontSize: 18, color: '#fff', background: '#222a', borderRadius: 8, padding: '8px 22px', marginTop: 12 }}>Paused</div>
      )}
    </div>
  );
};

export default HUD;
