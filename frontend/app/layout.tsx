import type { ReactNode } from 'react';
import './globals.css';
import { Header } from '../components/Header';
import { LanguageProvider } from '../components/LanguageProvider';

export const metadata = {
  title: 'ILikeToHave',
  description: 'Wishlist PWA',
  manifest: '/manifest.json',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#0ea5e9" />
      </head>
      <body>
        <LanguageProvider>
          <Header />
          <main>{children}</main>
        </LanguageProvider>
      </body>
    </html>
  );
}
