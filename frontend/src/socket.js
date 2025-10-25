// src/socket.js
import { io } from "socket.io-client";

// Connect to your backend
export const socket = io("http://localhost:5000", {
  transports: ["websocket"],
  reconnection: true,
});
