import { useAnalyses, Analysis } from '../hooks/useAnalysis';
import { Link } from 'react-router-dom';

export const AnalysisHistory = () => {
  const { analyses, loading, error } = useAnalyses();

  if (loading) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Loading analyses...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
        <p className="text-red-800 font-medium">{error}</p>
        <p className="text-red-600 text-sm mt-2">Please try refreshing the page or contact support if the issue persists.</p>
      </div>
    );
  }

  if (analyses.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="max-w-md mx-auto">
          <div className="mb-4">
            <svg 
              className="mx-auto h-16 w-16 text-gray-400" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={1.5} 
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No analyses yet</h3>
          <p className="text-gray-500 text-sm mb-4">
            You haven't created any strategic futures analyses yet. Get started by creating your first analysis!
          </p>
          <p className="text-gray-400 text-xs">
            Analyses will appear here once you create them from the home page.
          </p>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      {analyses.map((analysis: Analysis) => (
        <Link
          key={analysis.id}
          to={`/analyses/${analysis.id}`}
          className="block bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-800">{analysis.company_name}</h3>
              <p className="text-sm text-gray-600 mt-1">
                Created: {new Date(analysis.created_at).toLocaleDateString()}
              </p>
            </div>
            <div className="flex items-center gap-4">
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
                  analysis.status
                )}`}
              >
                {analysis.status}
              </span>
              {analysis.status === 'completed' && (
                <span className="text-primary-600 font-medium">View →</span>
              )}
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
};

