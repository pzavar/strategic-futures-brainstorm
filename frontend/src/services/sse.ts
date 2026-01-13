const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SSEEvent {
  event: string;
  data: any;
}

export class SSEClient {
  private eventSource: EventSource | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private shouldReconnect = true;
  private isTerminalState = false;

  constructor(
    private url: string,
    private onMessage: (event: SSEEvent) => void,
    private onError?: (error: Event) => void,
    private onOpen?: () => void
  ) {}

  connect(): void {
    const fullUrl = `${API_URL}${this.url}`;

    this.eventSource = new EventSource(fullUrl);

    this.eventSource.onopen = () => {
      this.reconnectAttempts = 0;
      if (this.onOpen) {
        this.onOpen();
      }
    };

    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'message',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE message:', error);
      }
    };

    // Handle custom events
    this.eventSource.addEventListener('status', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'status',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE status:', error);
      }
    });

    this.eventSource.addEventListener('research_start', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'research_start',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE research_start:', error);
      }
    });

    this.eventSource.addEventListener('research_complete', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'research_complete',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE research_complete:', error);
      }
    });

    this.eventSource.addEventListener('scenarios_start', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'scenarios_start',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE scenarios_start:', error);
      }
    });

    this.eventSource.addEventListener('scenarios_complete', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'scenarios_complete',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE scenarios_complete:', error);
      }
    });

    this.eventSource.addEventListener('strategies_start', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'strategies_start',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE strategies_start:', error);
      }
    });

    this.eventSource.addEventListener('strategies_complete', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'strategies_complete',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE strategies_complete:', error);
      }
    });

    this.eventSource.addEventListener('analysis_complete', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.isTerminalState = true;
        this.shouldReconnect = false;
        this.onMessage({
          event: 'analysis_complete',
          data,
        });
        // Close connection after completion
        this.disconnect();
      } catch (error) {
        console.error('Error parsing SSE analysis_complete:', error);
      }
    });

    this.eventSource.addEventListener('analysis_start', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'analysis_start',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE analysis_start:', error);
      }
    });

    this.eventSource.addEventListener('analysis_failed', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.isTerminalState = true;
        this.shouldReconnect = false;
        this.onMessage({
          event: 'analysis_failed',
          data,
        });
        // Close connection after failure
        this.disconnect();
      } catch (error) {
        console.error('Error parsing SSE analysis_failed:', error);
      }
    });

    this.eventSource.addEventListener('strategy_progress', (event: any) => {
      try {
        const data = JSON.parse(event.data);
        this.onMessage({
          event: 'strategy_progress',
          data,
        });
      } catch (error) {
        console.error('Error parsing SSE strategy_progress:', error);
      }
    });

    this.eventSource.onerror = (error) => {
      console.log('[SSE] Error event received', {
        readyState: this.eventSource?.readyState,
        isTerminalState: this.isTerminalState,
        shouldReconnect: this.shouldReconnect,
        reconnectAttempts: this.reconnectAttempts
      });

      // Don't reconnect if we're in a terminal state (completed/failed)
      if (this.isTerminalState || !this.shouldReconnect) {
        console.log('[SSE] Terminal state reached, not reconnecting');
        if (this.onError) {
          this.onError(error);
        }
        return;
      }

      // If connection is closed (readyState === 2), it might be intentional (analysis completed)
      // Only reconnect if we haven't received a completion event
      if (this.eventSource?.readyState === EventSource.CLOSED) {
        // Don't reconnect if connection was closed normally (after completion)
        // The onError will be called, but we won't spam reconnection attempts
        if (this.onError) {
          this.onError(error);
        }
      } else if (this.eventSource?.readyState === EventSource.CONNECTING) {
        // Still connecting, might be a temporary issue
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          console.log(`[SSE] Reconnecting (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
          setTimeout(() => {
            if (this.shouldReconnect && !this.isTerminalState) {
              this.connect();
            }
          }, this.reconnectDelay * this.reconnectAttempts);
        } else {
          console.log('[SSE] Max reconnection attempts reached');
          if (this.onError) {
            this.onError(error);
          }
        }
      } else {
        // Other error states
        if (this.onError) {
          this.onError(error);
        }
      }
    };
  }

  disconnect(): void {
    console.log('[SSE] Disconnecting');
    this.shouldReconnect = false;
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}

