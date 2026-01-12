import { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAnalysisStream } from '../hooks/useAnalysisStream';

interface AnalysisStatusProps {
  analysisId: number | null;
}

export const AnalysisStatus = ({ analysisId }: AnalysisStatusProps) => {
  const { status, error } = useAnalysisStream(analysisId);
  const navigate = useNavigate();
  const location = useLocation();
  const hasRedirectedRef = useRef(false);

  // Redirect to analysis view when completed (only if not already on that page)
  useEffect(() => {
    if (status.currentStep === 'completed' && analysisId && !hasRedirectedRef.current) {
      const isOnAnalysisPage = location.pathname === `/analyses/${analysisId}`;
      
      if (!isOnAnalysisPage) {
        hasRedirectedRef.current = true;
        // Small delay to show completion message, then redirect
        const timer = setTimeout(() => {
          navigate(`/analyses/${analysisId}`);
        }, 1500);
        return () => clearTimeout(timer);
      }
    }
  }, [status.currentStep, analysisId, navigate, location.pathname]);

  if (!analysisId) {
    return null;
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  const getStepLabel = (step: string) => {
    switch (step) {
      case 'research':
        return 'Research Phase';
      case 'scenarios':
        return 'Scenario Generation';
      case 'strategies':
        return 'Strategy Development';
      case 'processing':
        return 'Processing';
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      case 'connected':
        return 'Connected';
      default:
        return 'Initializing';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">
          {getStepLabel(status.currentStep)}
        </h3>
        <span className="text-sm text-gray-600">{status.progress}%</span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
        <div
          className="bg-primary-600 h-2.5 rounded-full transition-all duration-300"
          style={{ width: `${status.progress}%` }}
        />
      </div>
      
      <p className="text-sm text-gray-600">{status.message}</p>
    </div>
  );
};

