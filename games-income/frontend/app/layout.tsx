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

export default function RootLayout({ children }: { children: React.ReactNode }) {
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
                        <div className="flex items-center gap-3">
                            <span className="hidden sm:flex items-center gap-1.5 text-xs text-green-400 bg-green-900/30 border border-green-500/20 px-3 py-1.5 rounded-full">
                                <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                                Live Updates
                            </span>
                        </div>
                    </div>
                </nav>
                {children}
            </body>
        </html>
    );
}
