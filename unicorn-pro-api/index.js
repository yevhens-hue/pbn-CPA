const express = require('express');
const cors = require('cors');
const { PrismaClient } = require('@prisma/client');
const app = express();
const prisma = new PrismaClient();

app.use(cors());
app.use(express.json());

const LeadController = require('./src/controllers/LeadController');

// ---------------------------------------------------------
// PING-POST ENGINE: Handle new leads
// ---------------------------------------------------------
app.post('/api/leads', LeadController.submitLead);


// ---------------------------------------------------------
// B2B PORTAL API: Inbox & Campaigns
// ---------------------------------------------------------

// Helper: For MVP we hardcode buyerId = 1 (HVAC Masters LLC) to simulate login
const DEMO_BUYER_ID = 1;

// Get buyer wallet balance
app.get('/api/buyers/balance', async (req, res) => {
  const buyer = await prisma.buyer.findUnique({ where: { id: DEMO_BUYER_ID } });
  res.json({ balance: buyer.balance });
});

// Get Inbox Leads
app.get('/api/leads/inbox', async (req, res) => {
  const purchases = await prisma.leadPurchase.findMany({
    where: { buyerId: DEMO_BUYER_ID },
    include: { lead: true },
    orderBy: { createdAt: 'desc' }
  });

  const inbox = purchases.map(p => ({
    id: p.lead.id,
    purchaseId: p.id,
    name: p.lead.name,
    type: p.lead.serviceType,
    zip: p.lead.zipCode,
    urgency: p.lead.urgency,
    status: p.lead.status,
    price: p.price,
    time: p.createdAt,
    phone: p.lead.phone,
    email: p.lead.email
  }));

  res.json(inbox);
});

// Get Campaigns
app.get('/api/campaigns', async (req, res) => {
  const campaigns = await prisma.campaign.findMany({
    where: { buyerId: DEMO_BUYER_ID },
    orderBy: { createdAt: 'desc' }
  });
  res.json(campaigns);
});

// Toggle Campaign
app.post('/api/campaigns/:id/toggle', async (req, res) => {
  const { id } = req.params;
  const campaign = await prisma.campaign.findUnique({ where: { id: parseInt(id) } });
  const updated = await prisma.campaign.update({
    where: { id: parseInt(id) },
    data: { isActive: !campaign.isActive }
  });
  res.json(updated);
});


// Start server (only if not in Vercel production environment)
if (process.env.NODE_ENV !== 'production') {
  const PORT = process.env.PORT || 3001;
  app.listen(PORT, () => {
    console.log(`Unicorn Pro API is running on http://localhost:${PORT}`);
  });
}

// Export the Express API for Vercel Serverless Functions
module.exports = app;
