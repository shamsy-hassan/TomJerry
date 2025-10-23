// Tom/Jerry select screen
import React, { useState, useEffect, useRef, useContext } from 'react';
import { GameContext } from '../context/GameContext';

const abilities = {
  Tom: ['Strong', 'Slower'],
  Jerry: ['Fast', 'Nimble']
};
const tooltips = {
  Tom: 'Special: Dash, Trap Set',
  Jerry: 'Special: Hide, Dash'
};

const CharacterSelect = () => {
  const { setSelectedCharacter, startGame } = useContext(GameContext);
  const [selected, setSelected] = useState(localStorage.getItem('lastCharacter') || null);
  const [difficulty, setDifficulty] = useState('normal');
  const [hovered, setHovered] = useState(null);
  const cardRefs = { Tom: useRef(), Jerry: useRef() };

  useEffect(() => {
    if (selected) localStorage.setItem('lastCharacter', selected);
  }, [selected]);

  // Keyboard selection
  useEffect(() => {
    const handleKey = e => {
      if (e.key === 'ArrowLeft' || e.key === 'a') setSelected('Tom');
      if (e.key === 'ArrowRight' || e.key === 'd') setSelected('Jerry');
      if (e.key === 'Enter' && selected) handleStart();
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [selected]);

  const handleStart = () => {
    setSelectedCharacter(selected);
    startGame({ difficulty });
  };

  return (
    <div style={{
      background: 'linear-gradient(135deg, #fff 80%, #f9f9f9)',
      borderRadius: 16,
      boxShadow: '0 2px 16px #0004',
      padding: 32,
      minWidth: 260,
      textAlign: 'center',
      fontFamily: 'Inter, Arial, sans-serif'
    }}>
      <h2 style={{ color: '#222', fontWeight: 700, fontSize: 28, marginBottom: 18 }}>Choose Your Character</h2>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 32 }}>
        {['Tom', 'Jerry'].map(char => (
          <div
            key={char}
            ref={cardRefs[char]}
            tabIndex={0}
            aria-label={char}
            onClick={() => setSelected(char)}
            onMouseEnter={() => setHovered(char)}
            onMouseLeave={() => setHovered(null)}
            style={{
              background: selected === char ? '#f90' : '#fff',
              border: selected === char ? '2px solid #f90' : '2px solid #eee',
              borderRadius: 12,
              boxShadow: '0 2px 8px #0002',
              padding: 18,
              width: 120,
              cursor: 'pointer',
              outline: selected === char ? '2px solid #f90' : 'none',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              position: 'relative'
            }}
          >
            <img src={`/assets/icons/${char.toLowerCase()}-icon.png`} alt={char} style={{ width: 80, height: 80, marginBottom: 8, filter: 'drop-shadow(0 2px 8px #0002)' }} />
            <div style={{ fontWeight: 600, fontSize: 18 }}>{char}</div>
            <div style={{ fontSize: 13, color: '#666', margin: '6px 0' }}>{abilities[char].join(', ')}</div>
            <div style={{ marginTop: 8 }}>
              <label style={{ fontSize: 13, color: '#444' }}>AI Difficulty:</label>
              <select value={difficulty} onChange={e => setDifficulty(e.target.value)} style={{ marginLeft: 6, borderRadius: 6, padding: '2px 8px' }}>
                <option value="easy">Easy</option>
                <option value="normal">Normal</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            {hovered === char && (
              <div style={{
                position: 'absolute',
                bottom: -32,
                left: '50%',
                transform: 'translateX(-50%)',
                background: '#222',
                color: '#fff',
                padding: '6px 14px',
                borderRadius: 8,
                fontSize: 13,
                boxShadow: '0 2px 8px #0003',
                zIndex: 10
              }}>{tooltips[char]}</div>
            )}
          </div>
        ))}
      </div>
      <button
        onClick={handleStart}
        disabled={!selected}
        style={{
          marginTop: 22,
          fontSize: 18,
          borderRadius: 8,
          padding: '8px 22px',
          background: selected ? '#f90' : '#ccc',
          color: '#fff',
          fontWeight: 600,
          border: 'none',
          boxShadow: '0 1px 4px #0002',
          cursor: selected ? 'pointer' : 'not-allowed',
          transition: 'background 0.2s'
        }}
      >
        Start Game
      </button>
    </div>
  );
};

export default CharacterSelect;
