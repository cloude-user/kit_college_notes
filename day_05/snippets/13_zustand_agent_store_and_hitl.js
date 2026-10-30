/**
 * ============================================================================
 * 🍽️ CONCEPT 13: ZUSTAND AGENT STORE & HUMAN-IN-THE-LOOP (HITL)
 * Kitchen Analogy: The Banquet Master Whiteboard
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python LangGraph / CrewAI, an agent workflow passes a shared state dictionary:
 *     state = {"messages": [], "active_agent": "Coder", "pending_tool_call": {...}}
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In complex multi-agent web apps, local component state is not enough.
 * Zustand provides an ultra-lightweight, zero-boilerplate global store.
 * Agents can update their progress, and if an agent requests a sensitive tool
 * (e.g. `execute_sql_delete`), the UI pauses for Human-in-the-Loop (HITL) approval!
 */

// Simulating Zustand store creation pattern for browser & Node environments
export const createAgentStore = () => {
  let state = {
    agents: [
      { id: "planner", name: "Strategic Planner", status: "idle" },
      { id: "researcher", name: "Web & Doc Researcher", status: "idle" },
      { id: "coder", name: "Python Coder", status: "idle" }
    ],
    pendingApproval: null, // Holds tool call awaiting human confirmation
    executionLogs: []
  };

  const listeners = new Set();
  const notify = () => listeners.forEach(fn => fn(state));

  return {
    getState: () => state,
    subscribe: (fn) => {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },

    // Action: Set an agent's active status
    setAgentStatus: (agentId, status) => {
      state = {
        ...state,
        agents: state.agents.map(a => a.id === agentId ? { ...a, status } : a),
        executionLogs: [...state.executionLogs, `[${new Date().toLocaleTimeString()}] Agent ${agentId} -> ${status}`]
      };
      notify();
    },

    // Action: Propose a sensitive tool call requiring Human Approval (HITL)
    requestApproval: (toolCall) => {
      state = {
        ...state,
        pendingApproval: toolCall,
        executionLogs: [...state.executionLogs, `⚠️ HUMAN APPROVAL REQUIRED: ${toolCall.toolName}`]
      };
      notify();
    },

    // Action: Human clicks "Approve" or "Reject"
    resolveApproval: (approved) => {
      const toolName = state.pendingApproval?.toolName;
      state = {
        ...state,
        pendingApproval: null,
        executionLogs: [
          ...state.executionLogs, 
          approved ? `✅ Human APPROVED tool: ${toolName}` : `🛑 Human REJECTED tool: ${toolName}`
        ]
      };
      notify();
    }
  };
};
