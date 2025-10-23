import React, { useContext, useEffect } from 'react';
import { GameContext } from '../context/GameContext';
import { SoundContext } from '../context/SoundContext';

const GameResult = ({ result, onReplay, onChangeCharacter, onMainMenu }) => {
  const { selectedCharacter } = useContext(GameContext);
  const { playOneShot } = useContext(SoundContext);

  useEffect(() => {
    if (result === 'win') playOneShot('/assets/audio/win-sound.mp3');
    if (result === 'lose') playOneShot('/assets/audio/lose-sound.mp3');
    const handleKey = e => {
      if (e.key.toLowerCase() === 'r') onReplay && onReplay();
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [result, onReplay, playOneShot]);

  return (
    <div role="dialog" aria-modal="true" tabIndex={-1} style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: '#fff',
        padding: 32,
        borderRadius: 16,
        boxShadow: '0 2px 16px #0006',
        textAlign: 'center',
        minWidth: 220,
        outline: 'none',
        animation: result === 'win' ? 'bounce 1s' : 'shake 1s'
      }}>
        <img src={`/assets/sprites/${selectedCharacter?.toLowerCase()}-${result === 'win' ? 'run' : 'idle'}.png`} alt={result} style={{ width: 80, height: 80, marginBottom: 8 }} />
        <h2 style={{ color: '#222', fontWeight: 700, fontSize: 28, marginBottom: 12 }}>{result === 'win' ? 'Victory!' : 'Defeat!'}</h2>
        <div style={{ fontSize: 16, color: '#444', marginBottom: 18 }}>Stats summary here...</div>
        <button onClick={onReplay} style={{ fontSize: 18, borderRadius: 8, padding: '8px 22px', background: '#f90', color: '#fff', fontWeight: 600, border: 'none', boxShadow: '0 1px 4px #0002', cursor: 'pointer', marginRight: 8 }}>Replay</button>
        <button onClick={onChangeCharacter} style={{ fontSize: 18, borderRadius: 8, padding: '8px 22px', background: '#888', color: '#fff', fontWeight: 600, border: 'none', boxShadow: '0 1px 4px #0002', cursor: 'pointer', marginRight: 8 }}>Change Character</button>
        <button onClick={onMainMenu} style={{ fontSize: 18, borderRadius: 8, padding: '8px 22px', background: '#222', color: '#fff', fontWeight: 600, border: 'none', boxShadow: '0 1px 4px #0002', cursor: 'pointer' }}>Main Menu</button>
      </div>
      <style>{`
        @keyframes bounce { 0%{transform:scale(1);} 50%{transform:scale(1.2);} 100%{transform:scale(1);} }
        @keyframes shake { 0%,100%{transform:translateX(0);} 20%,60%{transform:translateX(-10px);} 40%,80%{transform:translateX(10px);} }
      `}</style>
    </div>
  );
};

export default GameResult;
