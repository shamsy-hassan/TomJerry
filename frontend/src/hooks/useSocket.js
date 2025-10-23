import { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import { SERVER_URL } from '../utils/constants';

export default function useSocket() {
  const [connected, setConnected] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const socketRef = useRef();

  useEffect(() => {
    if (!socketRef.current) {
      socketRef.current = io(SERVER_URL, {
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000
      });
      socketRef.current.on('connect', () => setConnected(true));
      socketRef.current.on('disconnect', () => setConnected(false));
      socketRef.current.on('reconnect_attempt', () => setReconnectAttempts(a => a + 1));
    }
    return () => {
      if (socketRef.current) socketRef.current.disconnect();
    };
  }, []);

  const emit = (event, payload) => socketRef.current?.emit(event, payload);
  const on = (event, handler) => socketRef.current?.on(event, handler);
  const off = (event, handler) => socketRef.current?.off(event, handler);
  const once = (event, handler) => socketRef.current?.once(event, handler);

  return {
    emit,
    on,
    off,
    once,
    connected,
    reconnectAttempts,
    joinRoom: room => emit('join_room', { room }),
    leaveRoom: room => emit('leave_room', { room })
  };
}
