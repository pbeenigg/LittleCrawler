// 类型定义文件

// 用户认证相关类型
export interface User {
  id: number;
  username: string;
  is_active: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// API健康检查响应
export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

// 爬虫配置类型
export interface CrawlerConfig {
  platform: 'xhs' | 'zhihu';
  crawler_type: 'search' | 'detail' | 'creator';
  login_type: 'qrcode' | 'phone' | 'cookie';
  keywords?: string;  // 搜索关键词（search模式）
  specified_ids?: string;  // 指定ID列表（detail模式）
  creator_ids?: string;  // 创作者ID列表（creator模式）
  start_page?: number;
  max_pages?: number;
  enable_comments?: boolean;
  enable_sub_comments?: boolean;
  enable_proxy?: boolean;
  enable_cdp?: boolean;
  save_option?: SaveDataOption;
  cookies?: string;
  headless?: boolean;
}

export type SaveDataOption = 'csv' | 'json' | 'db' | 'sqlite' | 'mongodb' | 'excel';

// 爬虫任务状态
export interface CrawlerTask {
  task_id: string;
  status: 'idle' | 'running' | 'completed' | 'error';
  platform: string;
  crawler_type: string;
  progress?: number;
  message?: string;
  created_at: string;
}

// 爬虫状态响应
export interface CrawlerStatusResponse {
  status: 'idle' | 'running' | 'stopping' | 'error';
  platform: string | null;
  crawler_type: string | null;
  started_at: string | null;
  error_message: string | null;
}

// 数据记录类型（通用）
export interface DataRecord {
  id: string;
  note_id?: string;
  title: string;
  desc?: string;
  author: string;
  avatar?: string;
  likes_count: number;
  comments_count: number;
  share_count?: number;
  collected_count?: number;
  create_time: string;
  source_keyword?: string;
  note_url?: string;
  image_list?: string[];
}

// 分页响应
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// 日志条目
export interface LogEntry {
  timestamp: string;
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS';
  message: string;
  module?: string;
}

// WebSocket消息类型
export interface WSMessage {
  type: 'log' | 'status' | 'progress' | 'error';
  data: LogEntry | CrawlerTask | string;
}

// ========== 笔记发布相关类型 ==========

// 话题信息
export interface TopicInfo {
  id: string;
  name: string;
  link: string;
  type: string;
}

// 话题搜索响应
export interface TopicSearchResponse {
  topics: TopicInfo[];
}

// 上传图片响应
export interface ImageUploadResponse {
  file_id: string;
  width: number;
  height: number;
  url: string;
}

// 发布笔记请求
export interface PublishNoteRequest {
  title: string;
  desc: string;
  image_ids: string[];
  topic_ids?: string[];
}

// 发布笔记响应
export interface PublishNoteResponse {
  success: boolean;
  note_id: string;
  message: string;
}

// 发布器状态响应
export interface PublisherStatusResponse {
  available: boolean;
  logged_in: boolean;
  platform: string;
  message: string;
}
