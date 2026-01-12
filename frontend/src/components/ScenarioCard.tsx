import { useState } from 'react';
import { StrategyCard } from './StrategyCard';
import { MarkdownRenderer } from './MarkdownRenderer';
import { Scenario, Strategy } from '../hooks/useAnalysis';

interface ScenarioCardProps {
  scenario: Scenario;
  strategies: Strategy[];
}

export const ScenarioCard = ({ scenario, strategies }: ScenarioCardProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-primary-500">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-800 mb-2">{scenario.title}</h3>
          {scenario.likelihood && (
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm text-gray-600">Likelihood:</span>
              <span className="text-sm font-semibold text-primary-600">
                {(scenario.likelihood * 100).toFixed(0)}%
              </span>
            </div>
          )}
          {scenario.timeline && (
            <p className="text-sm text-gray-600 mb-2">
              <span className="font-semibold">Timeline:</span> {scenario.timeline}
            </p>
          )}
        </div>
      </div>

      <div className="mb-4">
        <MarkdownRenderer content={scenario.description} />
      </div>

      {scenario.key_assumptions && (
        <div className="mb-4">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            {isExpanded ? 'Hide' : 'Show'} Key Assumptions
          </button>
          {isExpanded && (
            <div className="mt-2 p-3 bg-gray-50 rounded">
              <MarkdownRenderer content={scenario.key_assumptions} className="text-sm" />
            </div>
          )}
        </div>
      )}

      {strategies.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h4 className="text-lg font-semibold text-gray-800 mb-4">
            Strategic Recommendations ({strategies.length})
          </h4>
          <div className="space-y-4">
            {strategies.map((strategy) => (
              <StrategyCard key={strategy.id} strategy={strategy} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

