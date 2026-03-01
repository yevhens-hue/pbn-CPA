import { NextRequest, NextResponse } from 'next/server';
import { STATIC_BONUSES } from '@/lib/bonuses';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const type = searchParams.get('type') as 'casino' | 'betting' | null;
  const geo = (searchParams.get('geo') || 'IN').toUpperCase();

  const bonuses = STATIC_BONUSES.filter(b => {
    if (b.geo !== geo) return false;
    if (type && b.type !== type) return false;
    return true;
  });

  return NextResponse.json({
    updated_at: new Date().toISOString(),
    geo,
    type: type || 'all',
    count: bonuses.length,
    bonuses,
  });
}
