// 登录页面 - 炫酷风格
"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardHeader,
  CardBody,
  Input,
  Button,
} from "@nextui-org/react";
import { Eye, EyeOff, Zap, Sun, Moon, Globe } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useI18n } from "@/contexts/I18nContext";
import { useTheme } from "next-themes";

export default function LoginPage() {
  const router = useRouter();
  const { login, isAuthenticated, isLoading: authLoading } = useAuth();
  const { t, locale, setLocale } = useI18n();
  const { theme, setTheme } = useTheme();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      router.replace("/dashboard");
    }
  }, [isAuthenticated, authLoading, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError(t("login.error.required"));
      return;
    }

    setIsLoading(true);
    try {
      await login({ username, password });
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || t("login.error.invalid"));
    } finally {
      setIsLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  const toggleLocale = () => {
    setLocale(locale === "zh" ? "en" : "zh");
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center p-4 relative overflow-hidden">
      {/* 背景装饰 */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse" />
        <div className="absolute top-1/3 right-1/4 w-60 h-60 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" />
      </div>

      {/* 顶部工具栏 */}
      <div className="absolute top-4 right-4 flex gap-2 z-10">
        <Button
          isIconOnly
          variant="flat"
          onClick={toggleTheme}
          aria-label="Toggle theme"
          className="bg-white/10 hover:bg-white/20"
        >
          {theme === "dark" ? <Sun size={18} className="text-yellow-400" /> : <Moon size={18} className="text-gray-300" />}
        </Button>
        <Button
          isIconOnly
          variant="flat"
          onClick={toggleLocale}
          aria-label="Toggle language"
          className="bg-white/10 hover:bg-white/20"
        >
          <Globe size={18} className="text-gray-300" />
        </Button>
      </div>

      {/* 登录卡片 */}
      <Card className="w-full max-w-md bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl z-10">
        <CardHeader className="flex flex-col items-center gap-4 pt-10 pb-6">
          <div className="relative">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
              <Zap size={36} className="text-white" />
            </div>
            <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-slate-900 animate-pulse" />
          </div>
          <div className="text-center">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              LittleCrawler
            </h1>
            <p className="text-gray-400 mt-2 text-sm">{t("login.subtitle")}</p>
          </div>
        </CardHeader>
        <CardBody className="px-8 py-6">
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <Input
              label={t("common.username")}
              placeholder={t("login.placeholder.username")}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              classNames={{
                inputWrapper: "bg-white/5 border-white/10 hover:bg-white/10 group-data-[focused=true]:bg-white/10",
                label: "text-gray-400",
                input: "text-white placeholder:text-gray-500",
              }}
            />
            <Input
              label={t("common.password")}
              placeholder={t("login.placeholder.password")}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type={showPassword ? "text" : "password"}
              autoComplete="current-password"
              classNames={{
                inputWrapper: "bg-white/5 border-white/10 hover:bg-white/10 group-data-[focused=true]:bg-white/10",
                label: "text-gray-400",
                input: "text-white placeholder:text-gray-500",
              }}
              endContent={
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="focus:outline-none"
                >
                  {showPassword ? (
                    <EyeOff className="text-gray-400 hover:text-gray-300 transition-colors" size={18} />
                  ) : (
                    <Eye className="text-gray-400 hover:text-gray-300 transition-colors" size={18} />
                  )}
                </button>
              }
            />

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-2">
                <p className="text-red-400 text-sm text-center">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              size="lg"
              className="mt-2 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-shadow"
              isLoading={isLoading}
            >
              {t("common.login")}
            </Button>
          </form>
          
          {/* 默认账号提示 */}
          <div className="mt-6 text-center">
            <p className="text-gray-500 text-xs">
              默认账号：admin / admin123
            </p>
          </div>
        </CardBody>
      </Card>

      {/* 版本号 */}
      <p className="mt-6 text-gray-500 text-sm z-10">LittleCrawler v1.0 </p>
    </div>
  );
}
