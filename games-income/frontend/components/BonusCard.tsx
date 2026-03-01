'use client';
import type { Bonus } from '@/lib/bonuses';

const BONUS_TYPE_LABELS: Record<string, string> = {
    welcome: '🎁 Welcome',
    reload: '🔁 Reload',
    cashback: '💸 Cashback',
    free_spins: '🎡 Free Spins',
    sports: '🏆 Sports',
    vip: '👑 VIP',
    other: '🎯 Special',
};

const RANK_COLORS = ['from-yellow-500 to-amber-400', 'from-gray-400 to-gray-300', 'from-orange-700 to-orange-600'];

export default function BonusCard({ bonus, rank }: { bonus: Bonus; rank?: number }) {
    return (
        <div className="group relative bg-white/5 hover:bg-white/8 border border-white/10 hover:border-purple-500/50 rounded-2xl p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-purple-900/20">

            {/* Rank badge */}
            {rank && rank <= 3 && (
                <div className={`absolute -top-3 -right-3 w-8 h-8 rounded-full bg-gradient-to-br ${RANK_COLORS[rank - 1]} flex items-center justify-center text-white font-black text-xs shadow-lg`}>
                    #{rank}
                </div>
            )}

            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center overflow-hidden flex-shrink-0">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                        src={bonus.logo_url}
                        alt={bonus.brand_name}
                        className="w-6 h-6 object-contain"
                        onError={(e) => { (e.target as HTMLImageElement).src = '/logos/default.png'; }}
                    />
                </div>
                <div className="flex-1 min-w-0">
                    <h3 className="text-white font-bold text-sm truncate">{bonus.brand_name}</h3>
                    <div className="flex items-center gap-1 mt-0.5">
                        {[...Array(5)].map((_, i) => (
                            <span key={i} className={`text-xs ${i < Math.round(bonus.rating) ? 'text-yellow-400' : 'text-gray-600'}`}>★</span>
                        ))}
                        <span className="text-gray-500 text-xs ml-1">{bonus.rating.toFixed(1)}</span>
                    </div>
                </div>
                <span className="text-xs bg-purple-900/50 text-purple-300 px-2 py-0.5 rounded-full flex-shrink-0">
                    {BONUS_TYPE_LABELS[bonus.bonus_type] || '🎯 Bonus'}
                </span>
            </div>

            {/* Bonus Amount - the hero */}
            <div className="bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-xl p-4 mb-4 text-center">
                <div className="text-xs text-purple-400 mb-1 font-semibold uppercase tracking-wider">{bonus.bonus_title}</div>
                <div className="text-2xl font-black text-white leading-tight">{bonus.bonus_amount}</div>
            </div>

            {/* Details */}
            <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Wagering:</span>
                    <span className="text-gray-300 font-semibold">{bonus.wagering || 'N/A'}</span>
                </div>
                <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Conditions:</span>
                    <span className="text-gray-400 text-right text-xs max-w-[180px] leading-tight">{bonus.conditions}</span>
                </div>
            </div>

            {/* CTA */}
            <a
                href={bonus.affiliate_url}
                target="_blank"
                rel="nofollow sponsored noopener noreferrer"
                className="block w-full text-center bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold py-3 px-4 rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg shadow-purple-900/20 text-sm"
            >
                Claim Bonus via UPI →
            </a>

            <p className="text-xs text-gray-600 text-center mt-2">18+ | T&Cs Apply | Play Responsibly</p>
        </div>
    );
}
