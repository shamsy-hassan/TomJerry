import React, { useContext, useEffect, useState } from 'react';
import GameCanvas from '../components/GameCanvas';
import HUD from '../components/HUD';
import Controls from '../components/Controls';
import ScoreBoard from '../components/ScoreBoard';
import GameResult from '../components/GameResult';
import { GameContext } from '../context/GameContext';
import useSocket from '../hooks/useSocket';

const Game = () => {
  const { gameState, startGame, endGame, player, opponent, currentMap, timeLeft } = useContext(GameContext);
  const [result, setResult] = useState(null);
  const socket = useSocket();

  useEffect(() => {
    startGame();
    socket.emit('join_room', { room: 'main' });
    socket.on('match_end', res => {
      setResult(res.result);
      endGame(res);
    });
    return () => {
      socket.emit('leave_room', { room: 'main' });
      socket.off('match_end');
      endGame();
    };
  }, [startGame, endGame, socket]);

  // AI fallback if socket fails
  useEffect(() => {
    if (!socket.connected) {
      // Fallback to AI logic here
    }
  }, [socket.connected]);

  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: 480, margin: 'auto' }}>
      <GameCanvas map={currentMap} playerState={player} opponentState={opponent} />
      <HUD />
      <Controls />
      <ScoreBoard />
      {result && <GameResult result={result} />}
    </div>
  );
};

export default Game;
