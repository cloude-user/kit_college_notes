/**
 * ============================================================================
 * 🍽️ CONCEPT 05: CONDITIONAL RENDERING & SKELETON LOADERS
 * Kitchen Analogy: The "Currently Cooking" Sign & Empty Table Setup
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python:
 *     if is_loading:
 *         show_spinner()
 *     else:
 *         show_result()
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In React, you use inline JavaScript ternary `condition ? <A /> : <B />`
 * or short-circuit logical AND `condition && <Element />`.
 * In AI interfaces, NEVER leave a blank screen while waiting for the first token!
 * Always show an animated pulsating Skeleton Loader!
 */

import React from 'react';

// 1. Skeleton Loader Component: Pulsates while waiting for model inference
export function ChatMessageSkeleton() {
  return (
    <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 w-full max-w-lg animate-pulse mb-3">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-8 h-8 rounded-full bg-slate-800"></div>
        <div className="h-4 w-28 bg-slate-800 rounded"></div>
      </div>
      <div className="space-y-2">
        <div className="h-3.5 bg-slate-800 rounded w-full"></div>
        <div className="h-3.5 bg-slate-800 rounded w-5/6"></div>
        <div className="h-3.5 bg-slate-800 rounded w-2/3"></div>
      </div>
      <div className="mt-3 flex gap-2">
        <span className="text-[11px] text-slate-600 font-mono">Thinking with Gemini-1.5-Pro...</span>
      </div>
    </div>
  );
}

// 2. Real Chat Bubble Component
export function ActualResponse({ answer, model }) {
  return (
    <div className="p-4 rounded-xl bg-slate-800 border border-slate-700 w-full max-w-lg mb-3 text-slate-100 shadow-md">
      <div className="flex items-center gap-2 mb-2 text-xs font-semibold text-emerald-400">
        <span>🤖 {model}</span>
      </div>
      <p className="text-sm leading-relaxed">{answer}</p>
    </div>
  );
}

// 3. Parent Component switching between them based on state
export function AIResponseContainer({ isLoading, responseData }) {
  return (
    <div className="p-6 bg-slate-950 min-h-[250px]">
      <h3 className="text-sm font-semibold text-slate-400 mb-3">Model Inference Stream</h3>

      {/* Ternary conditional rendering */}
      {isLoading ? (
        <ChatMessageSkeleton />
      ) : responseData ? (
        <ActualResponse answer={responseData.text} model={responseData.model} />
      ) : (
        <div className="text-sm text-slate-600 italic">No prompt submitted yet.</div>
      )}

      {/* Short-circuit && rendering for warning alerts */}
      {responseData?.finishReason === "SAFETY" && (
        <div className="p-3 bg-amber-500/10 border border-amber-500/30 text-amber-300 rounded-lg text-xs mt-2">
          ⚠️ Output was partially truncated by AI Safety Filters.
        </div>
      )}
    </div>
  );
}
