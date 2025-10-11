'use client';

import { useEffect, useState } from 'react';

interface Position {
  x: number;
  y: number;
}

interface AgentState {
  id: string;
  name: string;
  position: Position;
  path: Position[];
  color: string;
  status: 'idle' | 'navigating' | 'completed';
  strategy: string;
  time?: number;
  steps?: number;
}

interface DemoPhase {
  current: string;
  message: string;
  step: number; // 1: Alpha exploring, 2: Skill extraction, 3: Beta learning, 4: Complete
}

interface ComparisonResult {
  agentA: { name: string; time: number; steps: number; strategy: string };
  agentB: { name: string; time: number; steps: number; strategy: string };
  improvement: number;
}

interface SkillData {
  skill_id: string;
  name: string;
  description: string;
  path_length: number;
  from_agent: string;
}

interface MazeVisualizationProps {
  messages: any[];
}

export function MazeVisualization({ messages }: MazeVisualizationProps) {
  const [maze, setMaze] = useState<number[][]>([]);
  const [agents, setAgents] = useState<Map<string, AgentState>>(new Map());
  const [demoActive, setDemoActive] = useState(false);
  const [demoPhase, setDemoPhase] = useState<DemoPhase>({ current: 'idle', message: '', step: 0 });
  const [comparison, setComparison] = useState<ComparisonResult | null>(null);
  const [skillExtracted, setSkillExtracted] = useState(false);
  const [skillTransfer, setSkillTransfer] = useState(false);
  const [skillData, setSkillData] = useState<SkillData | null>(null);

  // Default Labyrinth Challenge maze (15x15)
  useEffect(() => {
    const defaultMaze = [
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
      [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
      [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
      [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
      [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
      [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
      [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
      [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ];
    setMaze(defaultMaze);
  }, []);

  // Track last processed message index to avoid reprocessing
  const [lastProcessedIndex, setLastProcessedIndex] = useState(-1);

  // Process WebSocket messages to update agent positions
  useEffect(() => {
    if (!messages.length) return;

    // Process ALL new messages since last check (not just the latest one!)
    const newMessages = messages.slice(lastProcessedIndex + 1);

    newMessages.forEach((message) => {
      processMessage(message);
    });

    setLastProcessedIndex(messages.length - 1);
  }, [messages]);

  const processMessage = (latestMessage: any) => {
    switch (latestMessage.type) {
      case 'demo_starting':
        setDemoActive(true);
        setAgents(new Map());
        setComparison(null);
        setSkillExtracted(false);
        setSkillTransfer(false);
        setSkillData(null);
        setDemoPhase({ current: 'starting', message: 'Demo starting...', step: 0 });
        break;

      case 'agent_start':
        const agentId = latestMessage.data.agent_id;
        const agentName = latestMessage.data.agent_name;
        const strategy = latestMessage.data.strategy;

        console.log('🚀 Agent started:', { agentId, agentName, strategy });

        const isAlpha = agentId === 'agent_alpha';
        setDemoPhase({
          current: 'agent_navigating',
          message: `${agentName} is ${strategy === 'random_exploration' ? 'exploring randomly' : 'using learned skill'}...`,
          step: isAlpha ? 1 : 3
        });

        setAgents(prev => {
          const newAgents = new Map(prev);
          newAgents.set(agentId, {
            id: agentId,
            name: agentName,
            position: { x: 1, y: 1 }, // spawn point
            path: [{ x: 1, y: 1 }],
            color: agentId === 'agent_alpha' ? '#ff6464' : '#6464ff',
            status: 'navigating',
            strategy: strategy,
          });
          console.log('✅ Agent added to map. Total agents:', newAgents.size);
          return newAgents;
        });
        break;

      case 'agent_position':
        const posAgentId = latestMessage.data.agent_id;
        const position = latestMessage.data.position;

        setAgents(prev => {
          const newAgents = new Map(prev);
          const agent = newAgents.get(posAgentId);
          if (agent) {
            agent.position = position;
            agent.path.push(position);
            newAgents.set(posAgentId, agent);
            // Log every 10th position update to avoid spam
            if (agent.path.length % 10 === 0) {
              console.log(`📍 Agent ${posAgentId} at (${position.x}, ${position.y}) - ${agent.path.length} steps`);
            }
          } else {
            console.warn(`⚠️ Agent ${posAgentId} not found in map when updating position`);
          }
          return newAgents;
        });
        break;

      case 'agent_completed':
        const completedId = latestMessage.data.agent_id;

        setAgents(prev => {
          const newAgents = new Map(prev);
          const agent = newAgents.get(completedId);
          if (agent) {
            agent.status = 'completed';
            agent.time = latestMessage.data.completion_time;
            agent.steps = latestMessage.data.steps;
            newAgents.set(completedId, agent);
          }
          return newAgents;
        });
        break;

      case 'skill_extracted':
        // Phase 2: Skill extracted and saved to MongoDB (don't show card yet)
        setSkillExtracted(true);
        setDemoPhase({
          current: 'skill_extraction',
          message: `Skill extracted and saved to MongoDB! Ready for Agent Beta to retrieve it.`,
          step: 2
        });
        setTimeout(() => setSkillExtracted(false), 2000);
        break;

      case 'skill_retrieved':
        // Phase 3: Agent Beta retrieves skill from MongoDB (NOW show the card!)
        setSkillData({
          skill_id: `skill_${Date.now()}`,
          name: latestMessage.data.skill_name || 'Maze Navigation Strategy',
          description: latestMessage.data.description || `Learned navigation pattern from ${latestMessage.data.from_agent}`,
          path_length: latestMessage.data.path_length,
          from_agent: latestMessage.data.from_agent
        });
        setDemoPhase({
          current: 'skill_retrieval',
          message: `${latestMessage.data.agent_name} retrieved skill from MongoDB via Vector Search!`,
          step: 3
        });
        break;

      case 'skill_transfer':
        setSkillTransfer(true);
        setDemoPhase({
          current: 'skill_transfer',
          message: `Transferring skill to ${latestMessage.data.to_agent}...`,
          step: 3
        });
        setTimeout(() => setSkillTransfer(false), 2000);
        break;

      case 'demo_complete':
        const data = latestMessage.data;
        setComparison({
          agentA: data.agent_a,
          agentB: data.agent_b,
          improvement: data.improvement_percentage
        });
        setDemoPhase({
          current: 'complete',
          message: `Demo complete! Agent Beta was ${data.improvement_percentage.toFixed(1)}% faster!`,
          step: 4
        });
        setTimeout(() => setDemoActive(false), 5000);
        break;
    }
  };

  const cellSize = 35;  // Smaller cells for larger maze
  const gridWidth = maze[0]?.length || 15;
  const gridHeight = maze.length || 15;

  const getPhaseLabel = (step: number) => {
    switch (step) {
      case 0: return 'Idle';
      case 1: return 'Phase 1: Agent Alpha Exploring';
      case 2: return 'Phase 2: Skill Extraction';
      case 3: return 'Phase 3: Agent Beta Learning';
      case 4: return 'Phase 4: Complete';
      default: return 'Unknown';
    }
  };

  const getPhaseColor = (step: number) => {
    switch (step) {
      case 1: return 'bg-red-100 border-red-400 text-red-800';
      case 2: return 'bg-yellow-100 border-yellow-400 text-yellow-800';
      case 3: return 'bg-blue-100 border-blue-400 text-blue-800';
      case 4: return 'bg-green-100 border-green-400 text-green-800';
      default: return 'bg-slate-100 border-slate-400 text-slate-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
      <div className="space-y-4">
        {/* Phase Indicator */}
        {demoActive && (
          <div className={`px-4 py-3 rounded-lg border-2 font-semibold text-center ${getPhaseColor(demoPhase.step)}`}>
            <div className="flex items-center justify-center gap-2">
              <span className="text-lg">{getPhaseLabel(demoPhase.step)}</span>
              <span className="text-xs font-normal">({demoPhase.step}/4)</span>
            </div>
            <p className="text-xs font-normal mt-1">{demoPhase.message}</p>
          </div>
        )}

        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">Maze Navigation</h3>
            <p className="text-sm text-slate-600">
              {demoActive ? 'Demo in progress' : 'Waiting for demo to start'}
              {agents.size > 0 && (
                <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {agents.size} agent{agents.size !== 1 ? 's' : ''} active
                </span>
              )}
            </p>
          </div>

          {/* Legend */}
          <div className="flex gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-slate-800 border border-slate-400"></div>
              <span>Wall</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-white border border-slate-300"></div>
              <span>Path</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-400 border border-green-500"></div>
              <span>Goal</span>
            </div>
          </div>
        </div>

        {/* Skill Data Display - MongoDB Vector Search Result */}
        {skillData && demoPhase.step >= 3 && (
          <div className="p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border-2 border-purple-300">
            <div className="flex items-start gap-3">
              <div className="text-3xl">🧠</div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <h4 className="font-semibold text-purple-900">Skill Retrieved from MongoDB</h4>
                  <span className="text-xs bg-purple-200 text-purple-800 px-2 py-1 rounded-full">Vector Search</span>
                </div>
                <div className="text-sm space-y-1">
                  <p className="text-slate-700">
                    <span className="font-medium">Name:</span> {skillData.name}
                  </p>
                  <p className="text-slate-700">
                    <span className="font-medium">Description:</span> {skillData.description}
                  </p>
                  <p className="text-slate-700">
                    <span className="font-medium">Path Length:</span> {skillData.path_length} steps
                  </p>
                  <p className="text-slate-700">
                    <span className="font-medium">Author:</span> <span className="font-mono text-xs">{skillData.from_agent}</span>
                  </p>
                  <div className="mt-2 pt-2 border-t border-purple-200">
                    <p className="text-xs text-purple-700 font-medium">
                      ✨ Voyage AI embeddings enabled semantic search in MongoDB Atlas Vector Search
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Maze Grid */}
        <div className="flex justify-center bg-slate-50 p-8 rounded-lg">
          <div className="relative" style={{ width: cellSize * gridWidth, height: cellSize * gridHeight }}>
            {/* Draw maze grid */}
            {maze.map((row, y) =>
              row.map((cell, x) => {
                const isGoal = x === 13 && y === 13;
                const isSpawn = x === 1 && y === 1;

                return (
                  <div
                    key={`cell-${x}-${y}`}
                    className={`absolute border border-slate-300 ${cell === 1
                      ? 'bg-slate-800'
                      : isGoal
                        ? 'bg-green-400'
                        : isSpawn
                          ? 'bg-blue-100'
                          : 'bg-white'
                      }`}
                    style={{
                      left: x * cellSize,
                      top: y * cellSize,
                      width: cellSize,
                      height: cellSize,
                    }}
                  />
                );
              })
            )}

            {/* Draw agent paths */}
            {Array.from(agents.values()).map((agent) =>
              agent.path.map((pos, idx) => {
                // Fade trail from oldest to newest
                const opacity = 0.2 + (idx / agent.path.length) * 0.4;
                return (
                  <div
                    key={`path-${agent.id}-${idx}`}
                    className="absolute transition-opacity duration-500"
                    style={{
                      left: pos.x * cellSize + cellSize / 2 - 3,
                      top: pos.y * cellSize + cellSize / 2 - 3,
                      width: 6,
                      height: 6,
                      backgroundColor: agent.color,
                      opacity: opacity,
                      borderRadius: '50%',
                    }}
                  />
                );
              })
            )}

            {/* Draw agents */}
            {Array.from(agents.values()).map((agent) => (
              <div
                key={`agent-${agent.id}`}
                className={`absolute transition-all duration-150 ease-linear rounded-full border-3 border-white shadow-lg flex items-center justify-center font-bold text-white text-sm ${
                  agent.status === 'navigating' ? 'animate-pulse' : ''
                }`}
                style={{
                  left: agent.position.x * cellSize + cellSize / 2 - 16,
                  top: agent.position.y * cellSize + cellSize / 2 - 16,
                  width: 32,
                  height: 32,
                  backgroundColor: agent.color,
                  zIndex: 10,
                  boxShadow: agent.status === 'navigating'
                    ? `0 0 20px ${agent.color}`
                    : '0 4px 6px rgba(0,0,0,0.1)',
                }}
                title={agent.name}
              >
                {agent.id === 'agent_alpha' ? 'A' : 'B'}
              </div>
            ))}
          </div>
        </div>

        {/* Agent Stats */}
        {Array.from(agents.values()).length > 0 && (
          <div className="grid grid-cols-2 gap-4">
            {Array.from(agents.values()).map((agent) => (
              <div
                key={agent.id}
                className="p-4 rounded-lg border-2"
                style={{ borderColor: agent.color }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: agent.color }}
                  />
                  <span className="font-semibold">{agent.name}</span>
                  <span className="text-xs text-slate-600">
                    ({agent.strategy === 'random_exploration' ? 'Random' : 'Learned Skill'})
                  </span>
                </div>

                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-slate-600">Status:</span>
                    <span className="font-medium capitalize">{agent.status}</span>
                  </div>

                  {agent.time !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-slate-600">Time:</span>
                      <span className="font-medium">{agent.time.toFixed(2)}s</span>
                    </div>
                  )}

                  {agent.steps !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-slate-600">Steps:</span>
                      <span className="font-medium">{agent.steps}</span>
                    </div>
                  )}

                  <div className="flex justify-between">
                    <span className="text-slate-600">Position:</span>
                    <span className="font-mono text-xs">
                      ({agent.position.x}, {agent.position.y})
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Comparison Summary */}
        {comparison && (
          <div className="p-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border-2 border-green-400">
            <div className="text-center mb-4">
              <h4 className="text-xl font-bold text-slate-900">Demo Complete!</h4>
              <p className="text-sm text-slate-600 mt-1">Collective Intelligence in Action</p>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-4">
              {/* Agent Alpha */}
              <div className="bg-white p-4 rounded-lg border border-red-200">
                <div className="text-center">
                  <div className="text-xs text-slate-600 mb-1">Agent Alpha</div>
                  <div className="text-2xl font-bold text-red-600">{comparison.agentA.time.toFixed(2)}s</div>
                  <div className="text-xs text-slate-500">{comparison.agentA.steps} steps</div>
                  <div className="text-xs text-slate-500 mt-1">Random Exploration</div>
                </div>
              </div>

              {/* Improvement */}
              <div className="bg-gradient-to-br from-green-400 to-blue-400 p-4 rounded-lg flex flex-col items-center justify-center">
                <div className="text-white text-center">
                  <div className="text-3xl font-bold">{comparison.improvement.toFixed(1)}%</div>
                  <div className="text-sm mt-1">Faster!</div>
                </div>
              </div>

              {/* Agent Beta */}
              <div className="bg-white p-4 rounded-lg border border-blue-200">
                <div className="text-center">
                  <div className="text-xs text-slate-600 mb-1">Agent Beta</div>
                  <div className="text-2xl font-bold text-blue-600">{comparison.agentB.time.toFixed(2)}s</div>
                  <div className="text-xs text-slate-500">{comparison.agentB.steps} steps</div>
                  <div className="text-xs text-slate-500 mt-1">Learned Skill</div>
                </div>
              </div>
            </div>

            <div className="text-center text-sm text-slate-700">
              <p className="font-semibold">Agent Beta learned from Agent Alpha&apos;s experience!</p>
              <p className="text-xs mt-1">Skill stored in MongoDB with semantic embeddings via Voyage AI</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
