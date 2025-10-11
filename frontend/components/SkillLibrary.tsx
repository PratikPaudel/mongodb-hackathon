// components/SkillLibrary.tsx
'use client';

import { useState } from 'react';

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

interface SkillLibraryProps {
  skills: Skill[];
  onRefresh?: () => void;
}

export function SkillLibrary({ skills, onRefresh }: SkillLibraryProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('all');

  const skillTypes = ['all', 'navigation', 'pathfinding', 'optimization'];

  const filteredSkills = skills.filter((skill) => {
    const matchesSearch =
      skill.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      skill.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = selectedType === 'all' || skill.metadata.skill_type === selectedType;
    return matchesSearch && matchesType;
  });

  return (
    <div className="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-4 border-b border-slate-200 bg-slate-50">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Skill Library</h2>
            <p className="text-sm text-slate-600 mt-1">Shared procedural memory</p>
          </div>
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Refresh
            </button>
          )}
        </div>

        {/* Search */}
        <input
          type="text"
          placeholder="Search skills..."
          className="w-full px-4 py-2 border border-slate-300 rounded-lg mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />

        {/* Type Filter */}
        <div className="flex gap-2 flex-wrap">
          {skillTypes.map((type) => (
            <button
              key={type}
              onClick={() => setSelectedType(type)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                selectedType === type
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Skills Grid */}
      <div className="p-4 space-y-4 max-h-[600px] overflow-y-auto">
        {filteredSkills.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-slate-500 text-sm">
              {skills.length === 0 ? 'No skills yet. Run a demo to generate skills.' : 'No matching skills found.'}
            </p>
          </div>
        ) : (
          filteredSkills.map((skill) => (
            <div
              key={skill.skill_id}
              className="border border-slate-200 rounded-lg p-4 hover:shadow-md transition-all cursor-pointer hover:border-blue-300"
            >
              {/* Skill Header */}
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-slate-900">{skill.name}</h3>
                <div className="flex items-center gap-2">
                  {skill.stats.improvement_over_baseline > 0 && (
                    <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      +{(skill.stats.improvement_over_baseline * 100).toFixed(0)}% improvement
                    </span>
                  )}
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-700">
                    {(skill.stats.success_rate * 100).toFixed(0)}% success
                  </span>
                </div>
              </div>

              {/* Description */}
              <p className="text-sm text-slate-600 mb-3">{skill.description}</p>

              {/* Tags */}
              <div className="flex gap-2 flex-wrap mb-3">
                <span className="px-2 py-1 rounded-md text-xs font-medium bg-purple-100 text-purple-700">
                  {skill.metadata.maze_type}
                </span>
                {skill.metadata.tags.map((tag) => (
                  <span key={tag} className="px-2 py-1 rounded-md text-xs bg-slate-100 text-slate-700">
                    {tag}
                  </span>
                ))}
              </div>

              {/* Stats */}
              <div className="flex justify-between text-xs text-slate-500 pt-2 border-t border-slate-200">
                <span>
                  <span className="font-medium text-slate-700">{skill.stats.total_uses}</span> uses
                </span>
                <span>
                  By <span className="font-medium text-slate-700">{skill.metadata.author_agent}</span>
                </span>
                <span>
                  Avg: <span className="font-medium text-slate-700">
                    {(skill.stats.avg_completion_time_ms / 1000).toFixed(2)}s
                  </span>
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
