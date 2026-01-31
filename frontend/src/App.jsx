import React from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="min-h-screen w-full bg-vedic-bg text-vedic-text selection:bg-vedic-primary selection:text-vedic-bg font-sans relative pt-20">

      {/* Background Elements */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-vedic-secondary/20 via-vedic-bg to-vedic-bg pointer-events-none z-0"></div>

      {/* Subtle Rotating Mandala/Chakra Glow */}
      <div className="fixed top-[-50%] left-[-50%] w-[200%] h-[200%] bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-[0.03] animate-spin-slow pointer-events-none z-0"></div>
      <div className="fixed bottom-0 right-0 w-[500px] h-[500px] bg-vedic-primary/5 rounded-full blur-[120px] pointer-events-none z-0"></div>

      {/* Main Content Area */}
      <div className="w-full max-w-5xl mx-auto px-4 pb-10 relative z-10">
        <ChatInterface />
      </div>
    </div>
  );
}

export default App;
