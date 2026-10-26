/**
 * ============================================================================
 * 🍽️ CONCEPT 08: useEffect & SERVER-SENT EVENTS (SSE) STREAMING
 * Kitchen Analogy: Calling the Fresh Fish Market (External Side Effect)
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python FastAPI, you stream tokens using a generator:
 *     async for chunk in client.chat.completions.create(stream=True):
 *         yield f"data: {chunk}\n\n"
 * 
 * ⚛️ REACT MENTAL MODEL:
 * React components must be PURE functions (calculating UI from props/state).
 * When you need to talk to the OUTSIDE WORLD (APIs, WebSockets, Timers):
 * YOU USE `useEffect(setupFunction, dependencyArray)`!
 * 
 * 🧹 CLEANUP FUNCTION:
 * Returning a function from `useEffect` cleans up resources (cancelling streams,
 * removing event listeners) when the component unmounts.
 */

import React, { useState, useEffect } from 'react';

export function TokenStreamingMonitor({ sessionId }) {
  const [streamedText, setStreamedText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    // 1. External side-effect: Setup SSE or Fetch Stream
    let isCancelled = false;
    setIsStreaming(true);
    setStreamedText("");

    // Simulated token stream generator for classroom demonstration
    const mockTokens = ["Analyzing ", "user ", "query...", " Retrieving ", "vector ", "embeddings...", " Done!"];
    let tokenIndex = 0;

    const interval = setInterval(() => {
      if (tokenIndex < mockTokens.length && !isCancelled) {
        setStreamedText(prev => prev + mockTokens[tokenIndex]);
        tokenIndex++;
      } else {
        clearInterval(interval);
        if (!isCancelled) setIsStreaming(false);
      }
    }, 250);

    // 2. 🧹 CLEANUP FUNCTION: Called automatically if component unmounts or sessionId changes!
    return () => {
      isCancelled = true;
      clearInterval(interval);
      console.log(`[CLEANUP] Stream connection aborted for session ${sessionId}`);
    };
  }, [sessionId]); // Only re-run if sessionId changes!

  return (
    <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl max-w-md text-white font-mono text-xs">
      <div className="flex justify-between items-center mb-2 text-slate-400">
        <span>STREAM CHANNEL: {sessionId}</span>
        <span className={isStreaming ? "text-amber-400 animate-pulse" : "text-emerald-400"}>
          {isStreaming ? "● STREAMING" : "✓ FINISHED"}
        </span>
      </div>
      <div className="p-3 bg-slate-950 rounded-lg min-h-[60px] text-slate-200">
        {streamedText}
        {isStreaming && <span className="inline-block w-2 h-4 bg-emerald-400 ml-1 animate-ping" />}
      </div>
    </div>
  );
}
