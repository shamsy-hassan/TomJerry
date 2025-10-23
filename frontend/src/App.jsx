// Main React App entry point
import React, { useContext, useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Loader from './components/Loader';
import CharacterSelect from './components/CharacterSelect';
import GameCanvas from './components/GameCanvas';
import HUD from './components/HUD';
import ScoreBoard from './components/ScoreBoard';
import GameResult from './components/GameResult';
import Controls from './components/Controls';
import Home from './pages/Home';
import Game from './pages/Game';
import Leaderboard from './pages/Leaderboard';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import { GameContext } from './context/GameContext';
import { SoundContext } from './context/SoundContext';

const QuickControls = () => {
  const { isMuted, toggleMute } = useContext(SoundContext);
  const { restartGame } = useContext(GameContext);
  return (
    <div style={{ position: 'fixed', top: 12, right: 12, zIndex: 100, display: 'flex', gap: 10 }}>
      <button aria-label="Mute" onClick={toggleMute} style={{ fontSize: 18, borderRadius: 8, padding: '6px 14px' }}>{isMuted ? '🔇' : '🔊'}</button>
      <button aria-label="Restart" onClick={restartGame} style={{ fontSize: 18, borderRadius: 8, padding: '6px 14px' }}>⟳</button>
    </div>
  );
};

const AppShell = () => {
  const { loadingAssets, autoStart, gameState, setDevicePixelRatio } = useContext(GameContext);
  const [showLoader, setShowLoader] = useState(true);
  const navigate = useNavigate();

  // Keyboard shortcuts
  useEffect(() => {
    const handleKey = e => {
      if (e.key === 'Escape') {
        if (gameState === 'playing') navigate('/');
      }
      if (e.key.toLowerCase() === 'r') {
        if (gameState === 'ended') navigate('/game');
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [gameState, navigate]);

  // Device pixel ratio
  useEffect(() => {
    const updateDPR = () => setDevicePixelRatio(window.devicePixelRatio);
    window.addEventListener('resize', updateDPR);
    updateDPR();
    return () => window.removeEventListener('resize', updateDPR);
  }, [setDevicePixelRatio]);

  // Loader
  useEffect(() => {
    if (!loadingAssets) setShowLoader(false);
  }, [loadingAssets]);

  if (showLoader) return <Loader />;

  // Routing logic
  if (autoStart) return <Game />;
  return <Home />;
};

const App = () => (
  <Router>
    <QuickControls />
    <Routes>
      <Route path="/" element={<AppShell />} />
      <Route path="/game" element={<Game />} />
      <Route path="/leaderboard" element={<Leaderboard />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  </Router>
);

export default App;
