const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  // Create 3 demo buyers
  const buyer1 = await prisma.buyer.create({
    data: { name: 'HVAC Masters LLC', balance: 500.00 },
  });
  const buyer2 = await prisma.buyer.create({
    data: { name: 'Cool Breeze Air', balance: 300.00 },
  });
  const buyer3 = await prisma.buyer.create({
    data: { name: 'Rapid Heating', balance: 150.00 },
  });

  // Create active campaigns
  await prisma.campaign.create({
    data: {
      buyerId: buyer1.id,
      name: 'Miami Emergency HVAC',
      vertical: 'HVAC',
      zipCodes: '33101,33145',
      leadType: 'Exclusive',
      maxBid: 150.00,
      dailyLimit: 5,
    },
  });

  await prisma.campaign.create({
    data: {
      buyerId: buyer1.id,
      name: 'Florida Wide Maintenance',
      vertical: 'HVAC',
      zipCodes: 'all',
      leadType: 'Shared',
      maxBid: 50.00,
      dailyLimit: 20,
    },
  });

  await prisma.campaign.create({
    data: {
      buyerId: buyer2.id,
      name: 'Cool Breeze - Shared Leads',
      vertical: 'HVAC',
      zipCodes: '33101,33109',
      leadType: 'Shared',
      maxBid: 45.00,
      dailyLimit: 10,
    },
  });

  await prisma.campaign.create({
    data: {
      buyerId: buyer3.id,
      name: 'Rapid Heating - High Intent',
      vertical: 'HVAC',
      zipCodes: '33101,33145',
      leadType: 'Exclusive',
      maxBid: 80.00,
      dailyLimit: 3,
    },
  });

  console.log('Seed completed!');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
