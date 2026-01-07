// 类型定义文件

// 用户认证相关类型
export interface User {
  id: number;
  username: string;
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
  enable_comments?: boolean;
  enable_sub_comments?: boolean;
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
  is_running: boolean;
  current_task: CrawlerTask | null;
  supported_platforms: string[];
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
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
  message: string;
  module?: string;
}

// WebSocket消息类型
export interface WSMessage {
  type: 'log' | 'status' | 'progress' | 'error';
  data: LogEntry | CrawlerTask | string;
}
