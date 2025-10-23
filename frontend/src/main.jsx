import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { GameProvider } from './context/GameContext';
import { SoundProvider } from './context/SoundContext';
import './styles/index.css';

// Global CSS reset
const style = document.createElement('style');
style.innerHTML = `*{box-sizing:border-box;}body{margin:0;padding:0;}`;
document.head.appendChild(style);

// Preload persisted values
const lastCharacter = localStorage.getItem('lastCharacter');
const bestTime = localStorage.getItem('bestTime');

// Global error boundary
class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { hasError: false }; }
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error, info) { console.error('Global Error:', error, info); }
  render() { return this.state.hasError ? <div>Something went wrong.</div> : this.props.children; }
}

// Lazy WebSocket connection
let socketInitialized = false;
function lazyInitSocket() {
  if (!socketInitialized) {
    import('./hooks/useSocket').then();
    socketInitialized = true;
  }
}

// Service worker registration (optional)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}

const root = createRoot(document.getElementById('root'));
root.render(
  <StrictMode>
    <ErrorBoundary>
      <SoundProvider>
        <GameProvider lastCharacter={lastCharacter} bestTime={bestTime} onFirstScreen={lazyInitSocket}>
          <App />
        </GameProvider>
      </SoundProvider>
    </ErrorBoundary>
  </StrictMode>
);
