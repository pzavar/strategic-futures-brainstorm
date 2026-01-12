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
            Strategic Futures AI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Generate diverse future scenarios and strategic recommendations for any company
            using advanced AI research and analysis
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <CompanyInput onSubmit={handleSubmit} loading={loading} />
          
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

