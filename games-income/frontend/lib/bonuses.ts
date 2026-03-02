export interface Bonus {
  id: number;
  geo: string;
  type: 'casino' | 'betting';
  brand_id: string;
  brand_name: string;
  bonus_title: string;
  bonus_amount: string;
  bonus_type: string;
  wagering: string | null;
  conditions: string | null;
  affiliate_url: string;
  logo_url: string;
  rating: number;
  scraped_at: string;
  is_new?: boolean;
  is_expired?: boolean;
  is_active?: number;
  featured_providers?: string;
}

import bonusesData from '../data/bonuses.json';

export const STATIC_BONUSES: Bonus[] = bonusesData.bonuses as unknown as Bonus[];

export function getBonuses(type?: 'casino' | 'betting', geo: string = 'IN'): Bonus[] {
  const bonuses = bonusesData.bonuses as unknown as Bonus[];
  return bonuses.filter(
    b => (!type || b.type === type) && b.geo === geo.toUpperCase()
  );
}
