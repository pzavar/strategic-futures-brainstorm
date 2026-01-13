import { AnalysisHistory } from '../components/AnalysisHistory';

export const History = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analysis History</h1>
          <p className="text-gray-600">View and manage completed strategic analyses</p>
        </div>
        <AnalysisHistory />
      </div>
    </div>
  );
};

