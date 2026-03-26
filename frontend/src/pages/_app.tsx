// src/pages/_app.tsx
import React from 'react';
import { AppProps } from 'next/app';
import { AuthProvider } from '@/hooks/useAuth';
import '@/styles/globals.css';
import Navbar from '@/components/Navbar';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main>
          <Component {...pageProps} />
        </main>
      </div>
    </AuthProvider>
  );
}

export default MyApp;