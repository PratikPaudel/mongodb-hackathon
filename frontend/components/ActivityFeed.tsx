// components/ActivityFeed.tsx
'use client';

import { AgentMessage } from '@/hooks/useWebSocket';
import { useEffect, useRef } from 'react';

interface ActivityFeedProps {
  messages: AgentMessage[];
}

export function ActivityFeed({ messages }: ActivityFeedProps) {
  const feedRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (feedRef.current) {
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
    }
  }, [messages]);

  const getIcon = (type: string) => {
    const icons: Record<string, string> = {
      agent_created: '👤',
      agent_start: '🚀',
      agent_position: '📍',
      agent_completed: '✅',
      agent_failed: '❌',
      skill_created: '✨',
      skill_extracted: '🎓',
      skill_retrieved: '🔍',
      skill_transfer: '🔄',
      task_started: '▶️',
      demo_complete: '🎉',
      alpha_complete_waiting: '⏸️',
      subscribed: '🔔',
      pong: '🏓',
      stats: '📊',
    };
    return icons[type] || '📌';
  };

  const formatType = (type: string) => {
    return type
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const getEventColor = (type: string) => {
    if (type.includes('completed') || type.includes('success')) return 'border-green-500';
    if (type.includes('failed') || type.includes('error')) return 'border-red-500';
    if (type.includes('retrieved')) return 'border-purple-600';
    if (type.includes('transfer') || type.includes('skill')) return 'border-purple-500';
    if (type.includes('start') || type.includes('created')) return 'border-blue-500';
    return 'border-slate-300';
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-4 border-b border-slate-200 bg-slate-50">
        <h2 className="text-lg font-semibold text-slate-900">Activity Feed</h2>
        <p className="text-sm text-slate-600 mt-1">Real-time agent events</p>
      </div>

      <div ref={feedRef} className="p-4 space-y-3 max-h-[600px] overflow-y-auto scroll-smooth">
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-slate-500 text-sm">No activity yet. Start a demo to see real-time updates.</p>
          </div>
        ) : (
          messages.map((message, idx) => (
            <div
              key={`${message.timestamp}-${idx}`}
              className={`border-l-4 ${getEventColor(message.type)} pl-4 py-2 bg-slate-50 rounded-r transition-all hover:bg-slate-100`}
            >
              <div className="flex items-start gap-2">
                <span className="text-2xl">{getIcon(message.type)}</span>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm text-slate-900">{formatType(message.type)}</p>
                  <div className="text-xs text-slate-600 mt-1 space-y-1">
                    {/* Display relevant data based on event type */}
                    {message.type === 'agent_start' && (
                      <p>
                        <span className="font-medium">{message.data.agent_name}</span> started using{' '}
                        <span className="font-mono bg-slate-200 px-1 rounded">{message.data.strategy}</span>
                      </p>
                    )}
                    {message.type === 'agent_completed' && (
                      <p>
                        Completed in <span className="font-bold text-green-700">{message.data.completion_time?.toFixed(2)}s</span> ({message.data.steps} steps)
                      </p>
                    )}
                    {message.type === 'skill_retrieved' && (
                      <div className="space-y-1">
                        <p className="font-bold text-purple-700">
                          {message.data.agent_name} retrieved skill from MongoDB!
                        </p>
                        <p className="text-xs">
                          Skill: <span className="font-medium">{message.data.skill_name}</span>
                        </p>
                        <p className="text-xs">
                          Path Length: {message.data.path_length} steps
                        </p>
                        <p className="text-xs bg-purple-100 px-2 py-1 rounded">
                          🔍 MongoDB Atlas Vector Search
                        </p>
                      </div>
                    )}
                    {message.type === 'skill_transferred' && (
                      <p>
                        Skill transferred from <span className="font-medium">{message.data.from_agent}</span> to{' '}
                        <span className="font-medium">{message.data.to_agent}</span>
                      </p>
                    )}
                    {message.type === 'alpha_complete_waiting' && (
                      <div className="space-y-1">
                        <p className="font-bold text-blue-700">
                          Agent Alpha completed! Ready for Agent Beta.
                        </p>
                        <p className="text-xs">
                          Time: {message.data.completion_time?.toFixed(2)}s | Steps: {message.data.steps}
                        </p>
                        <p className="text-xs text-purple-600">
                          Click "Run Agent Beta" button to continue →
                        </p>
                      </div>
                    )}
                    {message.type === 'demo_complete' && (
                      <div className="space-y-1">
                        <p>
                          {message.data.agent_a?.name}: {message.data.agent_a?.time?.toFixed(2)}s
                        </p>
                        <p>
                          {message.data.agent_b?.name}: {message.data.agent_b?.time?.toFixed(2)}s
                        </p>
                        <p className="font-bold text-green-700">
                          Improvement: {message.data.improvement_percentage?.toFixed(1)}%
                        </p>
                      </div>
                    )}
                    {!['agent_start', 'agent_completed', 'skill_retrieved', 'skill_transfer', 'alpha_complete_waiting', 'demo_complete'].includes(message.type) && message.data && (
                      <p className="truncate">{JSON.stringify(message.data).slice(0, 100)}...</p>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
