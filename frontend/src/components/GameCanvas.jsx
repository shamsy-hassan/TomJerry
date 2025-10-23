import React, { useRef, useEffect, useContext } from 'react';
import { GameContext } from '../context/GameContext';
import { SoundContext } from '../context/SoundContext';

const SPRITE_SIZE = 64;
const TICK_RATE = 60;

const GameCanvas = ({ map, playerState, opponentState, interactables, onCollision, onTrapTriggered, onCatch }) => {
  const canvasRef = useRef();
  const animationFrame = useRef();
  const { devicePixelRatio } = useContext(GameContext);
  const { playOneShot } = useContext(SoundContext);

  // Main game loop
  useEffect(() => {
    let running = true;
    let lastTime = performance.now();
    const loop = (now) => {
      if (!running) return;
      const dt = (now - lastTime) / 1000;
      lastTime = now;
      renderFrame();
      animationFrame.current = requestAnimationFrame(loop);
    };
    animationFrame.current = requestAnimationFrame(loop);
    return () => {
      running = false;
      cancelAnimationFrame(animationFrame.current);
    };
  }, [map, playerState, opponentState, interactables, devicePixelRatio]);

  // Render tick
  const renderFrame = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = devicePixelRatio || window.devicePixelRatio || 1;
    canvas.width = 400 * dpr;
    canvas.height = 300 * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, 400, 300);
    // Draw background
    if (map?.background) {
      const bg = new window.Image();
      bg.src = map.background;
      ctx.drawImage(bg, 0, 0, 400, 300);
    }
    // Draw obstacles
    if (map?.obstacles) {
      ctx.save();
      ctx.fillStyle = 'rgba(80,80,80,0.5)';
      map.obstacles.forEach(poly => {
        ctx.beginPath();
        poly.forEach(([x, y], i) => i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y));
        ctx.closePath();
        ctx.fill();
      });
      ctx.restore();
    }
    // Draw interactables
    if (interactables) {
      interactables.forEach(obj => {
        ctx.save();
        ctx.fillStyle = obj.type === 'trap' ? '#f00' : '#ff0';
        ctx.globalAlpha = 0.8;
        ctx.fillRect(obj.x, obj.y, obj.width, obj.height);
        ctx.restore();
      });
    }
    // Draw player
    if (playerState) {
      const img = new window.Image();
      img.src = `/assets/sprites/${playerState.type}-run.png`;
      ctx.drawImage(img, playerState.x, playerState.y, SPRITE_SIZE, SPRITE_SIZE);
    }
    // Draw opponent
    if (opponentState) {
      const img = new window.Image();
      img.src = `/assets/sprites/${opponentState.type}-run.png`;
      ctx.drawImage(img, opponentState.x, opponentState.y, SPRITE_SIZE, SPRITE_SIZE);
    }
    // Draw particles/foreground
    // ...
  };

  // API hooks
  const spawnSprite = (type, x, y) => {
    // ...
  };
  const playAnimation = (sprite, name) => {
    // ...
  };
  const shakeScreen = (intensity) => {
    // ...
  };
  const particleBurst = (x, y, type) => {
    // ...
  };
  const takeScreenshot = () => {
    const canvas = canvasRef.current;
    return canvas ? canvas.toDataURL() : null;
  };

  // Emit events
  useEffect(() => {
    // Example: collision detection
    if (onCollision && playerState && map?.obstacles) {
      // ...collision logic...
    }
    // Example: trap triggered
    if (onTrapTriggered && interactables) {
      // ...trap logic...
    }
    // Example: catch event
    if (onCatch && playerState && opponentState) {
      // ...catch logic...
    }
  }, [playerState, opponentState, map, interactables, onCollision, onTrapTriggered, onCatch]);

  return (
    <canvas ref={canvasRef} width={400} height={300} style={{
      width: '100%',
      maxWidth: 480,
      height: 300,
      background: '#222',
      borderRadius: 12,
      boxShadow: '0 0 32px #0008',
      display: 'block',
      margin: 'auto'
    }} aria-label="Game Canvas" />
  );
};

export default GameCanvas;
