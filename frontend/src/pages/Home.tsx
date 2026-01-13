import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CompanyInput } from '../components/CompanyInput';
import { AnalysisStatus } from '../components/AnalysisStatus';
import { createAnalysis } from '../hooks/useAnalysis';

export const Home = () => {
  const [currentAnalysisId, setCurrentAnalysisId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (companyName: string) => {
    setLoading(true);
    try {
      const analysis = await createAnalysis(companyName);
      setCurrentAnalysisId(analysis.id);
      // Navigate to analysis view after a short delay
      setTimeout(() => {
        navigate(`/analyses/${analysis.id}`);
      }, 1000);
    } catch (error: any) {
      console.error('Error creating analysis:', error);
      // Provide more helpful error messages
      let errorMessage = 'Failed to create analysis. Please try again.';
      if (error.response?.status === 404) {
        errorMessage = 'Analysis feature is currently unavailable. Please contact support.';
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Strategic Futures Analysis
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Automated scenario-based strategic analysis for organizations
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <CompanyInput onSubmit={handleSubmit} loading={loading} />
          
          <div className="mt-4 flex items-center justify-center gap-6 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <span>125 S&P 500 companies</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span>Search by name, ticker, or fuzzy match</span>
            </div>
          </div>
          
          {currentAnalysisId && (
            <div className="mt-8">
              <AnalysisStatus analysisId={currentAnalysisId} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

