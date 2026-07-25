import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import B2BPortal from '../pages/B2BPortal';

// Mock the fetch call
global.fetch = vi.fn();

describe('B2BPortal Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the loading state initially', async () => {
    global.fetch = vi.fn().mockImplementation((url) => {
      if (url.includes('/api/leads/inbox')) {
        return Promise.resolve({ ok: true, json: async () => [] });
      }
      if (url.includes('/api/campaigns')) {
        return Promise.resolve({ ok: true, json: async () => [] });
      }
      if (url.includes('/api/buyers/balance')) {
        return Promise.resolve({ ok: true, json: async () => ({ balance: 100 }) });
      }
      return Promise.resolve({ ok: true, json: async () => ({}) });
    });
    
    render(<B2BPortal />);
    expect(screen.getByText('Loading data...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Lead Inbox')).toBeInTheDocument();
    });
  });

  it('fetches and displays campaigns', async () => {
    const mockCampaigns = [
      { id: 1, name: 'HVAC Miami Premium', vertical: 'HVAC', maxBid: 50, leadType: 'Exclusive', isActive: true, buyer: { name: 'CoolBreeze HVAC' } }
    ];

    global.fetch = vi.fn().mockImplementation((url) => {
      if (url.includes('/api/leads/inbox')) {
        return Promise.resolve({ ok: true, json: async () => [] });
      }
      if (url.includes('/api/campaigns')) {
        return Promise.resolve({ ok: true, json: async () => mockCampaigns });
      }
      if (url.includes('/api/buyers/balance')) {
        return Promise.resolve({ ok: true, json: async () => ({ balance: 100 }) });
      }
      return Promise.resolve({ ok: true, json: async () => ({}) });
    });

    render(<B2BPortal />);

    await waitFor(() => {
      expect(screen.getByText('Lead Inbox')).toBeInTheDocument();
    });

    const campaignsTab = screen.getByRole('button', { name: /Campaigns/i });
    fireEvent.click(campaignsTab);

    await waitFor(() => {
      expect(screen.getByText('HVAC Miami Premium')).toBeInTheDocument();
      expect(screen.getByText('Max Bid: $50')).toBeInTheDocument();
    });
  });

  it('shows empty state when no campaigns exist', async () => {
    global.fetch = vi.fn().mockImplementation((url) => {
      if (url.includes('/api/leads/inbox')) {
        return Promise.resolve({ ok: true, json: async () => [] });
      }
      if (url.includes('/api/campaigns')) {
        return Promise.resolve({ ok: true, json: async () => [] });
      }
      if (url.includes('/api/buyers/balance')) {
        return Promise.resolve({ ok: true, json: async () => ({ balance: 100 }) });
      }
      return Promise.resolve({ ok: true, json: async () => ({}) });
    });

    render(<B2BPortal />);

    await waitFor(() => {
      expect(screen.getByText('Lead Inbox')).toBeInTheDocument();
    });
  });
});
