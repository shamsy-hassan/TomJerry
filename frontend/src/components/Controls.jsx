import React, { useEffect, useRef } from 'react';

const isMobile = () => /Mobi|Android/i.test(navigator.userAgent);

const Controls = ({ onMove, onAction, onStart, onStop }) => {
  const touchRef = useRef();
  const lastDir = useRef({ x: 0, y: 0 });
  const lastAction = useRef(null);

  // Keyboard controls (desktop)
  useEffect(() => {
    if (isMobile()) return;
    const handleKey = e => {
      let dir = { x: 0, y: 0 };
      if (['ArrowUp', 'w'].includes(e.key)) dir.y = -1;
      if (['ArrowDown', 's'].includes(e.key)) dir.y = 1;
      if (['ArrowLeft', 'a'].includes(e.key)) dir.x = -1;
      if (['ArrowRight', 'd'].includes(e.key)) dir.x = 1;
      if (dir.x || dir.y) {
        lastDir.current = dir;
        onMove && onMove(dir);
      }
      if (e.key === ' ' || e.key === 'Spacebar') {
        lastAction.current = 'dash';
        onAction && onAction('dash');
      }
      if (e.key.toLowerCase() === 'p') {
        lastAction.current = 'pause';
        onAction && onAction('pause');
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [onMove, onAction]);

  // Virtual joystick (mobile)
  useEffect(() => {
    if (!isMobile()) return;
    const el = touchRef.current;
    if (!el) return;
    let startX, startY;
    const handleTouchStart = e => {
      const t = e.touches[0];
      startX = t.clientX;
      startY = t.clientY;
      onStart && onStart();
    };
    const handleTouchMove = e => {
      const t = e.touches[0];
      const dx = t.clientX - startX;
      const dy = t.clientY - startY;
      let dir = { x: 0, y: 0 };
      if (Math.abs(dx) > 20) dir.x = dx > 0 ? 1 : -1;
      if (Math.abs(dy) > 20) dir.y = dy > 0 ? 1 : -1;
      lastDir.current = dir;
      onMove && onMove(dir);
    };
    const handleTouchEnd = () => {
      onStop && onStop();
    };
    el.addEventListener('touchstart', handleTouchStart);
    el.addEventListener('touchmove', handleTouchMove);
    el.addEventListener('touchend', handleTouchEnd);
    return () => {
      el.removeEventListener('touchstart', handleTouchStart);
      el.removeEventListener('touchmove', handleTouchMove);
      el.removeEventListener('touchend', handleTouchEnd);
    };
  }, [onMove, onStart, onStop]);

  // Action buttons (mobile)
  return isMobile() ? (
    <div ref={touchRef} aria-label="Virtual Joystick" style={{
      position: 'fixed',
      bottom: 24,
      left: 24,
      width: 120,
      height: 120,
      background: '#222a',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100
    }}>
      <button aria-label="Dash" onClick={() => onAction && onAction('dash')} style={{
        position: 'absolute',
        right: -40,
        top: 40,
        fontSize: 22,
        borderRadius: 12,
        padding: '10px 18px',
        background: '#f90',
        color: '#fff',
        border: 'none',
        boxShadow: '0 1px 4px #0002',
        cursor: 'pointer'
      }}>Dash</button>
      <button aria-label="Pause" onClick={() => onAction && onAction('pause')} style={{
        position: 'absolute',
        left: -40,
        top: 40,
        fontSize: 22,
        borderRadius: 12,
        padding: '10px 18px',
        background: '#888',
        color: '#fff',
        border: 'none',
        boxShadow: '0 1px 4px #0002',
        cursor: 'pointer'
      }}>Pause</button>
    </div>
  ) : null;
};

export default Controls;
