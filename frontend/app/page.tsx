'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { SkillLibrary } from '@/components/SkillLibrary';
import { ActivityFeed } from '@/components/ActivityFeed';
import { PerformanceChart } from '@/components/PerformanceChart';
import { AgentCard } from '@/components/AgentCard';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useKeepAlive } from '@/lib/use-keep-alive';

// Hardcoded backend URLs - production | local
const API_URL =
  typeof window !== 'undefined' && window.location.hostname !== 'localhost'
    ? 'https://mongodb-hackathon.onrender.com'
    : 'http://localhost:8000';

const WS_URL = API_URL.replace('http', 'ws') + '/ws';

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

interface Skill {
  skill_id: string;
  name: string;
  description: string;
  metadata: {
    author_agent: string;
    skill_type: string;
    maze_type: string;
    tags: string[];
  };
  stats: {
    success_rate: number;
    total_uses: number;
    improvement_over_baseline: number;
    avg_completion_time_ms: number;
  };
}

export default function Dashboard() {
  const { isConnected, messages, clearMessages } = useWebSocket(WS_URL);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [demoRunning, setDemoRunning] = useState(false);

  // Keep the backend alive
  useKeepAlive(API_URL, true, 14);

  // Fetch initial data
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setIsLoading(true);

      // Fetch agents
      const agentsRes = await fetch(`${API_URL}/api/agents`);
      const agentsData = await agentsRes.json();
      setAgents(agentsData.agents || []);

      // Fetch skills
      const skillsRes = await fetch(`${API_URL}/api/skills?limit=20`);
      const skillsData = await skillsRes.json();
      setSkills(skillsData.skills || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const createDemoAgents = async () => {
    const agentConfigs = [
      { name: 'Agent Alpha', type: 'explorer', color: { r: 255, g: 100, b: 100 } },
      { name: 'Agent Beta', type: 'learner', color: { r: 100, g: 100, b: 255 } },
      { name: 'Agent Gamma', type: 'optimizer', color: { r: 100, g: 255, b: 100 } },
    ];

    for (const config of agentConfigs) {
      try {
        await fetch(`${API_URL}/api/agents/create`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            agent_name: config.name,
            agent_type: config.type,
            color: config.color,
          }),
        });
      } catch (error) {
        console.error('Error creating agent:', error);
      }
    }

    await fetchData();
  };

  const startDemo = async () => {
    try {
      setDemoRunning(true);
      clearMessages();

      // Create agents if they don't exist
      if (agents.length === 0) {
        await createDemoAgents();
      }

      // For now, just simulate - full integration with simulation_simple.py coming
      console.log('🎬 Demo would start here - integrate with backend/simulation_simple.py');

      // You can add a backend endpoint to trigger the simulation
      // await fetch(`${API_URL}/api/demo/start`, { method: 'POST' });

      setDemoRunning(false);
    } catch (error) {
      console.error('Error starting demo:', error);
      setDemoRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">MirrorMinds</h1>
              <p className="text-sm text-slate-600 mt-1">
                Multi-Agent Procedural Memory System
              </p>
            </div>

            <div className="flex items-center gap-4">
              {/* Connection Status */}
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-sm text-slate-600">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>

              {/* Start Demo Button */}
              <Button
                onClick={startDemo}
                disabled={demoRunning || isLoading}
                size="lg"
                className="bg-blue-600 hover:bg-blue-700"
              >
                {demoRunning ? 'Demo Running...' : 'Start Demo'}
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
            <p className="mt-4 text-slate-600">Loading MirrorMinds...</p>
          </div>
        )}

        {!isLoading && (
          <div className="space-y-6">
            {/* Agent Cards Row */}
            <div>
              <h2 className="text-xl font-semibold text-slate-900 mb-4">Active Agents</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {agents.length > 0 ? (
                  agents.map((agent) => <AgentCard key={agent.agent_id} agent={agent} />)
                ) : (
                  <div className="col-span-3 text-center py-8 bg-white rounded-lg border border-slate-200">
                    <p className="text-slate-600 mb-4">No agents yet.</p>
                    <Button onClick={createDemoAgents} variant="outline">
                      Create Demo Agents
                    </Button>
                  </div>
                )}
              </div>
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Skill Library (2 columns) */}
              <div className="lg:col-span-2">
                <SkillLibrary skills={skills} onRefresh={fetchData} />
              </div>

              {/* Activity Feed (1 column) */}
              <div className="lg:col-span-1">
                <ActivityFeed messages={messages} />
              </div>
            </div>

            {/* Performance Chart */}
            <div>
              <PerformanceChart agents={agents} />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto px-6 text-center text-sm text-slate-600">
          <p>MongoDB Agentic Memory Hackathon 2024 • Built with Next.js, FastAPI, and MongoDB Atlas</p>
        </div>
      </footer>
    </div>
  );
}
