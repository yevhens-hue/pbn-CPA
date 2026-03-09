import { getBonuses } from '@/lib/bonuses';
import BonusCard from '@/components/BonusCard';

export const metadata = {
    title: 'Best Casino Bonuses in India 2026 | Games Income',
    description: 'Compare the top casino welcome bonuses for Indian players. Get ₹75,000+ in bonuses from 1Win, 1xBet, Parimatch and more. Updated daily.',
};

export default function CasinoBonusesPage() {
    const bonuses = getBonuses('casino', 'IN');

    return (
        <main className="min-h-screen bg-[#0a0d1a] py-12 px-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <span className="inline-block bg-purple-900/50 text-purple-300 text-xs font-bold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
                        🎰 Casino Bonuses · India · 2026
                    </span>
                    <h1 className="text-4xl md:text-5xl font-black text-white mb-4">
                        Best Casino Bonuses<br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-300">
                            for Indian Players
                        </span>
                    </h1>
                    <p className="text-gray-400 max-w-2xl mx-auto">
                        All bonuses verified for INR deposits via UPI, Paytm & PhonePe.
                        Updated every 6 hours by our automated tracker.
                    </p>
                </div>

                {/* Filter bar */}
                <div className="flex flex-wrap gap-2 justify-center mb-8">
                    {['All', 'Welcome', 'Free Spins', 'Cashback', 'Reload'].map(f => (
                        <button key={f}
                            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all ${f === 'All'
                                ? 'bg-purple-600 text-white'
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

                {/* SEO text block */}
                <div className="mt-16 bg-white/3 border border-white/5 rounded-2xl p-8">
                    <h2 className="text-xl font-bold text-white mb-4">How to Choose the Best Casino Bonus in India</h2>
                    <div className="text-gray-500 text-sm space-y-3 leading-relaxed">
                        <p>When comparing casino bonus offers for Indian players, the most important factors are the <strong className="text-gray-400">wagering requirements</strong> (how many times you must bet the bonus before withdrawing), the <strong className="text-gray-400">minimum deposit</strong> in INR, and whether the casino accepts <strong className="text-gray-400">UPI and Paytm</strong> for instant payouts.</p>
                        <p>Our tracker automatically monitors bonus pages from the top licensed platforms every 6 hours, ensuring you always see the latest, active offers — not expired promotions from months ago.</p>
                    </div>
                </div>

                {/* Disclaimer */}
                <p className="text-center text-gray-700 text-xs mt-8">
                    18+ only. Gambling can be addictive. This site contains affiliate links — we may earn a commission when you sign up via our links. Bonus terms and availability may change. Always check the operator's site for current T&Cs.
                </p>
            </div>
        </main>
    );
}
