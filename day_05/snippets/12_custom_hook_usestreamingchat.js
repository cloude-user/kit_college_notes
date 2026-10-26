/**
 * ============================================================================
 * 🍽️ CONCEPT 12: CUSTOM HOOKS (useStreamingChat)
 * Kitchen Analogy: The Executive Chef's Standardized Master Recipe Pack
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, you package repeated logic into a reusable class or helper function:
 *     class StreamingChatClient: ...
 * 
 * ⚛️ REACT MENTAL MODEL:
 * When multiple components need the SAME combination of `useState` + `useEffect`
 * (e.g., token streaming, abort handling, message history), you package them
 * into a CUSTOM HOOK named `use...()`!
 */

import { useState, useRef, useCallback } from 'react';

export function useStreamingChat(apiEndpoint = "/api/chat") {
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);

  const sendMessage = useCallback(async (promptText) => {
    if (!promptText.trim()) return;

    setError(null);
    setIsStreaming(true);

    const userMessage = { id: `msg-${Date.now()}`, role: 'user', content: promptText };
    const assistantMessageId = `msg-${Date.now() + 1}`;
    
    // Add user message and an empty assistant placeholder
    setMessages(prev => [
      ...prev, 
      userMessage, 
      { id: assistantMessageId, role: 'assistant', content: "" }
    ]);

    // Create abort controller for this specific request
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      // In production: const response = await fetch(apiEndpoint, { method: "POST", signal: controller.signal, ... })
      // Simulated SSE streaming loop:
      const simulatedChunks = ["Understood! ", "Let me analyze ", "the vector database. ", "Here is the verified ", "answer."];
      
      for (const chunk of simulatedChunks) {
        if (controller.signal.aborted) break;
        await new Promise(r => setTimeout(r, 200));

        setMessages(prev => prev.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, content: msg.content + chunk } 
            : msg
        ));
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message);
      }
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  }, [apiEndpoint]);

  const stop = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  }, []);

  const clearHistory = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    isStreaming,
    error,
    sendMessage,
    stop,
    clearHistory
  };
}
