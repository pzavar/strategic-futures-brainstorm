import { MarkdownRenderer } from './MarkdownRenderer';
import { Strategy } from '../hooks/useAnalysis';

interface StrategyCardProps {
  strategy: Strategy;
}

export const StrategyCard = ({ strategy }: StrategyCardProps) => {
  return (
    <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
      <h5 className="text-md font-semibold text-gray-800 mb-2">{strategy.name}</h5>
      <div className="mb-3">
        <MarkdownRenderer content={strategy.description} className="text-sm" />
      </div>
      
      {strategy.expected_impact && (
        <div className="mb-3">
          <span className="text-xs font-semibold text-gray-600 uppercase">Expected Impact:</span>
          <div className="mt-1">
            <MarkdownRenderer content={strategy.expected_impact} className="text-sm" />
          </div>
        </div>
      )}
      
      {strategy.key_risks && (
        <div>
          <span className="text-xs font-semibold text-red-600 uppercase">Key Risks:</span>
          <div className="mt-1">
            <MarkdownRenderer content={strategy.key_risks} className="text-sm" />
          </div>
        </div>
      )}
    </div>
  );
};

