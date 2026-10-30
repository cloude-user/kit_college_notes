/**
 * ============================================================================
 * 🍽️ CONCEPT 10: useRef & CHAT AUTO-SCROLL (WITHOUT RE-RENDERS)
 * Kitchen Analogy: The Head Chef's Clipboard (Stores notes without ringing bells)
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, you can mutate an object attribute `self.last_seen = time.time()`
 * without recalculating or rebuilding the entire class.
 * 
 * ⚛️ REACT MENTAL MODEL:
 * If you store data in `useState`, updating it CAUSES THE COMPONENT TO RE-RENDER.
 * But what if you want to:
 * 1. Store a value that persists across renders WITHOUT triggering a re-render?
 * 2. Directly reference a real browser DOM node (like a scrollable `<div>`)?
 * -> YOU USE `useRef()`!
 */

import React, { useState, useEffect, useRef } from 'react';

export function AutoScrollChatContainer() {
  const [messages, setMessages] = useState([
    { id: 1, text: "System initialized. Vector store connected." }
  ]);

  // 1. Create a ref to attach to the bottom anchor element
  const chatBottomRef = useRef(null);

  // 2. Auto-scroll to the bottom whenever messages change
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const addMessage = () => {
    setMessages(prev => [
      ...prev,
      { id: Date.now(), text: `Token chunk received at ${new Date().toLocaleTimeString()}` }
    ]);
  };

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl max-w-md text-white">
      <div className="flex justify-between items-center mb-3">
        <h3 className="font-bold text-sm text-indigo-400">📜 Auto-Scrolling Chat Log</h3>
        <button 
          onClick={addMessage}
          className="bg-indigo-600 hover:bg-indigo-500 text-xs px-3 py-1.5 rounded-lg font-semibold"
        >
          + Add Stream Chunk
        </button>
      </div>

      {/* Scrollable container with fixed height */}
      <div className="h-48 overflow-y-auto bg-slate-950 rounded-xl p-3 space-y-2 border border-slate-800 text-xs font-mono">
        {messages.map(msg => (
          <div key={msg.id} className="p-2 bg-slate-900 rounded border border-slate-800">
            {msg.text}
          </div>
        ))}
        {/* Invisible anchor target for scrollIntoView */}
        <div ref={chatBottomRef} />
      </div>
    </div>
  );
}
