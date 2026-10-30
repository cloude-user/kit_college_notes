/**
 * ============================================================================
 * 🍽️ CONCEPT 02: PROPS & UNIDIRECTIONAL DATA FLOW
 * Kitchen Analogy: The Customer Order Ticket
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, props are like function arguments passed by the caller:
 *     def render_chat_bubble(sender, text, timestamp, is_error=False):
 *         ...
 * 
 * ⚛️ REACT MENTAL MODEL:
 * Props (short for "Properties") are passed from Parent component to Child.
 * Rule: PROPS ARE STRICTLY READ-ONLY (IMMUTABLE)!
 * The line cook NEVER alters the customer's written order ticket.
 * If the line cook wants to modify data, they must use State (the prep bowl).
 */

import React from 'react';

// Child Component: Receives 'props' object (destructured for clean code)
export function ChatMessageCard({ role, content, timestamp, modelName, tokenCount }) {
  const isUser = role === 'user';
  const isSystem = role === 'system';

  return (
    <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[75%] rounded-2xl p-4 shadow-lg ${
        isUser 
          ? 'bg-blue-600 text-white rounded-br-sm' 
          : isSystem 
            ? 'bg-amber-950/40 border border-amber-600/30 text-amber-200' 
            : 'bg-slate-800 border border-slate-700 text-slate-100 rounded-bl-sm'
      }`}>
        {/* Header with metadata passed via props */}
        <div className="flex items-center justify-between text-xs opacity-70 mb-2 gap-4">
          <span className="font-semibold uppercase tracking-wider">
            {isUser ? '👤 You' : `🤖 ${modelName || 'Assistant'}`}
          </span>
          <span className="font-mono">{timestamp}</span>
        </div>

        {/* Message body */}
        <div className="text-sm leading-relaxed whitespace-pre-wrap font-sans">
          {content}
        </div>

        {/* Optional footer if tokenCount prop was provided */}
        {tokenCount && (
          <div className="mt-2 pt-2 border-t border-white/10 text-[11px] opacity-60 font-mono text-right">
            {tokenCount} tokens consumed
          </div>
        )}
      </div>
    </div>
  );
}

// Parent Component: Hands the props to children (like the waiter handing tickets)
export function ChatConversationPreview() {
  return (
    <div className="p-6 bg-slate-950 min-h-screen">
      <ChatMessageCard 
        role="user" 
        content="Explain the difference between Real DOM and Virtual DOM in 1 sentence." 
        timestamp="20:25:01" 
      />
      <ChatMessageCard 
        role="assistant" 
        modelName="GPT-4o"
        content="Real DOM recalculates layout for the whole page when modified, while Virtual DOM diffs changes in memory and updates only the altered HTML tags." 
        timestamp="20:25:03" 
        tokenCount={34}
      />
    </div>
  );
}
