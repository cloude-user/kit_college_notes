/**
 * ============================================================================
 * 🍽️ CONCEPT 03: useState & THE FRESH PIZZA IMMUTABILITY RULE
 * Kitchen Analogy: The Line Cook's Active Prep Bowl
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, you can mutate a list in-place:
 *     messages = []
 *     messages.append("new message")  # Mutates the same object in RAM!
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In React, YOU MUST NEVER MUTATE STATE DIRECTLY!
 * If you write `messages.push(newMsg)`, React checks object identity (===).
 * It sees the same RAM address and ASSUMES NOTHING CHANGED -> ZERO RE-RENDER!
 * 
 * 🍕 THE FRESH PIZZA RULE:
 * If a customer orders extra mushrooms, you don't scrape the cooked pizza.
 * You stretch a BRAND NEW DOUGH, copy the existing toppings, and add mushrooms!
 * Code: `setMessages(prevMessages => [...prevMessages, newMsg]);`
 */

import React, { useState } from 'react';

export function PromptHistoryManager() {
  // 1. Declare state: [currentValue, setterFunction] = useState(initialValue)
  const [prompts, setPrompts] = useState([
    "Summarize the Q3 Financial Earnings",
    "Extract all action items from meeting transcript"
  ]);
  const [inputVal, setInputVal] = useState("");

  const handleAddPrompt = () => {
    if (!inputVal.trim()) return;

    // ❌ FATAL BEGINNER MISTAKE (MUTATION):
    // prompts.push(inputVal);
    // setPrompts(prompts); // React thinks nothing changed! UI freezes!

    // ✅ THE REACT WAY: The Spread Operator [...] creates a FRESH new array!
    setPrompts(prevPrompts => [...prevPrompts, inputVal.trim()]);
    setInputVal(""); // Clear the input box
  };

  const handleDelete = (indexToDelete) => {
    // Return a fresh new array with that element excluded (.filter())
    setPrompts(prevPrompts => prevPrompts.filter((_, idx) => idx !== indexToDelete));
  };

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl max-w-lg text-white">
      <h2 className="text-xl font-bold mb-4 text-emerald-400">⚡ Saved System Prompts</h2>

      {/* Input area */}
      <div className="flex gap-2 mb-4">
        <input 
          type="text" 
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder="Add a new system prompt..."
          className="flex-1 bg-slate-950 border border-slate-700 px-3 py-2 rounded-lg text-sm focus:outline-none focus:border-emerald-500"
        />
        <button 
          onClick={handleAddPrompt}
          className="bg-emerald-600 hover:bg-emerald-500 px-4 py-2 rounded-lg text-sm font-semibold transition"
        >
          Add
        </button>
      </div>

      {/* Render list of prompts */}
      <ul className="space-y-2">
        {prompts.map((promptText, idx) => (
          <li key={idx} className="flex justify-between items-center bg-slate-800/80 px-3 py-2 rounded-lg text-sm border border-slate-700/50">
            <span className="truncate pr-2">📌 {promptText}</span>
            <button 
              onClick={() => handleDelete(idx)}
              className="text-rose-400 hover:text-rose-300 font-bold px-2 py-1 text-xs"
            >
              ✕ Delete
            </button>
          </li>
        ))}
      </ul>
      <p className="text-xs text-slate-500 mt-3 font-mono">Count: {prompts.length} prompts</p>
    </div>
  );
}
