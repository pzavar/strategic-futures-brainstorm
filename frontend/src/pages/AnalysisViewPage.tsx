import { useParams } from 'react-router-dom';
import { AnalysisView } from '../components/AnalysisView';

export const AnalysisViewPage = () => {
  const { id } = useParams<{ id: string }>();
  const analysisId = id ? parseInt(id, 10) : null;

  if (!analysisId) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Invalid analysis ID</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <AnalysisView analysisId={analysisId} />
      </div>
    </div>
  );
};

