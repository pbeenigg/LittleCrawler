// 顶部导航栏组件
"use client";

import { useTheme } from "next-themes";
import {
  Button,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Chip,
} from "@nextui-org/react";
import { Sun, Moon, Languages, Activity } from "lucide-react";
import { useI18n } from "@/contexts/I18nContext";
import { useEffect, useState } from "react";
import { healthApi } from "@/lib/api";

export function Header() {
  const { theme, setTheme } = useTheme();
  const { t, locale, setLocale } = useI18n();
  const [mounted, setMounted] = useState(false);
  const [apiStatus, setApiStatus] = useState<"healthy" | "unhealthy" | "checking">("checking");

  useEffect(() => {
    setMounted(true);
    checkApiHealth();
    // 每30秒检查一次API状态
    const interval = setInterval(checkApiHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkApiHealth = async () => {
    try {
      await healthApi.check();
      setApiStatus("healthy");
    } catch {
      setApiStatus("unhealthy");
    }
  };

  if (!mounted) return null;

  return (
    <header className="h-16 bg-content1 border-b border-divider flex items-center justify-between px-6">
      {/* 左侧标题区域 */}
      <div className="flex items-center gap-4">
        {/* API状态指示器 */}
        <Chip
          color={apiStatus === "healthy" ? "success" : apiStatus === "unhealthy" ? "danger" : "warning"}
          variant="dot"
          size="sm"
        >
          {t("dashboard.apiStatus")}: {apiStatus === "checking" ? "..." : t(`dashboard.${apiStatus}`)}
        </Chip>
      </div>

      {/* 右侧工具栏 */}
      <div className="flex items-center gap-2">
        {/* 语言切换 */}
        <Dropdown>
          <DropdownTrigger>
            <Button isIconOnly variant="light" aria-label="Language">
              <Languages size={20} />
            </Button>
          </DropdownTrigger>
          <DropdownMenu
            aria-label="Language selection"
            selectedKeys={[locale]}
            selectionMode="single"
            onSelectionChange={(keys) => {
              const selected = Array.from(keys)[0] as "zh" | "en";
              setLocale(selected);
            }}
          >
            <DropdownItem key="zh">{t("common.chinese")}</DropdownItem>
            <DropdownItem key="en">{t("common.english")}</DropdownItem>
          </DropdownMenu>
        </Dropdown>

        {/* 主题切换 */}
        <Button
          isIconOnly
          variant="light"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          aria-label="Toggle theme"
        >
          {theme === "dark" ? <Sun size={20} /> : <Moon size={20} />}
        </Button>

        {/* 刷新API状态 */}
        <Button
          isIconOnly
          variant="light"
          onClick={checkApiHealth}
          aria-label="Refresh status"
        >
          <Activity size={20} />
        </Button>
      </div>
    </header>
  );
}
