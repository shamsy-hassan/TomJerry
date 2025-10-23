import { useRef, useEffect } from 'react';

export default function useControls({ sensitivity = 1, onMove, onAction }) {
  const directionRef = useRef({ x: 0, y: 0 });
  const isDashingRef = useRef(false);

  useEffect(() => {
    const handleKey = e => {
      let dir = { x: 0, y: 0 };
      if (['ArrowUp', 'w'].includes(e.key)) dir.y = -1;
      if (['ArrowDown', 's'].includes(e.key)) dir.y = 1;
      if (['ArrowLeft', 'a'].includes(e.key)) dir.x = -1;
      if (['ArrowRight', 'd'].includes(e.key)) dir.x = 1;
      if (dir.x || dir.y) {
        directionRef.current = { x: dir.x * sensitivity, y: dir.y * sensitivity };
        onMove && onMove(directionRef.current);
      }
      if (e.key === ' ' || e.key === 'Spacebar') {
        isDashingRef.current = true;
        onAction && onAction('dash');
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [sensitivity, onMove, onAction]);

  // Touch/virtual joystick
  function bindTouch(el) {
    let startX, startY;
    el.addEventListener('touchstart', e => {
      const t = e.touches[0];
      startX = t.clientX;
      startY = t.clientY;
    });
    el.addEventListener('touchmove', e => {
      const t = e.touches[0];
      const dx = t.clientX - startX;
      const dy = t.clientY - startY;
      let dir = { x: 0, y: 0 };
      if (Math.abs(dx) > 20) dir.x = dx > 0 ? 1 : -1;
      if (Math.abs(dy) > 20) dir.y = dy > 0 ? 1 : -1;
      directionRef.current = { x: dir.x * sensitivity, y: dir.y * sensitivity };
      onMove && onMove(directionRef.current);
    });
    el.addEventListener('touchend', () => {
      directionRef.current = { x: 0, y: 0 };
      onMove && onMove(directionRef.current);
    });
  }

  return { directionRef, isDashingRef, bindTouch };
}
