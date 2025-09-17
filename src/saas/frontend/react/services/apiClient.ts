/**
 * API Client for SaaS Frontend
 * 
 * This service handles all HTTP requests to the SaaS backend API.
 */

import { ApiResponse, ApiError } from '../types';

// ============================================================================
// INTERFACES
// ============================================================================

interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  url: string;
  data?: any;
  headers?: Record<string, string>;
  params?: Record<string, any>;
}

interface ApiClientConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

// ============================================================================
// API CLIENT CLASS
// ============================================================================

export class ApiClient {
  private config: ApiClientConfig;
  private authToken: string | null = null;

  constructor(config: Partial<ApiClientConfig> = {}) {
    this.config = {
      baseURL: config.baseURL || process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
      timeout: config.timeout || 10000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...config.headers
      }
    };
  }

  /**
   * Set authentication token
   */
  setAuthToken(token: string | null) {
    this.authToken = token;
    if (token) {
      this.config.headers['Authorization'] = `Bearer ${token}`;
    } else {
      delete this.config.headers['Authorization'];
    }
  }

  /**
   * Get authentication token
   */
  getAuthToken(): string | null {
    return this.authToken;
  }

  /**
   * Make HTTP request
   */
  async request<T>(config: RequestConfig): Promise<{ data: ApiResponse<T> }> {
    const { method, url, data, headers = {}, params } = config;
    
    // Build full URL
    const fullUrl = this.buildUrl(url, params);
    
    // Prepare request options
    const requestOptions: RequestInit = {
      method,
      headers: {
        ...this.config.headers,
        ...headers
      },
      signal: AbortSignal.timeout(this.config.timeout)
    };

    // Add body for non-GET requests
    if (data && method !== 'GET') {
      requestOptions.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(fullUrl, requestOptions);
      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      return { data: responseData };
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(error.message);
      }
      throw new Error('Network error occurred');
    }
  }

  /**
   * Build full URL with query parameters
   */
  private buildUrl(url: string, params?: Record<string, any>): string {
    const fullUrl = url.startsWith('http') ? url : `${this.config.baseURL}${url}`;
    
    if (!params) return fullUrl;
    
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, value.toString());
      }
    });
    
    const queryString = searchParams.toString();
    return queryString ? `${fullUrl}?${queryString}` : fullUrl;
  }

  /**
   * GET request
   */
  async get<T>(url: string, params?: Record<string, any>, headers?: Record<string, string>) {
    return this.request<T>({ method: 'GET', url, params, headers });
  }

  /**
   * POST request
   */
  async post<T>(url: string, data?: any, headers?: Record<string, string>) {
    return this.request<T>({ method: 'POST', url, data, headers });
  }

  /**
   * PUT request
   */
  async put<T>(url: string, data?: any, headers?: Record<string, string>) {
    return this.request<T>({ method: 'PUT', url, data, headers });
  }

  /**
   * PATCH request
   */
  async patch<T>(url: string, data?: any, headers?: Record<string, string>) {
    return this.request<T>({ method: 'PATCH', url, data, headers });
  }

  /**
   * DELETE request
   */
  async delete<T>(url: string, headers?: Record<string, string>) {
    return this.request<T>({ method: 'DELETE', url, headers });
  }

  /**
   * Upload file
   */
  async upload<T>(url: string, file: File, onProgress?: (progress: number) => void) {
    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();
    
    return new Promise<{ data: ApiResponse<T> }>((resolve, reject) => {
      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable && onProgress) {
          const progress = (event.loaded / event.total) * 100;
          onProgress(progress);
        }
      });

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            const response = JSON.parse(xhr.responseText);
            resolve({ data: response });
          } catch (error) {
            reject(new Error('Invalid JSON response'));
          }
        } else {
          reject(new Error(`HTTP ${xhr.status}: ${xhr.statusText}`));
        }
      });

      xhr.addEventListener('error', () => {
        reject(new Error('Network error occurred'));
      });

      xhr.open('POST', `${this.config.baseURL}${url}`);
      
      // Add authorization header if token exists
      if (this.authToken) {
        xhr.setRequestHeader('Authorization', `Bearer ${this.authToken}`);
      }
      
      xhr.send(formData);
    });
  }

  /**
   * Download file
   */
  async download(url: string, filename?: string) {
    const fullUrl = this.buildUrl(url);
    
    try {
      const response = await fetch(fullUrl, {
        headers: this.authToken ? { 'Authorization': `Bearer ${this.authToken}` } : {}
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename || 'download';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      throw new Error(error instanceof Error ? error.message : 'Download failed');
    }
  }
}

// ============================================================================
// EXPORT INSTANCE
// ============================================================================

export const apiClient = new ApiClient();
