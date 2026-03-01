// Frontend-only data layer — reads from static data
// (The SQLite DB is only used by the Python scraper backend)

export interface Bonus {
  id: number;
  geo: string;
  type: 'casino' | 'betting';
  brand_id: string;
  brand_name: string;
  bonus_title: string;
  bonus_amount: string;
  bonus_type: string;
  wagering: string;
  conditions: string;
  affiliate_url: string;
  logo_url: string;
  rating: number;
  scraped_at: string;
}

// Hardcoded fallback data for when DB is not ready
export const STATIC_BONUSES: Bonus[] = [
  {
    id: 1, geo: 'IN', type: 'casino', brand_id: '1win',
    brand_name: '1Win', bonus_title: 'Welcome Package',
    bonus_amount: '500% up to ₹75,000', bonus_type: 'welcome',
    wagering: '35x', conditions: 'Min deposit ₹300. New players only.',
    affiliate_url: 'https://1win.com/en/?ref=YOUR_REF',
    logo_url: '/logos/1win.png', rating: 4.7,
    scraped_at: new Date().toISOString()
  },
  {
    id: 2, geo: 'IN', type: 'casino', brand_id: '1xbet',
    brand_name: '1xBet', bonus_title: 'First Deposit Bonus',
    bonus_amount: '100% up to ₹10,000', bonus_type: 'welcome',
    wagering: '5x', conditions: 'Min deposit ₹100. Valid 30 days.',
    affiliate_url: 'https://refpa14435.com/L?tag=d_5300195m_1236c_&site=5300195&ad=1236',
    logo_url: '/logos/1xbet.png', rating: 4.5,
    scraped_at: new Date().toISOString()
  },
  {
    id: 3, geo: 'IN', type: 'casino', brand_id: 'parimatch',
    brand_name: 'Parimatch', bonus_title: 'Welcome Bonus',
    bonus_amount: '150% up to ₹20,000', bonus_type: 'welcome',
    wagering: '30x', conditions: 'Min deposit ₹300.',
    affiliate_url: 'https://parimatch.in/?ref=YOUR_REF',
    logo_url: '/logos/parimatch.png', rating: 4.4,
    scraped_at: new Date().toISOString()
  },
  {
    id: 4, geo: 'IN', type: 'casino', brand_id: 'betway',
    brand_name: 'Betway', bonus_title: 'Welcome Bonus',
    bonus_amount: '100% up to ₹10,000', bonus_type: 'welcome',
    wagering: '30x', conditions: 'Min deposit ₹500. Valid for 7 days.',
    affiliate_url: 'https://betway.in/?ref=YOUR_REF',
    logo_url: '/logos/betway.png', rating: 4.3,
    scraped_at: new Date().toISOString()
  },
  {
    id: 5, geo: 'IN', type: 'casino', brand_id: 'melbet',
    brand_name: 'Melbet', bonus_title: '100% First Deposit Bonus',
    bonus_amount: '100% up to ₹10,400', bonus_type: 'welcome',
    wagering: '14x', conditions: 'Min deposit ₹100. Code: MLBVIP.',
    affiliate_url: 'https://melbet.in/?ref=YOUR_REF',
    logo_url: '/logos/melbet.png', rating: 4.2,
    scraped_at: new Date().toISOString()
  },
  {
    id: 6, geo: 'IN', type: 'betting', brand_id: '1xbet_sports',
    brand_name: '1xBet Sports', bonus_title: 'Sports Welcome Bonus',
    bonus_amount: '100% up to ₹10,000', bonus_type: 'sports',
    wagering: '5x', conditions: 'Bet on odds ≥ 1.40. Min deposit ₹100.',
    affiliate_url: 'https://refpa14435.com/L?tag=d_5300195m_1236c_&site=5300195&ad=1236',
    logo_url: '/logos/1xbet.png', rating: 4.6,
    scraped_at: new Date().toISOString()
  },
  {
    id: 7, geo: 'IN', type: 'betting', brand_id: '10cric',
    brand_name: '10CRIC', bonus_title: 'Cricket Betting Bonus',
    bonus_amount: '100% up to ₹10,000', bonus_type: 'sports',
    wagering: '8x', conditions: 'India-focused. Cricket specialist.',
    affiliate_url: 'https://www.10cric.com/?ref=YOUR_REF',
    logo_url: '/logos/10cric.png', rating: 4.5,
    scraped_at: new Date().toISOString()
  },
  {
    id: 8, geo: 'IN', type: 'betting', brand_id: 'dafabet',
    brand_name: 'Dafabet', bonus_title: 'Sports First Deposit Bonus',
    bonus_amount: '170% up to ₹16,000', bonus_type: 'sports',
    wagering: '12x', conditions: 'Valid for sports markets only.',
    affiliate_url: 'https://www.dafabet.com/?ref=YOUR_REF',
    logo_url: '/logos/dafabet.png', rating: 4.3,
    scraped_at: new Date().toISOString()
  },
];


export function getBonuses(type?: 'casino' | 'betting', geo: string = 'IN'): Bonus[] {
  return STATIC_BONUSES.filter(
    b => (!type || b.type === type) && b.geo === geo.toUpperCase()
  );
}
