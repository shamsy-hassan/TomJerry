import React, { createContext, useState, useRef, useCallback, useEffect } from "react";
import { socket } from "../socket";

export const GameContext = createContext();

export const GameProvider = ({ children, lastCharacter, bestTime, onFirstScreen }) => {
  const [selectedCharacter, setSelectedCharacter] = useState(lastCharacter || null);
  const [gameState, setGameState] = useState("idle"); // idle, loading, playing, paused, ended
  const [player, setPlayer] = useState({ x: 0, y: 0, velocity: { x: 0, y: 0 }, animationState: "idle" });
  const [opponent, setOpponent] = useState({ x: 0, y: 0, velocity: { x: 0, y: 0 }, animationState: "idle" });
  const [currentMap, setCurrentMap] = useState("house");
  const [timeLeft, setTimeLeft] = useState(30);
  const [score, setScore] = useState(0);
  const [loadingAssets, setLoadingAssets] = useState(true);
  const [autoStart, setAutoStart] = useState(false);
  const [devicePixelRatio, setDevicePixelRatio] = useState(window.devicePixelRatio);
  const bestTimeRef = useRef(bestTime || 0);

  // 🧠 Persist player stats in localStorage
  const persistStats = useCallback(() => {
    localStorage.setItem("lastCharacter", selectedCharacter);
    localStorage.setItem("bestTime", bestTimeRef.current);
  }, [selectedCharacter]);

  // 🎮 Game lifecycle controls
  const startGame = useCallback(
    (options) => {
      setGameState("loading");
      setTimeout(() => {
        setGameState("playing");
        setTimeLeft(30);
        setScore(0);
        setPlayer(options?.player || { x: 0, y: 0, velocity: { x: 0, y: 0 }, animationState: "idle" });
        setOpponent(options?.opponent || { x: 5, y: 5, velocity: { x: 0, y: 0 }, animationState: "idle" });
        setCurrentMap(options?.map || "house");
        setAutoStart(true);
        if (onFirstScreen) onFirstScreen();
      }, 500);
    },
    [onFirstScreen]
  );

  const endGame = useCallback(
    (result) => {
      setGameState("ended");
      if (result?.bestTime && result.bestTime < bestTimeRef.current) {
        bestTimeRef.current = result.bestTime;
        persistStats();
      }
    },
    [persistStats]
  );

  const restartGame = useCallback(() => {
    setGameState("loading");
    setTimeout(() => setGameState("playing"), 500);
    setTimeLeft(30);
    setScore(0);
    setPlayer({ x: 0, y: 0, velocity: { x: 0, y: 0 }, animationState: "idle" });
    setOpponent({ x: 5, y: 5, velocity: { x: 0, y: 0 }, animationState: "idle" });
    setAutoStart(true);
  }, []);

  const updateLocalPosition = useCallback((pos) => {
    setPlayer((p) => ({ ...p, ...pos }));
  }, []);

  const applyServerSnapshot = useCallback((snapshot) => {
    setPlayer(snapshot.player);
    setOpponent(snapshot.opponent);
    setTimeLeft(snapshot.timeLeft);
    setScore(snapshot.score);
  }, []);

  // 💬 Send player movement to server
  const sendMove = useCallback((moveData) => {
    if (socket.connected) {
      socket.emit("player_move", moveData);
    }
  }, []);

  // ⚡ Socket.IO events
  useEffect(() => {
    socket.on("connect", () => {
      console.log("✅ Connected to backend:", socket.id);
    });

    socket.on("disconnect", () => {
      console.log("❌ Disconnected from backend");
    });

    socket.on("game_update", (data) => {
      console.log("📡 Game update:", data);
      applyServerSnapshot(data);
    });

    socket.on("game_over", (data) => {
      console.log("🏁 Game Over:", data);
      endGame(data);
    });

    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("game_update");
      socket.off("game_over");
    };
  }, [applyServerSnapshot, endGame]);

  // 🔁 Minimal re-render optimization
  const positionRef = useRef(player);
  positionRef.current = player;

  return (
    <GameContext.Provider
      value={{
        selectedCharacter,
        setSelectedCharacter,
        gameState,
        setGameState,
        player,
        setPlayer,
        opponent,
        setOpponent,
        currentMap,
        setCurrentMap,
        timeLeft,
        setTimeLeft,
        score,
        setScore,
        loadingAssets,
        setLoadingAssets,
        autoStart,
        setAutoStart,
        devicePixelRatio,
        setDevicePixelRatio,
        startGame,
        endGame,
        restartGame,
        updateLocalPosition,
        applyServerSnapshot,
        persistStats,
        sendMove,
        bestTime: bestTimeRef.current,
      }}
    >
      {children}
    </GameContext.Provider>
  );
};
