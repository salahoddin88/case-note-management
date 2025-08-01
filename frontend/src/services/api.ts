import axios, { AxiosError } from 'axios';
import { 
  Client, 
  CaseNote, 
  CaseNoteCreateRequest, 
  CaseNoteCreateResponse, 
  CaseNotesListResponse 
} from '@/types/api';

// Token management utilities
export class TokenManager {
  private static readonly ACCESS_TOKEN_KEY = 'access_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private static readonly USER_INFO_KEY = 'user_info';

  static getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  static getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  static getUserInfo(): any | null {
    const userInfo = localStorage.getItem(this.USER_INFO_KEY);
    return userInfo ? JSON.parse(userInfo) : null;
  }

  static setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }

  static setUserInfo(userInfo: any): void {
    localStorage.setItem(this.USER_INFO_KEY, JSON.stringify(userInfo));
  }

  static clearTokens(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem(this.USER_INFO_KEY);
  }

  static isTokenExpired(token: string): boolean {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  }
}

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = TokenManager.getAccessToken();
    if (token && !TokenManager.isTokenExpired(token)) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = TokenManager.getRefreshToken();
      if (refreshToken && !TokenManager.isTokenExpired(refreshToken)) {
        try {
          const response = await axios.post('http://localhost:8000/api/auth/refresh', {
            refresh_token: refreshToken
          });

          const { access_token } = response.data;
          TokenManager.setTokens(access_token, refreshToken);

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          TokenManager.clearTokens();
          window.location.href = '/';
          return Promise.reject(refreshError);
        }
      } else {
        // No valid refresh token, redirect to login
        TokenManager.clearTokens();
        window.location.href = '/';
      }
    }

    return Promise.reject(error);
  }
);

// API service class
export class ApiService {
  // Authentication
  static async login(username: string, password: string): Promise<any> {
    try {
      const response = await axios.post('http://localhost:8000/api/auth/login', {
        username,
        password,
      });

      const { access_token, refresh_token, user } = response.data;
      TokenManager.setTokens(access_token, refresh_token);
      TokenManager.setUserInfo(user);

      return { success: true, user };
    } catch (error: any) {
      console.error('Login error:', error);
      if (error.response?.status === 401) {
        throw new Error('Invalid credentials');
      }
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Login failed. Please try again.');
    }
  }

  static async logout(): Promise<any> {
    try {
      const refreshToken = TokenManager.getRefreshToken();
      
      if (refreshToken) {
        await axios.post('http://localhost:8000/api/auth/logout', {
          refresh_token: refreshToken
        });
      }

      TokenManager.clearTokens();
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      // Even if logout request fails, clear local tokens
      TokenManager.clearTokens();
      return { success: true };
    }
  }

  static isAuthenticated(): boolean {
    const token = TokenManager.getAccessToken();
    return token !== null && !TokenManager.isTokenExpired(token);
  }

  static async refreshToken(): Promise<boolean> {
    try {
      const refreshToken = TokenManager.getRefreshToken();
      if (!refreshToken || TokenManager.isTokenExpired(refreshToken)) {
        return false;
      }

      const response = await axios.post('http://localhost:8000/api/auth/refresh', {
        refresh_token: refreshToken
      });

      const { access_token } = response.data;
      TokenManager.setTokens(access_token, refreshToken);
      return true;
    } catch {
      TokenManager.clearTokens();
      return false;
    }
  }

  // Client search with pagination
  static async searchClients(query: string = "", page: number = 1, pageSize: number = 10): Promise<any> {
    try {
      const response = await api.get('/clients/search', {
        params: { q: query, page, page_size: pageSize }
      });
      return response.data;
    } catch (error) {
      console.error('Error searching clients:', error);
      throw new Error('Failed to search clients');
    }
  }

  // Create case note
  static async createCaseNote(data: CaseNoteCreateRequest): Promise<CaseNoteCreateResponse> {
    try {
      const response = await api.post<CaseNoteCreateResponse>('/case-notes/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error creating case note:', error);
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Failed to create case note');
    }
  }

  // Get case notes for a client
  static async getClientCaseNotes(clientId: string): Promise<CaseNote[]> {
    try {
      const response = await api.get<CaseNotesListResponse>(`/case-notes/client/${clientId}`);
      return response.data.case_notes;
    } catch (error: any) {
      console.error('Error fetching case notes:', error);
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw new Error('Failed to fetch case notes');
    }
  }
}

// Export the axios instance for direct use if needed
export default api;