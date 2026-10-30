/**
 * ============================================================================
 * 🍽️ CONCEPT 07: CONTROLLED COMPONENTS & AI HYPERPARAMETER FORM
 * Kitchen Analogy: The Single Master Thermostat on the Oven
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python UI frameworks (Streamlit), `st.slider(...)` keeps its state
 * synchronized with your Python variable automatically.
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In vanilla HTML, an `<input>` stores its own value inside the browser DOM.
 * But in React, WE WANT REACT TO BE THE SINGLE SOURCE OF TRUTH!
 * Controlled Component Formula:
 * 1. `value={temperature}` (React tells the input what to show)
 * 2. `onChange={(e) => setTemperature(e.target.value)}` (Input tells React user typed)
 */

import React, { useState } from 'react';

export function AIHyperparameterForm({ onConfigSubmit }) {
  // Controlled form state
  const [model, setModel] = useState("gemini-1.5-pro");
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(2048);
  const [systemPrompt, setSystemPrompt] = useState("You are an expert full-stack AI engineer.");

  const handleSubmit = (e) => {
    e.preventDefault(); // 🛑 CRUCIAL: Stops browser from submitting form & reloading page!
    onConfigSubmit({ model, temperature, maxTokens, systemPrompt });
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 bg-slate-900 border border-slate-800 rounded-2xl max-w-lg text-slate-100 shadow-xl space-y-4">
      <h3 className="text-lg font-bold text-emerald-400 flex items-center gap-2">
        ⚙️ Model Inference Hyperparameters
      </h3>

      {/* Model Selection Dropdown */}
      <div>
        <label className="block text-xs font-semibold text-slate-400 mb-1">FOUNDATION MODEL</label>
        <select 
          value={model} 
          onChange={(e) => setModel(e.target.value)}
          className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-200 focus:outline-none focus:border-emerald-500"
        >
          <option value="gemini-1.5-pro">Google Gemini 1.5 Pro (2M Context)</option>
          <option value="gpt-4o">OpenAI GPT-4o (Multimodal)</option>
          <option value="claude-3-5-sonnet">Anthropic Claude 3.5 Sonnet</option>
          <option value="llama-3.1-70b">Meta Llama 3.1 70B (Local Ollama)</option>
        </select>
      </div>

      {/* Controlled Temperature Slider */}
      <div>
        <div className="flex justify-between text-xs font-semibold text-slate-400 mb-1">
          <span>TEMPERATURE (CREATIVITY vs DETERMINISM)</span>
          <span className="font-mono text-emerald-400 font-bold">{temperature}</span>
        </div>
        <input 
          type="range" 
          min="0" 
          max="1.5" 
          step="0.05"
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value))}
          className="w-full accent-emerald-500 cursor-pointer"
        />
        <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-0.5">
          <span>0.0 (Strict Code/Math)</span>
          <span>0.7 (Default Balance)</span>
          <span>1.5 (High Creative)</span>
        </div>
      </div>

      {/* Controlled System Prompt */}
      <div>
        <label className="block text-xs font-semibold text-slate-400 mb-1">SYSTEM PROMPT (ROLE CONTEXT)</label>
        <textarea 
          rows={3}
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-emerald-500 resize-none"
        />
      </div>

      <button 
        type="submit" 
        className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 rounded-lg font-semibold text-sm transition shadow-lg shadow-emerald-900/30"
      >
        Save Model Configuration
      </button>
    </form>
  );
}
