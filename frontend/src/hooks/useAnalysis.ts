import { useState, useEffect } from 'react';
import api from '../services/api';

export interface Analysis {
  id: number;
  company_name: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  company_context?: string;
  created_at: string;
  updated_at: string;
}

export interface Scenario {
  id: number;
  scenario_number: number;
  title: string;
  description: string;
  timeline?: string;
  key_assumptions?: string;
  likelihood?: number;
}

export interface Strategy {
  id: number;
  name: string;
  description: string;
  expected_impact?: string;
  key_risks?: string;
}

export interface AnalysisDetail extends Analysis {
  scenarios: Scenario[];
  strategies: Record<string, Strategy[]>;
}

export const useAnalysis = (analysisId: number | null) => {
  const [analysis, setAnalysis] = useState<AnalysisDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!analysisId) {
      setAnalysis(null);
      return;
    }

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

  return { analysis, loading, error };
};

export const useAnalyses = () => {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalyses = async () => {
      setLoading(true);
      setError(null);
      try {
        console.log('[useAnalyses] Fetching analyses from /api/analyses');
        const response = await api.get('/api/analyses');
        console.log('[useAnalyses] Received response:', response.data);
        const analysesData = response.data || [];
        console.log(`[useAnalyses] Setting ${analysesData.length} analyses`);
        setAnalyses(analysesData);
      } catch (err: any) {
        console.error('[useAnalyses] Error fetching analyses:', err);
        console.error('[useAnalyses] Error details:', {
          message: err.message,
          response: err.response?.data,
          status: err.response?.status,
          statusText: err.response?.statusText
        });
        // Handle 404 or other errors more gracefully
        if (err.response?.status === 404) {
          // If endpoint doesn't exist, treat as empty list (analyses feature may not be available)
          console.warn('[useAnalyses] 404 - Endpoint not found, treating as empty list');
          setAnalyses([]);
          setError(null);
        } else {
          const errorMsg = err.response?.data?.detail || err.message || 'Unable to load analyses. Please try again later.';
          console.error('[useAnalyses] Setting error:', errorMsg);
          setError(errorMsg);
        }
      } finally {
        setLoading(false);
        console.log('[useAnalyses] Loading complete');
      }
    };

    fetchAnalyses();
  }, []);

  return { analyses, loading, error, refetch: () => {
    const fetchAnalyses = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get('/api/analyses');
        setAnalyses(response.data || []);
      } catch (err: any) {
        // Handle 404 or other errors more gracefully
        if (err.response?.status === 404) {
          // If endpoint doesn't exist, treat as empty list (analyses feature may not be available)
          setAnalyses([]);
          setError(null);
        } else {
          setError(err.response?.data?.detail || 'Unable to load analyses. Please try again later.');
        }
      } finally {
        setLoading(false);
      }
    };
    fetchAnalyses();
  }};
};

export const createAnalysis = async (companyName: string): Promise<Analysis> => {
  try {
    const response = await api.post('/api/analyses', { company_name: companyName });
    return response.data;
  } catch (error: any) {
    // Enhanced error logging
    console.error('Create analysis error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      statusText: error.response?.statusText,
      request: error.request,
      fullError: error
    });
    
    // Re-throw with more context
    if (error.response?.status === 404) {
      throw new Error('Analysis feature is currently unavailable. The endpoint was not found.');
    } else if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    } else if (error.message) {
      throw new Error(error.message);
    } else {
      throw new Error('Failed to create analysis. Please try again later.');
    }
  }
};

