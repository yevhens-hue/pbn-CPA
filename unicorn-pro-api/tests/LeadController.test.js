const request = require('supertest');
const app = require('../index'); // The express app

// We can mock the PrismaClient and PingPostService if we want pure unit/isolated tests,
// but for an integration test, we can mock just the processAuction part or use a test DB.
// Let's mock Prisma to avoid hitting a real DB during testing.
jest.mock('../src/repositories/CampaignRepository', () => ({
  getActiveMatchingCampaigns: jest.fn().mockResolvedValue([
    {
      id: 1,
      vertical: 'HVAC',
      zipCodes: 'all',
      leadType: 'Exclusive',
      maxBid: 50,
      isActive: true,
      buyer: { id: 1, name: 'Buyer A', balance: 100 }
    }
  ])
}));

jest.mock('../src/repositories/LeadRepository', () => ({
  saveUnsoldLead: jest.fn().mockResolvedValue({ id: 1 }),
  saveSoldLeadWithTransactions: jest.fn().mockResolvedValue({ id: 1 })
}));

describe('POST /api/leads', () => {
  it('should return 201 and auction result when lead is submitted', async () => {
    const res = await request(app)
      .post('/api/leads')
      .send({
        name: 'John Doe',
        phone: '1234567890',
        email: 'test@example.com',
        serviceType: 'HVAC',
        zipCode: '10001',
        urgency: 'This Week',
        address: '123 Main St'
      });
    
    expect(res.statusCode).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.auctionResult).toBeDefined();
    // Because of our mock, it should find the $50 Exclusive campaign and win.
    expect(res.body.auctionResult.status).toBe('Exclusive');
  });

  it('should return 400 if validation fails', async () => {
    const res = await request(app)
      .post('/api/leads')
      .send({
        firstName: 'John'
        // missing required fields
      });
    
    expect(res.statusCode).toBe(400);
    expect(res.body.error).toBeDefined();
  });
});
