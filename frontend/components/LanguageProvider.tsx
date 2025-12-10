'use client';

import { useEffect, useState } from 'react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../lib/i18n';

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const stored = typeof window !== 'undefined'
      ? window.localStorage.getItem('lang')
      : null;
    const initial = stored || 'en';
    i18n.changeLanguage(initial).finally(() => setReady(true));
  }, []);

  if (!ready) return null;

  return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>;
}
