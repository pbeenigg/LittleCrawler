'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Input,
  Select,
  SelectItem,
  Switch,
  Chip,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Avatar,
  Progress,
  Spinner,
  Tooltip,
  Divider,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from '@nextui-org/react';
import { useAuth } from '@/contexts/AuthContext';
import { useI18n } from '@/contexts/I18nContext';
import {
  Play,
  Square,
  Settings,
  Moon,
  Sun,
  Globe,
  LogOut,
  User,
  Zap,
  Activity,
  Terminal,
  Trash2,
  Pause,
  Maximize2,
  Minimize2,
  ChevronDown,
  Download,
  Search,
  Database,
  Wifi,
  WifiOff,
  RefreshCw,
  Eye,
  Copy,
  ExternalLink,
  BookOpen,
  MessageCircle,
  QrCode,
  Smartphone,
  Cookie,
  FileJson,
  FileSpreadsheet,
  HardDrive,
  Leaf,
  FileStack,
  PenSquare,
} from 'lucide-react';
import { useTheme } from 'next-themes';
import { crawlerApi, dataApi, getWsUrl } from '@/lib/api';
import type { CrawlerConfig, CrawlerStatusResponse, SaveDataOption } from '@/types';

// 格式化日志时间戳，支持 "YYYY-MM-DD HH:mm:ss" 和 ISO 格式
const formatLogTime = (timestamp: string): string => {
  try {
    // 尝试直接解析
    let date = new Date(timestamp);
    
    // 如果解析失败，尝试将 "YYYY-MM-DD HH:mm:ss" 转换为 ISO 格式
    if (isNaN(date.getTime())) {
      // 替换空格为 T，使其成为有效的 ISO 格式
      const isoTimestamp = timestamp.replace(' ', 'T');
      date = new Date(isoTimestamp);
    }
    
    // 如果仍然失败，返回原始时间戳中的时间部分
    if (isNaN(date.getTime())) {
      // 尝试提取 HH:mm:ss 部分
      const timeMatch = timestamp.match(/\d{2}:\d{2}:\d{2}/);
      return timeMatch ? timeMatch[0] : timestamp;
    }
    
    return date.toLocaleTimeString();
  } catch {
    return timestamp;
  }
};

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARNING' | 'ERROR' | 'DEBUG' | 'SUCCESS';
  message: string;
}

interface DataItem {
  id?: string;
  note_id?: string;
  title?: string;
  desc?: string;
  type?: string;
  liked_count?: string | number;
  collected_count?: string | number;
  comment_count?: string | number;
  share_count?: string | number;
  nickname?: string;  // 小红书用 nickname
  user_nickname?: string;  // 兼容其他格式
  note_url?: string;
  created_at?: string;
  time?: number;
}

const LOG_COLORS: Record<string, string> = {
  INFO: 'text-cyan-400',
  WARNING: 'text-yellow-400',
  ERROR: 'text-red-400',
  DEBUG: 'text-gray-400',
  SUCCESS: 'text-green-400',
};

