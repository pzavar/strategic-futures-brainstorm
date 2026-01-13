import { useState, useEffect, useRef } from 'react';
import { SSEClient, SSEEvent } from '../services/sse';

export interface StreamStatus {
  currentStep: string;
  message: string;
  progress: number;
}

export const useAnalysisStream = (analysisId: number | null) => {
  const [status, setStatus] = useState<StreamStatus>({
    currentStep: 'idle',
    message: '',
    progress: 0,
  });
  const [error, setError] = useState<string | null>(null);
  const clientRef = useRef<SSEClient | null>(null);
  const lastEventTimeRef = useRef<number>(Date.now());
  const statusPollIntervalRef = useRef<number | null>(null);
  const currentStepRef = useRef<string>('idle');

  useEffect(() => {
    if (!analysisId) {
      return;
    }

    // Fallback: Poll status if no events received for 15 seconds
    const startStatusPolling = () => {
      if (statusPollIntervalRef.current) {
        clearInterval(statusPollIntervalRef.current);
      }
      
      statusPollIntervalRef.current = window.setInterval(async () => {
        const timeSinceLastEvent = Date.now() - lastEventTimeRef.current;
        const currentStep = currentStepRef.current;
        // Only poll if no events received for 15 seconds and analysis is in progress
        if (timeSinceLastEvent > 15000 && (currentStep === 'processing' || currentStep === 'research' || currentStep === 'scenarios' || currentStep === 'strategies' || currentStep === 'initializing')) {
          try {
            const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/analyses/${analysisId}/status`);
            if (response.ok) {
              const analysis = await response.json();
              if (analysis.status === 'completed') {
                currentStepRef.current = 'completed';
                setStatus({
                  currentStep: 'completed',
                  message: 'Analysis completed successfully!',
                  progress: 100,
                });
                if (statusPollIntervalRef.current) {
                  clearInterval(statusPollIntervalRef.current);
                  statusPollIntervalRef.current = null;
                }
              } else if (analysis.status === 'failed') {
                currentStepRef.current = 'failed';
                setStatus({
                  currentStep: 'failed',
                  message: 'Analysis failed',
                  progress: 0,
                });
                setError('Analysis failed');
                if (statusPollIntervalRef.current) {
                  clearInterval(statusPollIntervalRef.current);
                  statusPollIntervalRef.current = null;
                }
              }
            }
          } catch (err) {
            console.error('Error polling analysis status:', err);
          }
        }
      }, 5000); // Check every 5 seconds
    };

    const client = new SSEClient(
      `/api/analyses/${analysisId}/stream`,
      (event: SSEEvent) => {
        lastEventTimeRef.current = Date.now(); // Update last event time
        const { event: eventType, data } = event;
        
        console.log(`[SSE] Received event: ${eventType}`, data);

        switch (eventType) {
          case 'status':
            // Check if analysis is already completed or failed
            if (data.status === 'completed') {
              currentStepRef.current = 'completed';
              setStatus({
                currentStep: 'completed',
                message: 'Analysis completed successfully!',
                progress: 100,
              });
              // Stop polling and disconnect
              if (statusPollIntervalRef.current) {
                clearInterval(statusPollIntervalRef.current);
                statusPollIntervalRef.current = null;
              }
              if (clientRef.current) {
                clientRef.current.disconnect();
              }
            } else if (data.status === 'failed') {
              currentStepRef.current = 'failed';
              setStatus({
                currentStep: 'failed',
                message: data.message || 'Analysis failed',
                progress: 0,
              });
              setError(data.message || 'Analysis failed');
              // Stop polling and disconnect
              if (statusPollIntervalRef.current) {
                clearInterval(statusPollIntervalRef.current);
                statusPollIntervalRef.current = null;
              }
              if (clientRef.current) {
                clientRef.current.disconnect();
              }
            } else if (data.status === 'processing') {
              currentStepRef.current = 'processing';
              setStatus({
                currentStep: 'processing',
                message: data.message || 'Analysis in progress...',
                progress: 10,
              });
            } else {
              currentStepRef.current = 'connected';
              setStatus({
                currentStep: 'connected',
                message: data.message || 'Connected',
                progress: 0,
              });
            }
            break;

          case 'research_start':
            currentStepRef.current = 'research';
            setStatus({
              currentStep: 'research',
              message: 'Researching company information...',
              progress: 10,
            });
            break;

          case 'research_complete':
            currentStepRef.current = 'research';
            setStatus({
              currentStep: 'research',
              message: 'Research completed',
              progress: 30,
            });
            break;

          case 'scenarios_start':
            currentStepRef.current = 'scenarios';
            setStatus({
              currentStep: 'scenarios',
              message: 'Generating future scenarios...',
              progress: 40,
            });
            break;

          case 'scenarios_complete':
            currentStepRef.current = 'scenarios';
            setStatus({
              currentStep: 'scenarios',
              message: 'Scenarios generated',
              progress: 60,
            });
            break;

          case 'strategies_start':
            currentStepRef.current = 'strategies';
            setStatus({
              currentStep: 'strategies',
              message: 'Generating strategic recommendations...',
              progress: 70,
            });
            break;

          case 'strategies_complete':
            currentStepRef.current = 'strategies';
            setStatus({
              currentStep: 'strategies',
              message: 'Strategies generated',
              progress: 90,
            });
            break;

          case 'analysis_complete':
            currentStepRef.current = 'completed';
            setStatus({
              currentStep: 'completed',
              message: 'Analysis completed successfully!',
              progress: 100,
            });
            if (statusPollIntervalRef.current) {
              clearInterval(statusPollIntervalRef.current);
              statusPollIntervalRef.current = null;
            }
            break;

          case 'analysis_start':
            currentStepRef.current = 'initializing';
            setStatus({
              currentStep: 'initializing',
              message: data.message || 'Starting analysis...',
              progress: 5,
            });
            break;

          case 'analysis_failed':
            currentStepRef.current = 'failed';
            setStatus({
              currentStep: 'failed',
              message: data.message || 'Analysis failed',
              progress: 0,
            });
            setError(data.message || 'Analysis failed');
            if (statusPollIntervalRef.current) {
              clearInterval(statusPollIntervalRef.current);
              statusPollIntervalRef.current = null;
            }
            break;

          case 'strategy_progress':
            // Update message but keep current progress
            setStatus((prev) => ({
              ...prev,
              message: data.message || prev.message,
            }));
            break;

          default:
            if (data.message) {
              setStatus((prev) => ({
                ...prev,
                message: data.message,
              }));
            }
        }
      },
      (err) => {
        setError('Connection error');
        console.error(`[SSE] Connection error for analysis ${analysisId}:`, err);
      },
      () => {
        console.log(`[SSE] Connected to stream for analysis ${analysisId}`);
        lastEventTimeRef.current = Date.now();
      }
    );

    clientRef.current = client;
    client.connect();
    startStatusPolling();

    return () => {
      if (clientRef.current) {
        clientRef.current.disconnect();
      }
      if (statusPollIntervalRef.current) {
        clearInterval(statusPollIntervalRef.current);
        statusPollIntervalRef.current = null;
      }
    };
  }, [analysisId]);

  return { status, error };
};

