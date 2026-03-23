import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Script from 'next/script';
import Link from 'next/link';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

const GA_ID = process.env.NEXT_PUBLIC_GA_ID || 'G-XXXXXXXXXX';

export const metadata: Metadata = {
    title: 'Games Income — Best Casino & Betting Bonuses 2026',
    description: 'Compare casino and sports betting bonuses across India, Turkey, and Brazil. Auto-updated every 6 hours. Expert insights and AI-powered guides.',
    icons: {
        icon: [
            { url: '/favicon.svg', type: 'image/svg+xml' },
        ],
        shortcut: '/favicon.svg',
        apple: '/favicon.svg',
    },
    verification: {
        // Add your Google Search Console verification token here
        google: process.env.NEXT_PUBLIC_GSC_VERIFICATION || '',
    },
    openGraph: {
        siteName: 'Games Income',
        type: 'website',
    },
};

import bonusesData from '../data/bonuses.json';

export default function RootLayout({ children }: { children: React.ReactNode }) {
    const lastUpdate = new Date(bonusesData.updated_at).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });

    return (
        <html lang="en">
            <body className={`${inter.className} bg-[#0a0d1a] text-white`}>
                {/* Google Analytics */}
                <Script
                    strategy="afterInteractive"
                    src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
                />
                <Script id="ga-init" strategy="afterInteractive">
                    {`
                        window.dataLayer = window.dataLayer || [];
                        function gtag(){dataLayer.push(arguments);}
                        gtag('js', new Date());
                        gtag('config', '${GA_ID}', {
                            page_path: window.location.pathname,
                            anonymize_ip: true
                        });
                    `}
                </Script>

                {/* Navigation */}
                <nav className="sticky top-0 z-50 bg-[#0a0d1a]/90 backdrop-blur-md border-b border-white/5">
                    <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
                        <Link href="/" className="flex items-center gap-2 flex-shrink-0">
                            <span className="text-xl font-black tracking-tight">
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-400">Games</span>
                                <span className="text-white">Income</span>
                            </span>
                        </Link>

                        <div className="hidden md:flex items-center gap-1 text-xs font-bold">
                            <Link href="/all-bonuses" className="text-gray-400 hover:text-white hover:bg-white/5 transition-all px-3 py-2 rounded-lg">
                                📊 All Bonuses
                            </Link>
                            <Link href="/casino-bonuses" className="text-gray-400 hover:text-white hover:bg-white/5 transition-all px-3 py-2 rounded-lg">
                                🎰 Casino
                            </Link>
                            <Link href="/betting-bonuses" className="text-gray-400 hover:text-white hover:bg-white/5 transition-all px-3 py-2 rounded-lg">
                                🏏 Betting
                            </Link>
                            <Link href="/blog" className="text-gray-400 hover:text-white hover:bg-white/5 transition-all px-3 py-2 rounded-lg">
                                ✍️ Blog
                            </Link>
                            <Link href="https://luckybetvip.com" target="_blank" rel="noopener noreferrer" className="text-yellow-400 hover:text-yellow-300 hover:bg-yellow-500/10 transition-all px-3 py-2 rounded-lg border border-yellow-500/20">
                                ✈️ Aviator Strategies
                            </Link>
                        </div>

                        <div className="flex items-center gap-2 flex-shrink-0">
                            <span className="flex items-center gap-1.5 text-[10px] uppercase font-bold tracking-wider text-green-400">
                                <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                                <span className="hidden sm:inline">Live · {lastUpdate}</span>
                                <span className="inline sm:hidden">Live</span>
                            </span>
                        </div>
                    </div>
                </nav>

                {children}
            </body>
        </html>
    );
}
