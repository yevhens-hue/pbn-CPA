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

import bonusesData from '../data/bonuses.json';

export const STATIC_BONUSES: Bonus[] = bonusesData.bonuses as Bonus[];

export function getBonuses(type?: 'casino' | 'betting', geo: string = 'IN'): Bonus[] {
  const bonuses = (bonusesData.bonuses as Bonus[]) || STATIC_BONUSES;
  return bonuses.filter(
    b => (!type || b.type === type) && b.geo === geo.toUpperCase()
  );
}
