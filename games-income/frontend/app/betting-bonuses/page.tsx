import { getBonuses } from '@/lib/bonuses';
import BonusCard from '@/components/BonusCard';

export const metadata = {
    title: 'Best Sports Betting Bonuses in India 2026 | Games Income',
    description: 'Top sportsbook bonus offers for Indian bettors. Cricket, IPL, and sports betting bonuses from 1xBet, 10CRIC, Dafabet and more.',
};

export default function BettingBonusesPage() {
    const bonuses = getBonuses('betting', 'IN');

    return (
        <main className="min-h-screen bg-[#0a0d1a] py-12 px-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <span className="inline-block bg-indigo-900/50 text-indigo-300 text-xs font-bold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
                        🏏 Betting Bonuses · India · 2026
                    </span>
                    <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
                        Best Betting Bonuses<br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-blue-300">
                            for Cricket & IPL 2026
                        </span>
                    </h1>
                    <p className="text-gray-400 max-w-2xl mx-auto">
                        Exclusively curated sportsbook bonuses for IPL, cricket, kabaddi, and football betting.
                        Supports INR via UPI and Paytm.
                    </p>
                </div>

                {/* Sports filter bar */}
                <div className="flex flex-wrap gap-2 justify-center mb-8">
                    {['All Sports', '🏏 Cricket', '⚽ Football', '🏀 Basketball', '🎾 Tennis', '🏉 Kabaddi'].map(f => (
                        <button key={f}
                            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${f === 'All Sports'
                                ? 'bg-indigo-600 text-white'
                                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white border border-white/10'
                                }`}>
                            {f}
                        </button>
                    ))}
                </div>

                {/* Bonus Cards Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {bonuses.map((bonus, i) => (
                        <BonusCard key={bonus.id} bonus={bonus} rank={i + 1} />
                    ))}
                </div>

                {/* SEO text */}
                <div className="mt-16 bg-white/3 border border-white/5 rounded-2xl p-8">
                    <h2 className="text-xl font-bold text-white mb-4">Sports Betting Bonuses for India: What to Look For</h2>
                    <div className="text-gray-500 text-sm space-y-3 leading-relaxed">
                        <p>For cricket betting in India, the best bonus offers combine a generous <strong className="text-gray-400">first deposit match</strong> with low wagering requirements. Look for platforms that offer <strong className="text-gray-400">IPL-specific promotions</strong> during the tournament season, as these often have better value than standard welcome offers.</p>
                        <p>All platforms listed here support <strong className="text-gray-400">instant INR deposits via UPI</strong>, and most allow withdrawals to Paytm wallets within 1-4 hours. Our tracker verifies each bonus is currently active before displaying it.</p>
                    </div>
                </div>

                <p className="text-center text-gray-700 text-xs mt-8">
                    18+ only. Sports betting involves risk. This site contains affiliate links. Always check the operator's site for current T&Cs.
                </p>
            </div>
        </main>
    );
}