export default function DashboardPage() {
  const { user, token, logout } = useAuth();
  const { t, locale, setLocale } = useI18n();
  const { theme, setTheme } = useTheme();
  const router = useRouter();

  // 爬虫配置
  const [platform, setPlatform] = useState<CrawlerConfig['platform']>('xhs');
  const [crawlerType, setCrawlerType] = useState<CrawlerConfig['crawler_type']>('search');
  const [loginType, setLoginType] = useState<CrawlerConfig['login_type']>('qrcode');
  const [saveFormat, setSaveFormat] = useState<SaveDataOption>('json');
  const [maxPages, setMaxPages] = useState('');  // 空字符串表示使用后端默认限制
  const [keywords, setKeywords] = useState('');
  const [enableProxy, setEnableProxy] = useState(false);
  const [enableCdp, setEnableCdp] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const [crawlerStatus, setCrawlerStatus] = useState<CrawlerStatusResponse | null>(null);

  // 日志
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isPaused, setIsPaused] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  // 数据
  const [dataList, setDataList] = useState<DataItem[]>([]);
  const [dataLoading, setDataLoading] = useState(false);
  const [dataTotal, setDataTotal] = useState(0);

  // 滚动到底部
  const scrollToBottom = useCallback(() => {
    if (!isPaused && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [isPaused]);

  useEffect(() => {
    scrollToBottom();
  }, [logs, scrollToBottom]);

  // WebSocket 连接
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;

    const connectWs = () => {
      const ws = new WebSocket(`${getWsUrl()}/api/ws/logs?token=${token}`);
      wsRef.current = ws;

      ws.onopen = () => {
        setWsConnected(true);
        addSystemLog('WebSocket 连接已建立');
      };

      ws.onmessage = (event) => {
        try {
          // 处理 ping/pong 心跳
          if (event.data === 'ping') {
            ws.send('pong');
            return;
          }
          if (event.data === 'pong') {
            return;
          }
          
          const data = JSON.parse(event.data);
          // 后端日志格式: { id, timestamp, level, message }
          if (data.message) {
            const logEntry: LogEntry = {
              id: data.id?.toString() || Date.now().toString() + Math.random(),
              timestamp: data.timestamp || new Date().toISOString(),
              level: (data.level?.toUpperCase() || 'INFO') as LogEntry['level'],
              message: data.message || '',
            };
            setLogs((prev) => [...prev.slice(-500), logEntry]);
          }
        } catch (e) {
          // 非JSON消息忽略
          if (event.data !== 'ping' && event.data !== 'pong') {
            console.error('解析日志失败', e);
          }
        }
      };

      ws.onclose = () => {
        setWsConnected(false);
        addSystemLog('WebSocket 连接已断开，5秒后重连...');
        setTimeout(connectWs, 5000);
      };

      ws.onerror = () => {
        setWsConnected(false);
      };
    };

    connectWs();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // 添加系统日志
  const addSystemLog = (message: string, level: LogEntry['level'] = 'INFO') => {
    setLogs((prev) => [
      ...prev.slice(-500),
      {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        level,
        message: `[System] ${message}`,
      },
    ]);
  };

  // 获取爬虫状态
  useEffect(() => {
    if (!token) return;
    
    const fetchStatus = async () => {
      try {
        const status = await crawlerApi.getStatus(token);
        setCrawlerStatus(status);
        // 后端返回 status: "idle" | "running" | "stopping" | "error"
        setIsRunning(status.status === 'running' || status.status === 'stopping');
      } catch (e) {
        console.error('获取状态失败', e);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [token]);

  // 加载数据
  const loadData = async () => {
    if (!token) return;
    setDataLoading(true);
    try {
      const fileType = saveFormat === 'excel'
        ? 'xlsx'
        : saveFormat === 'json' || saveFormat === 'csv'
          ? saveFormat
          : null;
      if (!fileType) {
        setDataList([]);
        setDataTotal(0);
        return;
      }

      // 1. 获取该平台的文件列表
      const filesRes = await dataApi.getFiles(token, platform, fileType);
      const files = filesRes.files || [];
      
      if (files.length > 0) {
        // 2. 优先选择 contents 文件（笔记/文章），其次是 comments
        const contentsFile = files.find((file) => file.name.includes('contents'));
        const latestFile = contentsFile || files[0];
        
        // 3. 获取文件内容预览
        const contentRes = await dataApi.getFileContent<DataItem>(token, latestFile.path, 10);
        setDataList(contentRes.data || []);
        setDataTotal(contentRes.total || 0);
      } else {
        setDataList([]);
        setDataTotal(0);
      }
    } catch (e) {
      console.error('加载数据失败', e);
      setDataList([]);
      setDataTotal(0);
    } finally {
      setDataLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      loadData();
    }
  }, [platform, saveFormat, token]);
  
  // 爬虫运行时定期刷新数据
  useEffect(() => {
    if (!isRunning || !token) return;
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, [isRunning, token, platform, saveFormat]);

  // 启动爬虫
  const handleStart = async () => {
    if (!token) return;
    const inputValue = keywords.trim();
    if (!inputValue) {
      const inputName = crawlerType === 'search' ? '搜索关键词' : crawlerType === 'detail' ? '内容 ID/URL' : '创作者 ID/URL';
      addSystemLog(`请输入${inputName}`, 'WARNING');
      return;
    }

    try {
      addSystemLog(`开始启动 ${platform} 爬虫...`);
      const crawlerConfig: CrawlerConfig = {
        platform,
        crawler_type: crawlerType,
        login_type: loginType,
        save_option: saveFormat,
        start_page: 1,
        max_pages: maxPages ? parseInt(maxPages) : undefined,
        enable_comments: true,
        enable_proxy: enableProxy,
        enable_cdp: enableCdp,
      };
      if (crawlerType === 'search') crawlerConfig.keywords = inputValue;
      if (crawlerType === 'detail') crawlerConfig.specified_ids = inputValue;
      if (crawlerType === 'creator') crawlerConfig.creator_ids = inputValue;

      await crawlerApi.start(token, crawlerConfig);
      setIsRunning(true);
      addSystemLog('爬虫启动成功！', 'INFO');
    } catch (e: any) {
      addSystemLog(`启动失败: ${e.message}`, 'ERROR');
    }
  };

  // 停止爬虫
  const handleStop = async () => {
    if (!token) return;
    try {
      await crawlerApi.stop(token);
      setIsRunning(false);
      addSystemLog('爬虫已停止', 'WARNING');
    } catch (e: any) {
      addSystemLog(`停止失败: ${e.message}`, 'ERROR');
    }
  };

  // 清空日志
  const clearLogs = () => {
    setLogs([]);
    addSystemLog('日志已清空');
  };

  // 登出
  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // 复制内容
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* 背景装饰 */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-pulse" />
      </div>

      {/* 主容器 */}
      <div className="relative z-10">
        {/* 顶部导航 */}
        <header className="sticky top-0 z-50 backdrop-blur-xl bg-black/30 border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center">
                  <Zap className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-slate-900 animate-pulse" />
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                  LittleCrawler
                </h1>
                <p className="text-xs text-gray-400">v1.0</p>
              </div>
            </div>

            {/* 状态指示器 */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10">
                {wsConnected ? (
                  <>
                    <Wifi className="w-4 h-4 text-green-400" />
                    <span className="text-xs text-green-400">{t('common.connected')}</span>
                  </>
                ) : (
                  <>
                    <WifiOff className="w-4 h-4 text-red-400" />
                    <span className="text-xs text-red-400">{t('common.disconnected')}</span>
                  </>
                )}
              </div>

              {isRunning && (
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/20 border border-cyan-500/30">
                  <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
                  <span className="text-xs text-cyan-400">{t('common.running')}</span>
                </div>
              )}
            </div>

            {/* 右侧控制 */}
            <div className="flex items-center gap-3">
              {/* 语言切换 */}
              <Tooltip content={locale === 'zh' ? 'English' : '中文'}>
                <Button
                  isIconOnly
                  variant="flat"
                  className="bg-white/5 hover:bg-white/10"
                  onClick={() => setLocale(locale === 'zh' ? 'en' : 'zh')}
                >
                  <span className="text-xs font-medium text-gray-300">{locale === 'zh' ? 'EN' : '中'}</span>
                </Button>
              </Tooltip>

              {/* 主题切换 */}
              <Tooltip content={t('common.theme')}>
                <Button
                  isIconOnly
                  variant="flat"
                  className="bg-white/5 hover:bg-white/10"
                  onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                >
                  {theme === 'dark' ? (
                    <Sun className="w-4 h-4 text-yellow-400" />
                  ) : (
                    <Moon className="w-4 h-4 text-gray-400" />
                  )}
                </Button>
              </Tooltip>

              {/* 用户菜单 */}
              <Dropdown>
                <DropdownTrigger>
                  <Button variant="flat" className="bg-white/5 hover:bg-white/10 gap-2">
                    <Avatar
                      size="sm"
                      name={user?.username?.[0]?.toUpperCase()}
                      className="bg-gradient-to-br from-cyan-400 to-purple-500"
                    />
                    <span className="text-sm text-gray-300">{user?.username}</span>
                    <ChevronDown className="w-4 h-4 text-gray-400" />
                  </Button>
                </DropdownTrigger>
                <DropdownMenu>
                  <DropdownItem key="profile" startContent={<User className="w-4 h-4" />}>
                    {t('common.profile')}
                  </DropdownItem>
                  <DropdownItem key="settings" startContent={<Settings className="w-4 h-4" />}>
                    {t('common.settings')}
                  </DropdownItem>
                  <DropdownItem
                    key="logout"
                    className="text-danger"
                    color="danger"
                    startContent={<LogOut className="w-4 h-4" />}
                    onClick={handleLogout}
                  >
                    {t('common.logout')}
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </div>
          </div>
        </header>

        {/* 主内容区 */}
        <main className="max-w-7xl mx-auto px-4 py-6 space-y-6">
          {/* 上部：爬虫配置 + 数据概览 */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* 爬虫配置卡片 */}
            <Card className="lg:col-span-2 bg-white/5 backdrop-blur-xl border border-white/10">
              <CardHeader className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center">
                    <Settings className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-white">{t('dashboard.crawlerConfig')}</h2>
                    <p className="text-xs text-gray-400">{t('dashboard.configDescription')}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  {isRunning ? (
                    <Button
                      color="danger"
                      variant="flat"
                      startContent={<Square className="w-4 h-4" />}
                      onClick={handleStop}
                      className="bg-red-500/20 hover:bg-red-500/30"
                    >
                      {t('common.stop')}
                    </Button>
                  ) : (
                    <Button
                      color="success"
                      variant="flat"
                      startContent={<Play className="w-4 h-4" />}
                      onClick={handleStart}
                      className="bg-green-500/20 hover:bg-green-500/30"
                    >
                      {t('common.start')}
                    </Button>
                  )}
                </div>
              </CardHeader>
              <Divider className="bg-white/10" />
              <CardBody className="space-y-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Select
                    label={t('crawler.platform')}
                    selectedKeys={[platform]}
                    onChange={(e) => setPlatform(e.target.value as CrawlerConfig['platform'])}
                    classNames={{
                      trigger: 'bg-white/5 border-white/10 hover:bg-white/10',
                      label: 'text-gray-400',
                    }}
                  >
                    <SelectItem key="xhs" value="xhs" startContent={<BookOpen className="w-4 h-4 text-red-400" />}>
                      {t('crawler.platforms.xhs')}
                    </SelectItem>
                    <SelectItem key="zhihu" value="zhihu" startContent={<MessageCircle className="w-4 h-4 text-blue-400" />}>
                      {t('crawler.platforms.zhihu')}
                    </SelectItem>
                  </Select>

                  <Select
                    label={t('crawler.crawlerType')}
                    selectedKeys={[crawlerType]}
                    onChange={(e) => setCrawlerType(e.target.value as CrawlerConfig['crawler_type'])}
                    classNames={{
                      trigger: 'bg-white/5 border-white/10 hover:bg-white/10',
                      label: 'text-gray-400',
                    }}
                  >
                    <SelectItem key="search" value="search" startContent={<Search className="w-4 h-4 text-cyan-400" />}>
                      {t('crawler.types.search')}
                    </SelectItem>
                    <SelectItem key="detail" value="detail" startContent={<Eye className="w-4 h-4 text-purple-400" />}>
                      {t('crawler.types.detail')}
                    </SelectItem>
                    <SelectItem key="creator" value="creator" startContent={<User className="w-4 h-4 text-green-400" />}>
                      {t('crawler.types.creator')}
                    </SelectItem>
                  </Select>

                  <Select
                    label={t('crawler.loginType')}
                    selectedKeys={[loginType]}
                    onChange={(e) => setLoginType(e.target.value as CrawlerConfig['login_type'])}
                    classNames={{
                      trigger: 'bg-white/5 border-white/10 hover:bg-white/10',
                      label: 'text-gray-400',
                    }}
                  >
                    <SelectItem key="qrcode" value="qrcode" startContent={<QrCode className="w-4 h-4 text-orange-400" />}>
                      {t('crawler.loginTypes.qrcode')}
                    </SelectItem>
                    <SelectItem key="phone" value="phone" startContent={<Smartphone className="w-4 h-4 text-blue-400" />}>
                      {t('crawler.loginTypes.phone')}
                    </SelectItem>
                    <SelectItem key="cookie" value="cookie" startContent={<Cookie className="w-4 h-4 text-yellow-400" />}>
                      {t('crawler.loginTypes.cookie')}
                    </SelectItem>
                  </Select>

                  <Select
                    label={t('data.saveFormat')}
                    selectedKeys={[saveFormat]}
                    onChange={(e) => setSaveFormat(e.target.value as SaveDataOption)}
                    classNames={{
                      trigger: 'bg-white/5 border-white/10 hover:bg-white/10',
                      label: 'text-gray-400',
                    }}
                  >
                    <SelectItem key="json" value="json" startContent={<FileJson className="w-4 h-4 text-yellow-400" />}>
                      {t('data.formats.json')}
                    </SelectItem>
                    <SelectItem key="csv" value="csv" startContent={<FileSpreadsheet className="w-4 h-4 text-green-400" />}>
                      {t('data.formats.csv')}
                    </SelectItem>
                    <SelectItem key="sqlite" value="sqlite" startContent={<HardDrive className="w-4 h-4 text-blue-400" />}>
                      {t('data.formats.sqlite')}
                    </SelectItem>
                    <SelectItem key="mongodb" value="mongodb" startContent={<Leaf className="w-4 h-4 text-green-500" />}>
                      {t('data.formats.mongodb')}
                    </SelectItem>
                  </Select>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Input
                    label={crawlerType === 'search'
                      ? t('crawler.keywords')
                      : crawlerType === 'detail'
                        ? t('crawler.specifiedIds')
                        : t('crawler.creatorIds')}
                    placeholder={crawlerType === 'search'
                      ? t('crawler.keywordsPlaceholder')
                      : crawlerType === 'detail'
                        ? t('crawler.specifiedIdsPlaceholder')
                        : t('crawler.creatorIdsPlaceholder')}
                    value={keywords}
                    onChange={(e) => setKeywords(e.target.value)}
                    startContent={<Search className="w-4 h-4 text-gray-400" />}
                    classNames={{
                      inputWrapper: 'bg-white/5 border-white/10 hover:bg-white/10',
                      label: 'text-gray-400',
                    }}
                    className="md:col-span-2"
                  />

                  <Input
                    label={t('crawler.maxPages')}
                    placeholder={t('crawler.maxPagesPlaceholder')}
                    description={t('crawler.maxPagesDescription')}
                    type="number"
                    min="1"
                    value={maxPages}
                    onChange={(e) => setMaxPages(e.target.value)}
                    startContent={<FileStack className="w-4 h-4 text-gray-400" />}
                    classNames={{
                      inputWrapper: 'bg-white/5 border-white/10 hover:bg-white/10',
                      label: 'text-gray-400',
                      description: 'text-gray-500 text-xs',
                    }}
                  />
                </div>

                <div className="flex flex-wrap gap-6">
                  <Switch
                    isSelected={enableProxy}
                    onValueChange={setEnableProxy}
                    classNames={{
                      wrapper: 'group-data-[selected=true]:bg-cyan-500',
                    }}
                  >
                    <span className="text-sm text-gray-300">{t('crawler.enableProxy')}</span>
                  </Switch>
                  <Switch
                    isSelected={enableCdp}
                    onValueChange={setEnableCdp}
                    classNames={{
                      wrapper: 'group-data-[selected=true]:bg-purple-500',
                    }}
                  >
                    <span className="text-sm text-gray-300">{t('crawler.cdpMode')}</span>
                  </Switch>
                </div>
              </CardBody>
            </Card>

            {/* 右侧区域：数据概览 + 发布模块 */}
            <div className="space-y-6">
              {/* 数据概览卡片 */}
              <Card className="bg-white/5 backdrop-blur-xl border border-white/10">
                <CardHeader className="flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center">
                      <Database className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-white">{t('dashboard.dataStats')}</h2>
                    <p className="text-xs text-gray-400">{t('dashboard.collectedData')}</p>
                  </div>
                </div>
                <Button
                  isIconOnly
                  variant="flat"
                  size="sm"
                  onClick={loadData}
                  className="bg-white/5 hover:bg-white/10"
                >
                  <RefreshCw className={`w-4 h-4 text-gray-400 ${dataLoading ? 'animate-spin' : ''}`} />
                </Button>
              </CardHeader>
              <Divider className="bg-white/10" />
              <CardBody className="space-y-4">
                <div className="text-center py-4">
                  <div className="text-5xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                    {dataTotal.toLocaleString()}
                  </div>
                  <p className="text-sm text-gray-400 mt-2">{t('data.records')}</p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-2xl font-semibold text-cyan-400">
                      {crawlerStatus?.platform || '-'}
                    </div>
                    <p className="text-xs text-gray-400">{t('crawler.platform')}</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3 text-center">
                    <div className="text-2xl font-semibold text-purple-400">
                      {crawlerStatus?.crawler_type || '-'}
                    </div>
                    <p className="text-xs text-gray-400">{t('crawler.crawlerType')}</p>
                  </div>
                </div>

                {isRunning && (
                  <Progress
                    size="sm"
                    isIndeterminate
                    color="secondary"
                    className="max-w-full"
                    classNames={{
                      indicator: 'bg-gradient-to-r from-cyan-400 to-purple-500',
                    }}
                  />
                )}
              </CardBody>
            </Card>

            {/* 发布模块卡片 */}
            <Card className="bg-white/5 backdrop-blur-xl border border-white/10">
              <CardHeader className="flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center">
                    <PenSquare className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-white">{t('publish.center')}</h2>
                    <p className="text-xs text-gray-400">{t('publish.description')}</p>
                  </div>
                </div>
              </CardHeader>
              <Divider className="bg-white/10" />
              <CardBody className="space-y-3">
                {/* 小红书 */}
                <Button
                  className="w-full justify-start bg-gradient-to-r from-red-500/20 to-pink-500/20 hover:from-red-500/30 hover:to-pink-500/30 border border-red-500/30"
                  variant="flat"
                  startContent={
                    <div className="w-6 h-6 rounded bg-gradient-to-br from-red-500 to-pink-500 flex items-center justify-center">
                      <BookOpen className="w-3.5 h-3.5 text-white" />
                    </div>
                  }
                  onClick={() => router.push('/dashboard/publish')}
                >
                  <div className="flex-1 text-left">
                    <div className="text-sm font-medium text-white">{t('publish.xhs')}</div>
                    <div className="text-xs text-gray-400">{t('publish.xhsDesc')}</div>
                  </div>
                  <Chip size="sm" color="success" variant="flat">{t('publish.available')}</Chip>
                </Button>

                {/* 小黄鱼 */}
                <Button
                  className="w-full justify-start bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 opacity-60 cursor-not-allowed"
                  variant="flat"
                  isDisabled
                  startContent={
                    <div className="w-6 h-6 rounded bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center">
                      <Leaf className="w-3.5 h-3.5 text-white" />
                    </div>
                  }
                >
                  <div className="flex-1 text-left">
                    <div className="text-sm font-medium text-white">{t('publish.xhy')}</div>
                    <div className="text-xs text-gray-400">{t('publish.xhyDesc')}</div>
                  </div>
                  <Chip size="sm" color="default" variant="flat">{t('publish.comingSoon')}</Chip>
                </Button>

                {/* 知乎 */}
                <Button
                  className="w-full justify-start bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-500/30 opacity-60 cursor-not-allowed"
                  variant="flat"
                  isDisabled
                  startContent={
                    <div className="w-6 h-6 rounded bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                      <MessageCircle className="w-3.5 h-3.5 text-white" />
                    </div>
                  }
                >
                  <div className="flex-1 text-left">
                    <div className="text-sm font-medium text-white">{t('publish.zhihu')}</div>
                    <div className="text-xs text-gray-400">{t('publish.zhihuDesc')}</div>
                  </div>
                  <Chip size="sm" color="default" variant="flat">{t('publish.comingSoon')}</Chip>
                </Button>
              </CardBody>
            </Card>
          </div>
          </div>

          {/* 数据表格 */}
          <Card className="bg-white/5 backdrop-blur-xl border border-white/10">
            <CardHeader className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
                  <Database className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">{t('dashboard.latestData')}</h2>
                  <p className="text-xs text-gray-400">{t('dashboard.latestRecords')}</p>
                </div>
              </div>
              <Dropdown>
                <DropdownTrigger>
                  <Button
                    variant="flat"
                    size="sm"
                    startContent={<Download className="w-4 h-4" />}
                    className="bg-white/5 hover:bg-white/10"
                  >
                    {t('common.export')}
                  </Button>
                </DropdownTrigger>
                <DropdownMenu>
                  <DropdownItem key="json">{t('data.exportJson')}</DropdownItem>
                  <DropdownItem key="csv">{t('data.exportCsv')}</DropdownItem>
                  <DropdownItem key="excel">{t('data.exportExcel')}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </CardHeader>
            <Divider className="bg-white/10" />
            <CardBody className="overflow-x-auto">
              {dataLoading ? (
                <div className="flex justify-center py-8">
                  <Spinner color="secondary" />
                </div>
              ) : dataList.length === 0 ? (
                <div className="text-center py-8 text-gray-400">
                  {t('data.noData')}
                </div>
              ) : (
                <Table
                  aria-label={t('dashboard.latestData')}
                  classNames={{
                    wrapper: 'bg-transparent shadow-none',
                    th: 'bg-white/5 text-gray-300',
                    td: 'text-gray-300',
                  }}
                >
                  <TableHeader>
                    <TableColumn>{t('data.title')}</TableColumn>
                    <TableColumn>{t('data.author')}</TableColumn>
                    <TableColumn>{t('data.type')}</TableColumn>
                    <TableColumn>{t('data.likes')}</TableColumn>
                    <TableColumn>{t('common.actions')}</TableColumn>
                  </TableHeader>
                  <TableBody>
                    {dataList.map((item, index) => (
                      <TableRow key={item.note_id || item.id || index}>
                        <TableCell>
                          <div className="max-w-xs truncate">{item.title || item.desc || '-'}</div>
                        </TableCell>
                        <TableCell>{item.nickname || item.user_nickname || '-'}</TableCell>
                        <TableCell>
                          <Chip size="sm" variant="flat" className="bg-white/10">
                            {item.type === 'video' ? '视频' : item.type === 'normal' ? '图文' : item.type || 'note'}
                          </Chip>
                        </TableCell>
                        <TableCell>{item.liked_count || 0}</TableCell>
                        <TableCell>
                          <div className="flex gap-1">
                            <Tooltip content="查看详情">
                              <Button
                                isIconOnly
                                size="sm"
                                variant="flat"
                                className="bg-white/5 hover:bg-white/10"
                              >
                                <Eye className="w-3 h-3" />
                              </Button>
                            </Tooltip>
                            {item.note_url && (
                              <Tooltip content={t('common.openLink')}>
                                <Button
                                  isIconOnly
                                  size="sm"
                                  variant="flat"
                                  className="bg-white/5 hover:bg-white/10"
                                  onClick={() => window.open(item.note_url, '_blank')}
                                >
                                  <ExternalLink className="w-3 h-3" />
                                </Button>
                              </Tooltip>
                            )}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardBody>
          </Card>

          {/* 日志控制台 */}
          <Card
            className={`bg-white/5 backdrop-blur-xl border border-white/10 transition-all duration-300 ${
              isExpanded ? 'fixed inset-4 z-50' : ''
            }`}
          >
            <CardHeader className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center">
                  <Terminal className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-white">{t('dashboard.realtimeLogs')}</h2>
                  <p className="text-xs text-gray-400">{logs.length} {t('logs.entries')}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button
                  isIconOnly
                  size="sm"
                  variant="flat"
                  onClick={() => setIsPaused(!isPaused)}
                  className="bg-white/5 hover:bg-white/10"
                >
                  {isPaused ? (
                    <Play className="w-4 h-4 text-green-400" />
                  ) : (
                    <Pause className="w-4 h-4 text-yellow-400" />
                  )}
                </Button>
                <Button
                  isIconOnly
                  size="sm"
                  variant="flat"
                  onClick={clearLogs}
                  className="bg-white/5 hover:bg-white/10"
                >
                  <Trash2 className="w-4 h-4 text-gray-400" />
                </Button>
                <Button
                  isIconOnly
                  size="sm"
                  variant="flat"
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="bg-white/5 hover:bg-white/10"
                >
                  {isExpanded ? (
                    <Minimize2 className="w-4 h-4 text-gray-400" />
                  ) : (
                    <Maximize2 className="w-4 h-4 text-gray-400" />
                  )}
                </Button>
              </div>
            </CardHeader>
            <Divider className="bg-white/10" />
            <CardBody className={`p-0 ${isExpanded ? 'h-[calc(100vh-12rem)]' : 'h-64'}`}>
              <div className="h-full overflow-y-auto font-mono text-xs p-4 bg-black/30">
                {logs.length === 0 ? (
                  <div className="text-gray-500 text-center py-8">{t('logs.waiting')}</div>
                ) : (
                  logs.map((log) => (
                    <div
                      key={log.id}
                      className="flex gap-2 py-0.5 hover:bg-white/5 px-2 -mx-2 rounded group"
                    >
                      <span className="text-gray-500 select-none">
                        {formatLogTime(log.timestamp)}
                      </span>
                      <span className={`font-semibold w-16 ${LOG_COLORS[log.level]}`}>
                        [{log.level}]
                      </span>
                      <span className="text-gray-300 flex-1">{log.message}</span>
                      <Button
                        isIconOnly
                        size="sm"
                        variant="light"
                        className="opacity-0 group-hover:opacity-100 transition-opacity h-4 w-4 min-w-4"
                        onClick={() => copyToClipboard(log.message)}
                      >
                        <Copy className="w-3 h-3 text-gray-400" />
                      </Button>
                    </div>
                  ))
                )}
                <div ref={logsEndRef} />
              </div>
            </CardBody>
          </Card>
        </main>

        {/* 页脚 */}
        <footer className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-500 text-sm">
          <p>{t('common.copyright')}</p>
        </footer>
      </div>
    </div>
  );
}
