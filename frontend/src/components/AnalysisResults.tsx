import { ScenarioCard } from './ScenarioCard';
import { MarkdownRenderer } from './MarkdownRenderer';
import { AnalysisDetail } from '../hooks/useAnalysis';

interface AnalysisResultsProps {
  analysis: AnalysisDetail;
}

export const AnalysisResults = ({ analysis }: AnalysisResultsProps) => {
  if (analysis.status !== 'completed') {
    return null;
  }

  return (
    <div className="space-y-8">
      {analysis.company_context && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Company Context</h2>
          <MarkdownRenderer content={analysis.company_context} />
        </div>
      )}

      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Future Scenarios</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {analysis.scenarios.map((scenario) => (
            <ScenarioCard
              key={scenario.id}
              scenario={scenario}
              strategies={analysis.strategies[scenario.title] || []}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

