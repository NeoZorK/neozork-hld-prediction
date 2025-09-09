/**
 * API Client Tests
 * 
 * Unit tests for the API client.
 */

import { ApiClient } from '../services/apiClient';

// Mock fetch
global.fetch = jest.fn();
const mockFetch = fetch as jest.MockedFunction<typeof fetch>;

// Mock AbortSignal
global.AbortSignal = {
  timeout: jest.fn(() => ({ aborted: false }))
} as any;

// ============================================================================
// TESTS
// ============================================================================

describe('ApiClient', () => {
  let apiClient: ApiClient;

  beforeEach(() => {
    jest.clearAllMocks();
    apiClient = new ApiClient({
      baseURL: 'https://api.example.com',
      timeout: 5000
    });
  });

  describe('constructor', () => {
    it('initializes with default config', () => {
      const client = new ApiClient();
      expect(client).toBeDefined();
    });

    it('initializes with custom config', () => {
      const client = new ApiClient({
        baseURL: 'https://custom.api.com',
        timeout: 10000,
        headers: { 'Custom-Header': 'value' }
      });
      expect(client).toBeDefined();
    });
  });

  describe('setAuthToken', () => {
    it('sets authentication token', () => {
      apiClient.setAuthToken('test-token');
      expect(apiClient.getAuthToken()).toBe('test-token');
    });

    it('removes authentication token when set to null', () => {
      apiClient.setAuthToken('test-token');
      apiClient.setAuthToken(null);
      expect(apiClient.getAuthToken()).toBeNull();
    });
  });

  describe('request', () => {
    it('makes successful GET request', async () => {
      const mockResponse = {
        success: true,
        data: { message: 'success' }
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response);

      const result = await apiClient.request({
        method: 'GET',
        url: '/test',
        data: { test: 'data' }
      });

      expect(result.data).toEqual(mockResponse);
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          })
        })
      );
    });

    it('makes successful POST request with data', async () => {
      const mockResponse = {
        success: true,
        data: { id: 1 }
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response);

      const result = await apiClient.request({
        method: 'POST',
        url: '/test',
        data: { name: 'test' }
      });

      expect(result.data).toEqual(mockResponse);
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ name: 'test' })
        })
      );
    });

    it('handles API errors', async () => {
      const mockError = {
        error: 'API Error',
        message: 'Something went wrong'
      };

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => mockError
      } as Response);

      await expect(apiClient.request({
        method: 'GET',
        url: '/test'
      })).rejects.toThrow('API Error');
    });

    it('handles network errors', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      await expect(apiClient.request({
        method: 'GET',
        url: '/test'
      })).rejects.toThrow('Network error');
    });

    it('handles JSON parsing errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => { throw new Error('Invalid JSON'); }
      } as Response);

      await expect(apiClient.request({
        method: 'GET',
        url: '/test'
      })).rejects.toThrow('Invalid JSON response');
    });

    it('includes authentication token in headers', async () => {
      apiClient.setAuthToken('test-token');

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, data: {} })
      } as Response);

      await apiClient.request({
        method: 'GET',
        url: '/test'
      });

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer test-token'
          })
        })
      );
    });

    it('builds URL with query parameters', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, data: {} })
      } as Response);

      await apiClient.request({
        method: 'GET',
        url: '/test',
        params: { page: 1, limit: 10, search: 'test' }
      });

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test?page=1&limit=10&search=test',
        expect.any(Object)
      );
    });

    it('handles absolute URLs', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ success: true, data: {} })
      } as Response);

      await apiClient.request({
        method: 'GET',
        url: 'https://external.api.com/test'
      });

      expect(mockFetch).toHaveBeenCalledWith(
        'https://external.api.com/test',
        expect.any(Object)
      );
    });
  });

  describe('HTTP methods', () => {
    beforeEach(() => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: async () => ({ success: true, data: {} })
      } as Response);
    });

    it('makes GET request', async () => {
      await apiClient.get('/test', { param: 'value' });
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test?param=value',
        expect.objectContaining({ method: 'GET' })
      );
    });

    it('makes POST request', async () => {
      await apiClient.post('/test', { data: 'value' });
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ data: 'value' })
        })
      );
    });

    it('makes PUT request', async () => {
      await apiClient.put('/test', { data: 'value' });
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'PUT',
          body: JSON.stringify({ data: 'value' })
        })
      );
    });

    it('makes PATCH request', async () => {
      await apiClient.patch('/test', { data: 'value' });
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({
          method: 'PATCH',
          body: JSON.stringify({ data: 'value' })
        })
      );
    });

    it('makes DELETE request', async () => {
      await apiClient.delete('/test');
      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/test',
        expect.objectContaining({ method: 'DELETE' })
      );
    });
  });

  describe('upload', () => {
    it('uploads file successfully', async () => {
      const mockFile = new File(['test'], 'test.txt', { type: 'text/plain' });
      const mockResponse = { success: true, data: { url: 'uploaded-url' } };

      // Mock XMLHttpRequest
      const mockXHR = {
        upload: {
          addEventListener: jest.fn()
        },
        addEventListener: jest.fn(),
        open: jest.fn(),
        send: jest.fn(),
        setRequestHeader: jest.fn(),
        status: 200,
        responseText: JSON.stringify(mockResponse)
      };

      global.XMLHttpRequest = jest.fn(() => mockXHR) as any;

      const result = await apiClient.upload('/upload', mockFile);

      expect(result.data).toEqual(mockResponse);
      expect(mockXHR.open).toHaveBeenCalledWith('POST', 'https://api.example.com/upload');
      expect(mockXHR.send).toHaveBeenCalled();
    });
  });

  describe('download', () => {
    it('downloads file successfully', async () => {
      const mockBlob = new Blob(['test content'], { type: 'text/plain' });
      const mockResponse = {
        ok: true,
        blob: async () => mockBlob
      };

      mockFetch.mockResolvedValueOnce(mockResponse as Response);

      // Mock DOM methods
      const mockLink = {
        href: '',
        download: '',
        click: jest.fn()
      };
      const mockCreateElement = jest.fn(() => mockLink);
      const mockAppendChild = jest.fn();
      const mockRemoveChild = jest.fn();
      const mockRevokeObjectURL = jest.fn();

      global.document.createElement = mockCreateElement;
      global.document.body.appendChild = mockAppendChild;
      global.document.body.removeChild = mockRemoveChild;
      global.URL.createObjectURL = jest.fn(() => 'blob-url');
      global.URL.revokeObjectURL = mockRevokeObjectURL;

      await apiClient.download('/download', 'test.txt');

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.example.com/download',
        expect.objectContaining({
          headers: {}
        })
      );
      expect(mockCreateElement).toHaveBeenCalledWith('a');
      expect(mockLink.href).toBe('blob-url');
      expect(mockLink.download).toBe('test.txt');
      expect(mockLink.click).toHaveBeenCalled();
      expect(mockAppendChild).toHaveBeenCalledWith(mockLink);
      expect(mockRemoveChild).toHaveBeenCalledWith(mockLink);
      expect(mockRevokeObjectURL).toHaveBeenCalledWith('blob-url');
    });

    it('handles download errors', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found'
      } as Response);

      await expect(apiClient.download('/download')).rejects.toThrow('HTTP 404: Not Found');
    });
  });
});
