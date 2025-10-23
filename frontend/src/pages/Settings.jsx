import React, { useState } from 'react';

const Settings = () => {
  const [musicVolume, setMusicVolume] = useState(() => Number(localStorage.getItem('musicVolume') || 0.3));
  const [effectsVolume, setEffectsVolume] = useState(() => Number(localStorage.getItem('effectsVolume') || 0.5));
  const [graphicsQuality, setGraphicsQuality] = useState(() => localStorage.getItem('graphicsQuality') || 'High');
  const [controlSensitivity, setControlSensitivity] = useState(() => Number(localStorage.getItem('controlSensitivity') || 1));
  const [showFPS, setShowFPS] = useState(() => localStorage.getItem('showFPS') === 'true');

  const persist = (key, value) => localStorage.setItem(key, value);

  return (
    <div style={{ minHeight: '100vh', background: '#222', color: '#fff', padding: 32 }}>
      <h2 style={{ fontSize: 28, fontWeight: 700, marginBottom: 18 }}>Settings</h2>
      <div style={{ marginBottom: 18 }}>
        <label>Music Volume: </label>
        <input type="range" min={0} max={1} step={0.01} value={musicVolume} onChange={e => { setMusicVolume(e.target.value); persist('musicVolume', e.target.value); }} />
        <span>{Math.round(musicVolume * 100)}%</span>
      </div>
      <div style={{ marginBottom: 18 }}>
        <label>Effects Volume: </label>
        <input type="range" min={0} max={1} step={0.01} value={effectsVolume} onChange={e => { setEffectsVolume(e.target.value); persist('effectsVolume', e.target.value); }} />
        <span>{Math.round(effectsVolume * 100)}%</span>
      </div>
      <div style={{ marginBottom: 18 }}>
        <label>Graphics Quality: </label>
        <select value={graphicsQuality} onChange={e => { setGraphicsQuality(e.target.value); persist('graphicsQuality', e.target.value); }}>
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>
      </div>
      <div style={{ marginBottom: 18 }}>
        <label>Control Sensitivity: </label>
        <input type="range" min={0.5} max={2} step={0.01} value={controlSensitivity} onChange={e => { setControlSensitivity(e.target.value); persist('controlSensitivity', e.target.value); }} />
        <span>{controlSensitivity}</span>
      </div>
      <div style={{ marginBottom: 18 }}>
        <label>Show FPS: </label>
        <input type="checkbox" checked={showFPS} onChange={e => { setShowFPS(e.target.checked); persist('showFPS', e.target.checked); }} />
      </div>
      <button onClick={() => { localStorage.clear(); window.location.reload(); }} style={{ marginTop: 18, fontSize: 16, borderRadius: 8, padding: '8px 18px', background: '#f90', color: '#fff', border: 'none', cursor: 'pointer' }}>Clear Local Data</button>
    </div>
  );
};

export default Settings;
