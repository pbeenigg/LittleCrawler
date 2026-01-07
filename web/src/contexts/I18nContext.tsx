// 国际化Context - 提供多语言支持
"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import zhLocale from '@/locales/zh.json';
import enLocale from '@/locales/en.json';

type Locale = 'zh' | 'en';
type LocaleMessages = typeof zhLocale;

interface I18nContextType {
  locale: Locale;
  messages: LocaleMessages;
  setLocale: (locale: Locale) => void;
  t: (key: string, params?: Record<string, string | number>) => string;
}

const locales: Record<Locale, LocaleMessages> = {
  zh: zhLocale,
  en: enLocale,
};

const I18nContext = createContext<I18nContextType | undefined>(undefined);

// 获取嵌套对象的值
function getNestedValue(obj: any, path: string): string {
  return path.split('.').reduce((acc, part) => acc?.[part], obj) ?? path;
}

// 替换模板参数
function interpolate(str: string, params?: Record<string, string | number>): string {
  if (!params) return str;
  return str.replace(/\{(\w+)\}/g, (_, key) => String(params[key] ?? `{${key}}`));
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('zh');
  const [messages, setMessages] = useState<LocaleMessages>(zhLocale);

  useEffect(() => {
    // 从localStorage读取语言设置
    const savedLocale = localStorage.getItem('locale') as Locale;
    if (savedLocale && locales[savedLocale]) {
      setLocaleState(savedLocale);
      setMessages(locales[savedLocale]);
    }
  }, []);

  const setLocale = (newLocale: Locale) => {
    setLocaleState(newLocale);
    setMessages(locales[newLocale]);
    localStorage.setItem('locale', newLocale);
  };

  // 翻译函数
  const t = (key: string, params?: Record<string, string | number>): string => {
    const value = getNestedValue(messages, key);
    return interpolate(value, params);
  };

  return (
    <I18nContext.Provider value={{ locale, messages, setLocale, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error('useI18n must be used within I18nProvider');
  }
  return context;
}
