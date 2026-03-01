import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Games Income — Best Casino & Betting Bonuses India 2026',
    description: 'Compare casino and sports betting bonuses for Indian players. Auto-updated every 6 hours from top platforms.',
    icons: { icon: '/favicon.ico' },
};

import bonusesData from '../data/bonuses.json';

export default function RootLayout({ children }: { children: React.ReactNode }) {
    const lastUpdate = new Date(bonusesData.updated_at).toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
    });

    return (
        <html lang="en">
            <body className={`${inter.className} bg-[#0a0d1a] text-white`}>
                {/* Navigation */}
                <nav className="sticky top-0 z-50 bg-[#0a0d1a]/80 backdrop-blur-md border-b border-white/5">
                    <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
                        <Link href="/" className="flex items-center gap-2">
                            <span className="text-2xl font-black">
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-400">Games</span>
                                <span className="text-white">Income</span>
                            </span>
                        </Link>
                        <div className="hidden md:flex items-center gap-6 text-sm">
                            <Link href="/casino-bonuses" className="text-gray-400 hover:text-white transition-colors">
                                🎰 Casino Bonuses
                            </Link>
                            <Link href="/betting-bonuses" className="text-gray-400 hover:text-white transition-colors">
                                🏏 Betting Bonuses
                            </Link>
                        </div>
                        <div className="flex flex-col items-end gap-1">
                            <span className="flex items-center gap-1.5 text-[10px] uppercase font-bold tracking-wider text-green-400">
                                <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                                Updated {lastUpdate}
                            </span>
                            <span className="text-[9px] text-gray-500 font-medium">Automatic 12h Cycle</span>
                        </div>
                    </div>
                </nav>
                {children}
            </body>
        </html>
    );
}
