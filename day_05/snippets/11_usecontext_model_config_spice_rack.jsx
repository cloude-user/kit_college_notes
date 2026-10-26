/**
 * ============================================================================
 * 🍽️ CONCEPT 11: useContext & AVOIDING PROP DRILLING
 * Kitchen Analogy: The Central Kitchen Spice Rack (Available to any station)
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, you avoid passing `config` through 10 nested functions by using
 * dependency injection or a module-level singleton: `from config import settings`.
 * 
 * ⚛️ REACT MENTAL MODEL:
 * Passing props down through 5 levels of components (App -> Chat -> Window -> Input -> Button)
 * is called "PROP DRILLING" and is agonizing to maintain.
 * `createContext` + `useContext` provides a TELEPORTATION TUNNEL for global data!
 */

import React, { createContext, useContext, useState } from 'react';

// 1. Create the Context (The Spice Rack)
const AIConfigContext = createContext(null);

// 2. Provider Component (Places the Spice Rack in the Kitchen)
export function AIConfigProvider({ children }) {
  const [modelConfig, setModelConfig] = useState({
    activeModel: "gpt-4o",
    apiKeyPresent: true,
    temperature: 0.7
  });

  return (
    <AIConfigContext.Provider value={{ modelConfig, setModelConfig }}>
      {children}
    </AIConfigContext.Provider>
  );
}

// 3. Deeply nested child component consumes context directly (NO PROP DRILLING!)
export function DeepNestedStatusTag() {
  const { modelConfig } = useContext(AIConfigContext);

  return (
    <div className="p-2 rounded bg-indigo-950/60 border border-indigo-700/50 text-indigo-300 text-xs font-mono">
      Active: <strong>{modelConfig.activeModel}</strong> (T={modelConfig.temperature})
    </div>
  );
}

// 4. Demonstration Component
export function ContextDemoApp() {
  return (
    <AIConfigProvider>
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl max-w-md text-white">
        <h3 className="font-bold text-sm mb-3 text-emerald-400">🌐 Context Spice Rack Demonstration</h3>
        <p className="text-xs text-slate-400 mb-3">This tag is 5 levels deep in the component tree without any passed props:</p>
        <DeepNestedStatusTag />
      </div>
    </AIConfigProvider>
  );
}
