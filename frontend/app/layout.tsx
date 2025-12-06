import type { ReactNode } from 'react';
import './globals.css';
import { Header } from '../components/Header';

export const metadata = {
  title: 'iliketohave',
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
        <Header />
        <main>{children}</main>
        <script
          dangerouslySetInnerHTML={{
            __html: `if ('serviceWorker' in navigator) { window.addEventListener('load', function() { navigator.serviceWorker.register('/sw.js').catch(function(e){console.error('SW registration failed', e); }); }); }`,
          }}
        />
      </body>
    </html>
  );
}
