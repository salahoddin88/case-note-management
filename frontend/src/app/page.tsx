'use client';

import { useState, useEffect } from 'react';
import CaseNoteManager from '@/components/CaseNoteManager';
import LoginForm from '@/components/LoginForm';
import ErrorBoundary from '@/components/ErrorBoundary';
import LoadingSpinner from '@/components/LoadingSpinner';
import { ApiService, TokenManager } from '@/services/api';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [currentUser, setCurrentUser] = useState<any>(null);

  useEffect(() => {
    // Check if user is already authenticated on page load
    const checkAuth = async () => {
      if (ApiService.isAuthenticated()) {
        setIsAuthenticated(true);
        const userInfo = TokenManager.getUserInfo();
        setCurrentUser(userInfo);
      } else {
        // Try to refresh token if available
        const refreshed = await ApiService.refreshToken();
        setIsAuthenticated(refreshed);
        if (refreshed) {
          const userInfo = TokenManager.getUserInfo();
          setCurrentUser(userInfo);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const handleLogin = (userInfo?: any) => {
    setIsAuthenticated(true);
    if (userInfo) {
      setCurrentUser(userInfo);
    } else {
      const storedUserInfo = TokenManager.getUserInfo();
      setCurrentUser(storedUserInfo);
    }
  };

  const handleLogout = async () => {
    try {
      await ApiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setIsAuthenticated(false);
      setCurrentUser(null);
    }
  };

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <main className="min-h-screen bg-gray-100 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading..." />
      </main>
    );
  }

  return (
    <ErrorBoundary>
      <main className="min-h-screen bg-gray-100">
        {isAuthenticated ? (
          <div>
            <div className="bg-white shadow-sm border-b">
              <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
                <h1 className="text-xl font-semibold text-gray-900">
                  Case Note Management System
                </h1>
                <div className="flex items-center space-x-4">
                  {currentUser && (
                    <div className="text-sm text-gray-700">
                      Welcome, <span className="font-medium">{currentUser.name || currentUser.username}</span>
                    </div>
                  )}
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
            <CaseNoteManager />
          </div>
        ) : (
          <LoginForm onLogin={handleLogin} />
        )}
      </main>
    </ErrorBoundary>
  );
}
