// components/PerformanceChart.tsx
'use client';

interface Agent {
  agent_id: string;
  agent_name: string;
  agent_type: string;
  color: { r: number; g: number; b: number };
  performance: {
    tasks_completed: number;
    success_rate: number;
    avg_completion_time_ms: number;
  };
}

interface PerformanceChartProps {
  agents: Agent[];
}

export function PerformanceChart({ agents }: PerformanceChartProps) {
  // Calculate aggregate stats
  const totalTasks = agents.reduce((sum, agent) => sum + agent.performance.tasks_completed, 0);
  const avgSuccessRate = agents.length > 0
    ? agents.reduce((sum, agent) => sum + agent.performance.success_rate, 0) / agents.length
    : 0;

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-4 border-b border-slate-200 bg-slate-50">
        <h2 className="text-lg font-semibold text-slate-900">Performance Metrics</h2>
        <p className="text-sm text-slate-600 mt-1">System-wide performance overview</p>
      </div>

      <div className="p-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <p className="text-sm font-medium text-blue-700 mb-1">Total Agents</p>
            <p className="text-3xl font-bold text-blue-900">{agents.length}</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4 border border-green-200">
            <p className="text-sm font-medium text-green-700 mb-1">Total Tasks</p>
            <p className="text-3xl font-bold text-green-900">{totalTasks}</p>
          </div>
          <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
            <p className="text-sm font-medium text-purple-700 mb-1">Avg Success Rate</p>
            <p className="text-3xl font-bold text-purple-900">{(avgSuccessRate * 100).toFixed(1)}%</p>
          </div>
        </div>

        {/* Agent Comparison */}
        {agents.length > 0 && (
          <div>
            <h3 className="font-semibold text-slate-900 mb-3">Agent Comparison</h3>
            <div className="space-y-3">
              {agents.map((agent) => {
                const agentColor = `rgb(${agent.color.r}, ${agent.color.g}, ${agent.color.b})`;
                const successPercentage = agent.performance.success_rate * 100;

                return (
                  <div key={agent.agent_id} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: agentColor }}
                        />
                        <span className="text-sm font-medium text-slate-900">{agent.agent_name}</span>
                      </div>
                      <span className="text-sm text-slate-600">
                        {successPercentage.toFixed(0)}% • {agent.performance.tasks_completed} tasks
                      </span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-2">
                      <div
                        className="h-2 rounded-full transition-all duration-500"
                        style={{
                          width: `${successPercentage}%`,
                          backgroundColor: agentColor,
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {agents.length === 0 && (
          <div className="text-center py-12">
            <p className="text-slate-500 text-sm">No agents to display. Create agents to see performance metrics.</p>
          </div>
        )}
      </div>
    </div>
  );
}
