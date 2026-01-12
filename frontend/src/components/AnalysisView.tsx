import { useEffect, useRef, useState } from 'react';
import { useAnalysisStream } from '../hooks/useAnalysisStream';
import { AnalysisResults } from './AnalysisResults';
import { AnalysisStatus } from './AnalysisStatus';
import { AnalysisDetail } from '../hooks/useAnalysis';
import api from '../services/api';

interface AnalysisViewProps {
  analysisId: number;
}

export const AnalysisView = ({ analysisId }: AnalysisViewProps) => {
  const [analysis, setAnalysis] = useState<AnalysisDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Only connect to stream if analysis is not already completed
  const { status: streamStatus } = useAnalysisStream(
    analysis && analysis.status !== 'completed' ? analysisId : null
  );
  const hasRefetchedRef = useRef(false);

  // Fetch analysis data
  useEffect(() => {
    const fetchAnalysis = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get(`/api/analyses/${analysisId}`);
        setAnalysis(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch analysis');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [analysisId]);

  // Refetch analysis when stream indicates completion (if not already completed in DB)
  useEffect(() => {
    if (streamStatus.currentStep === 'completed' && 
        !hasRefetchedRef.current && 
        analysis && 
        analysis.status !== 'completed') {
      hasRefetchedRef.current = true;
      // Refetch after a short delay to ensure backend has saved the data
      const timer = setTimeout(async () => {
        try {
          const response = await api.get(`/api/analyses/${analysisId}`);
          setAnalysis(response.data);
        } catch (err: any) {
          console.error('Error refetching analysis:', err);
        }
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [streamStatus.currentStep, analysis?.status, analysisId]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">Loading analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  if (!analysis) {
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
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Analysis Not Found</h3>
          <p className="text-gray-500 text-sm mb-4">
            The analysis you're looking for doesn't exist or you don't have permission to view it.
          </p>
          <p className="text-gray-400 text-xs">
            It may have been deleted or the link may be incorrect.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          {analysis.company_name}
        </h1>
        <p className="text-sm text-gray-600">
          Created: {new Date(analysis.created_at).toLocaleString()}
        </p>
      </div>

      {analysis.status === 'processing' || analysis.status === 'pending' ? (
        <AnalysisStatus analysisId={analysisId} />
      ) : analysis.status === 'completed' ? (
        <AnalysisResults analysis={analysis} />
      ) : (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Analysis failed. Please try again.</p>
        </div>
      )}
    </div>
  );
};

