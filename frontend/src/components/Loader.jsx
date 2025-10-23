import React, { useState, useEffect, useRef } from 'react';

const tips = [
  'Use arrow keys or WASD to move.',
  'Space to dash, P to pause.',
  'Catch Jerry or escape Tom!',
  'Mobile: use joystick and buttons.',
  'Replay instantly after each round.'
];

export function preloadAssets(assetList) {
  return new Promise(resolve => {
    let loaded = 0;
    let failed = 0;
    assetList.forEach(src => {
      const isImg = src.endsWith('.png') || src.endsWith('.webp');
      const el = isImg ? new window.Image() : new window.Audio();
      el.src = src;
      el.onload = el.oncanplaythrough = () => {
        loaded++;
        if (loaded + failed === assetList.length) resolve({ loaded, failed });
      };
      el.onerror = () => {
        failed++;
        if (loaded + failed === assetList.length) resolve({ loaded, failed });
      };
    });
  });
}

const Loader = ({ assetList = [], onStart }) => {
  const [progress, setProgress] = useState(0);
  const [loaded, setLoaded] = useState(0);
  const [failed, setFailed] = useState(0);
  const [tipIdx, setTipIdx] = useState(0);
  const [ready, setReady] = useState(false);
  const startBtnRef = useRef();

  useEffect(() => {
    let running = true;
    preloadAssets(assetList).then(({ loaded, failed }) => {
      if (!running) return;
      setLoaded(loaded);
      setFailed(failed);
      setProgress(Math.round((loaded / assetList.length) * 100));
      setReady(true);
    });
    return () => { running = false; };
  }, [assetList]);

  useEffect(() => {
    const interval = setInterval(() => setTipIdx(i => (i + 1) % tips.length), 3500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (ready && startBtnRef.current) startBtnRef.current.focus();
  }, [ready]);

  return (
    <div role="dialog" aria-modal="true" tabIndex={-1} style={{
      position: 'fixed',
      inset: 0,
      background: 'linear-gradient(135deg, #222 60%, #444)',
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
        outline: 'none'
      }}>
        <div style={{ fontSize: 32, fontWeight: 'bold', color: '#222', marginBottom: 12 }}>
          Loading Game...
        </div>
        <div style={{ width: 180, margin: '16px auto' }}>
          <div style={{ height: 18, background: '#eee', borderRadius: 9, overflow: 'hidden' }}>
            <div style={{ width: `${progress}%`, height: 18, background: '#f90', transition: 'width 0.4s', borderRadius: 9 }} />
          </div>
          <div style={{ fontSize: 14, color: '#444', marginTop: 6 }}>
            {loaded + failed}/{assetList.length} assets loaded
          </div>
        </div>
        <div style={{ fontSize: 15, color: '#666', margin: '12px 0' }}>
          Tip: {tips[tipIdx]}
        </div>
        <button
          ref={startBtnRef}
          onClick={onStart}
          disabled={!ready}
          style={{
            marginTop: 18,
            fontSize: 18,
            borderRadius: 8,
            padding: '8px 22px',
            background: ready ? '#f90' : '#ccc',
            color: '#fff',
            fontWeight: 600,
            border: 'none',
            boxShadow: '0 1px 4px #0002',
            cursor: ready ? 'pointer' : 'not-allowed',
            transition: 'background 0.2s'
          }}
        >
          {ready ? 'Start' : 'Loading...'}
        </button>
        {failed > 0 && (
          <button
            onClick={onStart}
            style={{
              marginTop: 8,
              fontSize: 15,
              borderRadius: 8,
              padding: '6px 18px',
              background: '#888',
              color: '#fff',
              fontWeight: 500,
              border: 'none',
              boxShadow: '0 1px 4px #0002',
              cursor: 'pointer'
            }}
          >
            Continue in low quality
          </button>
        )}
      </div>
    </div>
  );
};

export default Loader;
