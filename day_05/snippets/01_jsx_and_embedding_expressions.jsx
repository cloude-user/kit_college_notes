/**
 * ============================================================================
 * 🍽️ CONCEPT 01: JSX & EMBEDDING EXPRESSIONS
 * Kitchen Analogy: The Recipe Card with Dynamic Portion Stickers
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, you insert variables into strings using f-strings:
 *     model = "Claude-3-Opus"
 *     tokens = 1500
 *     output = f"Model: {model} | Cost: ${tokens * 0.000015:.4f}"
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In React, JSX allows you to insert live JavaScript expressions directly
 * into HTML using single curly braces `{}`:
 *     <h1>Model: {model}</h1>
 *     <span>Cost: ${(tokens * 0.000015).toFixed(4)}</span>
 * 
 * ⚠️ CORE REVELATION:
 * A Python function returns raw data (a dict, str, or int).
 * A React component function returns a LIVING HTML USER INTERFACE (Virtual DOM).
 */

import React from 'react';

export function ModelStatusBadge() {
  // 1. Raw JavaScript variables (like Python variables)
  const activeModel = "Claude-3-7-Sonnet";
  const contextLength = 200000;
  const isOnline = true;
  const latencyMs = 240;

  // 2. Returning JSX (HTML with embedded JavaScript expressions)
  return (
    <div className="p-4 rounded-xl border border-slate-700 bg-slate-900 text-slate-100 max-w-md shadow-xl">
      {/* Dynamic string embedding - exactly like Python f"{activeModel}" */}
      <div className="flex items-center justify-between">
        <h3 className="font-bold text-lg text-emerald-400">🤖 {activeModel}</h3>
        <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
          isOnline ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300'
        }`}>
          {/* Conditional ternary expression inside JSX */}
          {isOnline ? "● READY" : "○ OFFLINE"}
        </span>
      </div>

      <p className="text-sm text-slate-400 mt-2">
        Active Context Window: <span className="text-indigo-300 font-mono font-medium">{(contextLength / 1000).toLocaleString()}k tokens</span>
      </p>

      {/* Evaluating arithmetic right inside JSX */}
      <div className="mt-3 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-500">
        <span>Roundtrip Latency:</span>
        <span className="font-mono text-amber-400 font-semibold">{latencyMs} ms ({latencyMs < 300 ? "⚡ FAST" : "🐢 SLOW"})</span>
      </div>
    </div>
  );
}
