import type {
  CrawlerConfig,
  CrawlerStatusResponse,
  HealthResponse,
  ImageUploadResponse,
  LoginRequest,
  LoginResponse,
  PublishNoteRequest,
  PublishNoteResponse,
  PublisherStatusResponse,
  TopicSearchResponse,
  User,
} from '@/types';

const getApiUrl = (): string => {
  const configuredUrl = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '');
  if (configuredUrl) return configuredUrl;
  return typeof window === 'undefined' ? '' : window.location.origin;
};

export const getWsUrl = (): string => {
  const apiUrl = getApiUrl();
  if (apiUrl) return apiUrl.replace(/^http/, 'ws');

  if (typeof window === 'undefined') return '';
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}`;
};

async function apiRequest<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const headers = new Headers(options.headers);
  if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  if (token) headers.set('Authorization', `Bearer ${token}`);

  const response = await fetch(`${getApiUrl()}${path}`, { ...options, headers });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const healthApi = {
  check: () => apiRequest<HealthResponse>('/api/health'),
};

export const authApi = {
  login: (credentials: LoginRequest) =>
    apiRequest<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    }),
  getCurrentUser: (token: string) => apiRequest<User>('/api/auth/me', {}, token),
  logout: (token: string) => apiRequest<{ message: string }>('/api/auth/logout', { method: 'POST' }, token),
};

export const crawlerApi = {
  getStatus: (token: string) => apiRequest<CrawlerStatusResponse>('/api/crawler/status', {}, token),
  start: (token: string, config: CrawlerConfig) =>
    apiRequest<{ status: string; message: string }>(
      '/api/crawler/start',
      { method: 'POST', body: JSON.stringify(config) },
      token,
    ),
  stop: (token: string) =>
    apiRequest<{ status: string; message: string }>('/api/crawler/stop', { method: 'POST' }, token),
};

export interface DataFileInfo {
  name: string;
  path: string;
  size: number;
  modified_at: number;
  record_count: number | null;
  type: string;
}

export const dataApi = {
  getFiles: (token: string, platform?: string, fileType?: string) => {
    const params = new URLSearchParams();
    if (platform) params.set('platform', platform);
    if (fileType) params.set('file_type', fileType);
    const query = params.toString();
    return apiRequest<{ files: DataFileInfo[] }>(`/api/data/files${query ? `?${query}` : ''}`, {}, token);
  },
  getFileContent: <T>(token: string, filePath: string, limit = 10) =>
    apiRequest<{ data: T[]; total: number }>(
      `/api/data/files/${encodeURIComponent(filePath)}?preview=true&limit=${limit}`,
      {},
      token,
    ),
};

export const publisherApi = {
  getStatus: (token: string) => apiRequest<PublisherStatusResponse>('/api/publisher/status', {}, token),
  searchTopic: (token: string, keyword: string, page = 1) =>
    apiRequest<TopicSearchResponse>(
      '/api/publisher/topic/search',
      { method: 'POST', body: JSON.stringify({ keyword, page, page_size: 20 }) },
      token,
    ),
  uploadImage: (token: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiRequest<ImageUploadResponse>('/api/publisher/upload', { method: 'POST', body: formData }, token);
  },
  deleteImage: (token: string, fileId: string) =>
    apiRequest<{ status: string; message: string }>(
      `/api/publisher/upload/${encodeURIComponent(fileId)}`,
      { method: 'DELETE' },
      token,
    ),
  publishNote: (token: string, request: PublishNoteRequest) =>
    apiRequest<PublishNoteResponse>(
      '/api/publisher/publish',
      { method: 'POST', body: JSON.stringify(request) },
      token,
    ),
};
