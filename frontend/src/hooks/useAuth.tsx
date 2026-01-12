import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../services/api';
import { setToken, removeToken, isAuthenticated } from '../services/auth';

interface AuthContextType {
  user: any | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated on mount
    if (isAuthenticated()) {
      // Token exists, but we don't have user info endpoint
      // For now, just set authenticated state
      setUser({ authenticated: true });
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post('/api/auth/login', { email, password });
      const { access_token } = response.data;
      setToken(access_token);
      setUser({ authenticated: true, email });
      window.location.href = '/app';
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const response = await api.post('/api/auth/register', { email, password });
      const { access_token } = response.data;
      setToken(access_token);
      setUser({ authenticated: true, email });
      window.location.href = '/app';
    } catch (error: any) {
      // Enhanced error logging
      console.error('Registration error:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        statusText: error.response?.statusText,
        request: error.request,
        fullError: error
      });
      
      // Extract error message
      let errorMessage = 'Registration failed';
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      } else if (error.request) {
        errorMessage = 'Unable to connect to server. Please ensure the backend is running.';
      }
      
      throw new Error(errorMessage);
    }
  };

  const logout = () => {
    removeToken();
    setUser(null);
    window.location.href = '/';
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

