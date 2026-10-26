/**
 * ============================================================================
 * 🍽️ CONCEPT 04: SYNTHETICEVENTS & KEYBOARD SHORTCUTS
 * Kitchen Analogy: The Kitchen Bell (Dings when food is ready or order arrives)
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python CLI apps, you use `input()` which blocks execution until Enter.
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In React, the browser is event-driven. React wraps native browser events in
 * a cross-browser `SyntheticEvent` wrapper:
 * - `onClick`: Click trigger
 * - `onChange`: Every single character typed
 * - `onKeyDown`: Intercepting keys before typing (Enter to Send vs Shift+Enter for Newline)
 */

import React, { useState } from 'react';

export function AIChatInputBar({ onSendMessage, isGenerating }) {
  const [text, setText] = useState("");

  const handleKeyDown = (e) => {
    // 🧠 AI INTERFACE PATTERN:
    // If user presses Enter WITHOUT Shift -> Send the message!
    // If user presses Enter WITH Shift -> Let them create a multi-line newline!
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Stop default newline creation
      submitMessage();
    }
  };

  const submitMessage = () => {
    if (!text.trim() || isGenerating) return;
    onSendMessage(text.trim());
    setText(""); // Reset input box
  };

  return (
    <div className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl p-3 shadow-2xl focus-within:border-indigo-500 transition">
      <textarea
        rows={3}
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your AI prompt here... (Press Enter to Send, Shift+Enter for new line)"
        className="w-full bg-transparent resize-none text-slate-100 placeholder-slate-500 focus:outline-none text-sm font-sans"
        disabled={isGenerating}
      />
      <div className="flex justify-between items-center mt-2 pt-2 border-t border-slate-800">
        <span className="text-xs text-slate-500 font-mono">
          {text.length} chars | ~{Math.ceil(text.length / 4)} tokens
        </span>
        <button
          onClick={submitMessage}
          disabled={!text.trim() || isGenerating}
          className={`px-4 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition ${
            !text.trim() || isGenerating
              ? 'bg-slate-800 text-slate-600 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-md shadow-indigo-600/30'
          }`}
        >
          {isGenerating ? "⏳ Streaming..." : "Send Prompt ➔"}
        </button>
      </div>
    </div>
  );
}
