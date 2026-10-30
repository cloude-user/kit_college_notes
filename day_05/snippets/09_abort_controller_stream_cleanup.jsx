/**
 * ============================================================================
 * 🍽️ CONCEPT 09: ABORTCONTROLLER & STOP GENERATION BUTTON
 * Kitchen Analogy: The "STOP THE ORDER" Kitchen Bell
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, pressing Ctrl+C raises KeyboardInterrupt and cancels execution.
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In web browsers, ongoing HTTP fetch streams DO NOT stop just because the
 * user clicked away. They keep consuming user bandwidth and API credits!
 * The Standard Web Solution: `AbortController()`!
 * 1. Pass `controller.signal` into `fetch(url, { signal })`
 * 2. When the user clicks "Stop Generating" -> call `controller.abort()`!
 */

import React, { useState, useRef } from 'react';

export function AbortableChatGenerator() {
  const [output, setOutput] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  
  // Keep the AbortController instance stored in a ref so it survives renders
  const abortControllerRef = useRef(null);

  const startGenerating = async () => {
    // 1. Create a fresh AbortController
    const controller = new AbortController();
    abortControllerRef.current = controller;
    setIsGenerating(true);
    setOutput("");

    try {
      // In real code: const res = await fetch("/api/chat", { signal: controller.signal });
      // Here we simulate a chunked stream reader:
      const chunks = [
        "Step 1: Ingesting enterprise documents...\n",
        "Step 2: Building FAISS dense index...\n",
        "Step 3: Calculating Cross-Encoder rerank scores...\n",
        "Step 4: Formulating grounded final response...\n"
      ];

      for (const chunk of chunks) {
        if (controller.signal.aborted) {
          throw new DOMException("Stream aborted by user", "AbortError");
        }
        await new Promise(r => setTimeout(r, 600));
        setOutput(prev => prev + chunk);
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        setOutput(prev => prev + "\n[STREAM TERMINATED BY USER]");
      } else {
        setOutput(prev => prev + `\n[ERROR: ${err.message}]`);
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const stopGenerating = () => {
    // 2. Trigger the abort signal
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl max-w-lg text-white">
      <h3 className="font-bold text-lg mb-3 text-cyan-400">🛑 LLM Stream Interrupter</h3>
      
      <div className="flex gap-2 mb-4">
        <button 
          onClick={startGenerating}
          disabled={isGenerating}
          className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 px-4 py-2 rounded-lg text-sm font-semibold transition"
        >
          {isGenerating ? "Generating..." : "Start Generation"}
        </button>

        <button 
          onClick={stopGenerating}
          disabled={!isGenerating}
          className="bg-rose-600 hover:bg-rose-500 disabled:bg-slate-800 disabled:text-slate-600 px-4 py-2 rounded-lg text-sm font-semibold transition"
        >
          Stop Generating (Abort)
        </button>
      </div>

      <pre className="p-4 bg-slate-950 rounded-xl font-mono text-xs text-slate-300 min-h-[120px] whitespace-pre-wrap">
        {output || "Click 'Start Generation' to observe streaming..."}
      </pre>
    </div>
  );
}
