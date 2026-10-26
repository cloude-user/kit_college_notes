/**
 * ============================================================================
 * 🍽️ CONCEPT 06: LISTS & KEYS (WHY INDEX BREAKS REACT)
 * Kitchen Analogy: The Unique Order Claim Check Number
 * ============================================================================
 * 
 * 🐍 PYTHON MENTAL MODEL:
 * In Python, you loop over a list with list comprehension:
 *     html_items = [f"<li>{msg['text']}</li>" for msg in messages]
 * 
 * ⚛️ REACT MENTAL MODEL:
 * In React, you use `.map()`:
 *     messages.map(msg => <li key={msg.id}>{msg.text}</li>)
 * 
 * ⚠️ THE GOLDEN RULE OF KEYS:
 * ALWAYS provide a globally unique ID (e.g., `key={msg.id}`).
 * NEVER USE `key={index}` when items can be inserted, sorted, or deleted!
 * 
 * ❌ Why does `key={index}` fail?
 * If you delete message 0, message 1 becomes the new index 0.
 * React compares Virtual DOM node key=0 to previous key=0, thinks it's the
 * SAME component, and REUSES the old state (checkboxes, inputs, audio players break)!
 */

import React, { useState } from 'react';

export function AgentTaskList() {
  const [tasks, setTasks] = useState([
    { id: "task-001", name: "Vector Search on Knowledge Base", status: "completed" },
    { id: "task-002", name: "Re-ranking top 20 candidate chunks", status: "in_progress" },
    { id: "task-003", name: "Synthesizing answer with Citations", status: "pending" }
  ]);

  // Remove a task by unique ID
  const removeTask = (targetId) => {
    setTasks(prev => prev.filter(t => t.id !== targetId));
  };

  return (
    <div className="p-6 bg-slate-900 rounded-2xl max-w-md border border-slate-800 text-white">
      <h3 className="font-bold text-lg mb-3 text-indigo-400">🤖 Agent Execution DAG</h3>
      
      <div className="space-y-2">
        {/* ✅ CORRECT: Using unique stable ID (t.id) as key */}
        {tasks.map((task) => (
          <div 
            key={task.id} 
            className="flex items-center justify-between p-3 rounded-xl bg-slate-800/80 border border-slate-700/60"
          >
            <div className="flex items-center gap-2">
              <span className={`w-2.5 h-2.5 rounded-full ${
                task.status === 'completed' ? 'bg-emerald-400' :
                task.status === 'in_progress' ? 'bg-amber-400 animate-ping' : 'bg-slate-600'
              }`} />
              <span className="text-sm font-medium">{task.name}</span>
            </div>
            
            <button 
              onClick={() => removeTask(task.id)}
              className="text-slate-500 hover:text-rose-400 text-xs px-2 py-1 rounded"
              title="Delete task"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      <div className="mt-4 p-3 bg-slate-950 rounded-lg text-xs text-slate-400 font-mono">
        Active Tasks: {tasks.length} (React keys track each node across diffs)
      </div>
    </div>
  );
}
