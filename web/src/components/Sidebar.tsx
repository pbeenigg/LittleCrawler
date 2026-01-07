// 侧边栏导航组件
"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import {
  Bug,
  LayoutDashboard,
  Webhook,
  Database,
  ScrollText,
  Settings,
  LogOut,
} from "lucide-react";
import { Button, Tooltip } from "@nextui-org/react";
import { useI18n } from "@/contexts/I18nContext";
import { useAuth } from "@/contexts/AuthContext";

interface NavItem {
  key: string;
  href: string;
  icon: React.ReactNode;
}

export function Sidebar() {
  const pathname = usePathname();
  const { t } = useI18n();
  const { logout, user } = useAuth();

  const navItems: NavItem[] = [
    {
      key: "dashboard",
      href: "/dashboard",
      icon: <LayoutDashboard size={22} />,
    },
    {
      key: "crawler",
      href: "/dashboard/crawler",
      icon: <Webhook size={22} />,
    },
    {
      key: "data",
      href: "/dashboard/data",
      icon: <Database size={22} />,
    },
    {
      key: "logs",
      href: "/dashboard/logs",
      icon: <ScrollText size={22} />,
    },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-16 lg:w-64 bg-content1 border-r border-divider flex flex-col z-40">
      {/* Logo */}
      <div className="h-16 flex items-center justify-center lg:justify-start px-4 border-b border-divider">
        <Bug className="text-primary" size={28} />
        <span className="hidden lg:block ml-2 font-bold text-lg">
          {t("common.appName")}
        </span>
      </div>

      {/* 导航菜单 */}
      <nav className="flex-1 py-4">
        <ul className="space-y-1 px-2">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.key}>
                <Tooltip
                  content={t(`nav.${item.key}`)}
                  placement="right"
                  className="lg:hidden"
                >
                  <Link href={item.href}>
                    <div
                      className={`
                        flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors
                        ${
                          isActive
                            ? "bg-primary text-primary-foreground"
                            : "hover:bg-default-100 text-default-600"
                        }
                      `}
                    >
                      {item.icon}
                      <span className="hidden lg:block">
                        {t(`nav.${item.key}`)}
                      </span>
                    </div>
                  </Link>
                </Tooltip>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* 底部用户区域 */}
      <div className="border-t border-divider p-4">
        <div className="hidden lg:flex items-center justify-between mb-2">
          <span className="text-sm text-default-500 truncate">
            {user?.username}
          </span>
        </div>
        <Tooltip content={t("common.logout")} placement="right">
          <Button
            isIconOnly
            variant="light"
            className="w-full lg:w-auto"
            onClick={logout}
          >
            <LogOut size={20} />
            <span className="hidden lg:inline ml-2">{t("common.logout")}</span>
          </Button>
        </Tooltip>
      </div>
    </aside>
  );
}
