import Link from 'next/link';
import { STATIC_BONUSES } from '@/lib/bonuses';
import BonusCard from '@/components/BonusCard';

export const metadata = {
    title: 'Games Income — Best Casino & Betting Bonuses in India 2026',
    description: 'Compare the latest casino bonuses and sports betting offers for Indian players. Verified, up-to-date deals from top platforms.',
};

export default function HomePage() {
    const topCasino = STATIC_BONUSES.filter(b => b.type === 'casino').slice(0, 3);
    const topBetting = STATIC_BONUSES.filter(b => b.type === 'betting').slice(0, 3);

    return (
        <main className="min-h-screen bg-[#0a0d1a]">
            {/* Hero */}
            <section className="relative overflow-hidden py-20 px-4 text-center">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-900/30 via-[#0a0d1a] to-indigo-900/20 pointer-events-none" />
                <div className="absolute top-10 left-1/4 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl" />
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl" />
                <div className="relative max-w-4xl mx-auto">
                    <span className="inline-block bg-gradient-to-r from-purple-500 to-indigo-400 text-white text-xs font-bold uppercase tracking-widest px-4 py-1.5 rounded-full mb-6">
                        🇮🇳 Updated Daily · India Edition 2026
                    </span>
                    <h1 className="text-5xl md:text-6xl font-black text-white mb-6 leading-tight">
                        Best Casino & Betting<br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-300">
                            Bonuses in India
                        </span>
                    </h1>
                    <p className="text-gray-400 text-xl max-w-2xl mx-auto mb-10">
                        We automatically track and verify the latest bonus offers from India's top platforms.
                        Real deals, updated every 6 hours.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/casino-bonuses"
                            className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold px-8 py-4 rounded-xl transition-all transform hover:scale-105 shadow-lg shadow-purple-900/30">
                            🎰 Casino Bonuses
                        </Link>
                        <Link href="/betting-bonuses"
                            className="bg-white/5 hover:bg-white/10 border border-white/10 text-white font-bold px-8 py-4 rounded-xl transition-all transform hover:scale-105">
                            🏏 Betting Bonuses
                        </Link>
                    </div>
                </div>
            </section>

            {/* Stats Bar */}
            <section className="border-y border-white/5 bg-white/3 py-6 px-4">
                <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    {[
                        { value: '8+', label: 'Verified Platforms' },
                        { value: '₹75,000', label: 'Max Welcome Bonus' },
                        { value: '6h', label: 'Update Frequency' },
                        { value: '100%', label: 'Free to Use' },
                    ].map((stat) => (
                        <div key={stat.label}>
                            <div className="text-2xl font-black text-purple-400">{stat.value}</div>
                            <div className="text-gray-500 text-sm mt-1">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Top Casino Bonuses */}
            <section className="py-16 px-4 max-w-6xl mx-auto">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h2 className="text-3xl font-black text-white">🎰 Top Casino Bonuses</h2>
                        <p className="text-gray-500 mt-1">Best welcome offers for Indian casino players</p>
                    </div>
                    <Link href="/casino-bonuses" className="text-purple-400 hover:text-purple-300 text-sm font-semibold">
                        View all →
                    </Link>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {topCasino.map((bonus, i) => (
                        <BonusCard key={bonus.id} bonus={bonus} rank={i + 1} />
                    ))}
                </div>
            </section>

            {/* Top Betting Bonuses */}
            <section className="pb-16 px-4 max-w-6xl mx-auto">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h2 className="text-3xl font-black text-white">🏏 Top Betting Bonuses</h2>
                        <p className="text-gray-500 mt-1">Best sportsbook offers for IPL & cricket betting</p>
                    </div>
                    <Link href="/betting-bonuses" className="text-purple-400 hover:text-purple-300 text-sm font-semibold">
                        View all →
                    </Link>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {topBetting.map((bonus, i) => (
                        <BonusCard key={bonus.id} bonus={bonus} rank={i + 1} />
                    ))}
                </div>
            </section>

            {/* Trust Section */}
            <section className="py-12 px-4 border-t border-white/5 bg-white/2">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-2xl font-bold text-white mb-8">Why Trust Games Income?</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {[
                            { icon: '🔄', title: 'Auto-Updated', desc: 'Our scraper checks bonuses every 6 hours so you always get the latest offers.' },
                            { icon: '✅', title: 'Expert Verified', desc: 'Each platform is reviewed for licensing, payment speed, and support quality.' },
                            { icon: '🇮🇳', title: 'India Focused', desc: 'All bonuses are verified for INR deposits via UPI, Paytm, and PhonePe.' },
                        ].map((item) => (
                            <div key={item.title} className="bg-white/5 border border-white/10 rounded-xl p-6">
                                <div className="text-3xl mb-3">{item.icon}</div>
                                <h3 className="text-white font-bold mb-2">{item.title}</h3>
                                <p className="text-gray-500 text-sm">{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-8 px-4 border-t border-white/5 text-center text-gray-600 text-sm">
                <p>© 2026 Games Income. For adults 18+ only. Gambling can be addictive — please play responsibly.</p>
                <p className="mt-2">This site contains affiliate links. We may earn commission when you sign up via our links.</p>
            </footer>
        </main>
    );
}
