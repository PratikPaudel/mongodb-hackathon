// components/AgentCard.tsx
'use client';

interface Agent {
  agent_id: string;
  agent_name: string;
  agent_type: string;
  color: { r: number; g: number; b: number };
  current_state: {
    status: string;
    position: { x: number; y: number };
  };
  performance: {
    tasks_completed: number;
    success_rate: number;
    avg_completion_time_ms: number;
  };
}

interface AgentCardProps {
  agent: Agent;
}

export function AgentCard({ agent }: AgentCardProps) {
  const statusColors = {
    idle: 'bg-gray-200 text-gray-700',
    navigating: 'bg-blue-200 text-blue-700',
    completed: 'bg-green-200 text-green-700',
    failed: 'bg-red-200 text-red-700',
  };

  const statusColor = statusColors[agent.current_state.status as keyof typeof statusColors] || statusColors.idle;
  const agentColor = `rgb(${agent.color.r}, ${agent.color.g}, ${agent.color.b})`;

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm p-5 hover:shadow-md transition-shadow">
      {/* Agent Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {/* Agent Color Indicator */}
          <div
            className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg"
            style={{ backgroundColor: agentColor }}
          >
            {agent.agent_name.charAt(0)}
          </div>
          <div>
            <h3 className="font-semibold text-slate-900">{agent.agent_name}</h3>
            <p className="text-sm text-slate-600 capitalize">{agent.agent_type}</p>
          </div>
        </div>

        {/* Status Badge */}
        <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${statusColor}`}>
          {agent.current_state.status}
        </span>
      </div>

      {/* Position Info */}
      <div className="mb-4 p-3 bg-slate-50 rounded-lg">
        <p className="text-xs text-slate-600 mb-1">Current Position</p>
        <p className="text-sm font-mono text-slate-900">
          ({agent.current_state.position.x}, {agent.current_state.position.y})
        </p>
      </div>

      {/* Performance Stats */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <p className="text-xs text-slate-600 mb-1">Tasks</p>
          <p className="text-lg font-bold text-slate-900">{agent.performance.tasks_completed}</p>
        </div>
        <div>
          <p className="text-xs text-slate-600 mb-1">Success Rate</p>
          <p className="text-lg font-bold text-slate-900">
            {(agent.performance.success_rate * 100).toFixed(0)}%
          </p>
        </div>
        <div className="col-span-2">
          <p className="text-xs text-slate-600 mb-1">Avg Time</p>
          <p className="text-sm font-medium text-slate-900">
            {agent.performance.avg_completion_time_ms > 0
              ? `${(agent.performance.avg_completion_time_ms / 1000).toFixed(2)}s`
              : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  );
}
