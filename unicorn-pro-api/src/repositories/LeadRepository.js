const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

class LeadRepository {
  /**
   * Save an unsold lead.
   * @param {Object} leadData
   * @returns {Promise<Object>}
   */
  static async saveUnsoldLead(leadData) {
    return prisma.lead.create({
      data: { ...leadData, status: 'Unsold' }
    });
  }

  /**
   * Save a sold lead and execute billing transactions atomically to prevent race conditions.
   * @param {Object} leadData 
   * @param {import('../types').Campaign[]} winners 
   * @param {string} status 'Exclusive' or 'Shared'
   * @returns {Promise<Object>} The created lead
   */
  static async saveSoldLeadWithTransactions(leadData, winners, status) {
    return prisma.$transaction(async (tx) => {
      // 1. Create the lead
      const newLead = await tx.lead.create({
        data: { ...leadData, status }
      });

      // 2. Process each winner
      for (const campaign of winners) {
        // a. Deduct balance. We use decrement to ensure atomicity at DB level
        await tx.buyer.update({
          where: { id: campaign.buyerId },
          data: { balance: { decrement: campaign.maxBid } }
        });

        // b. Double check if balance dropped below 0 (if DB doesn't have constraint)
        const updatedBuyer = await tx.buyer.findUnique({
          where: { id: campaign.buyerId }
        });

        if (updatedBuyer.balance < 0) {
          throw new Error(`Insufficient funds for buyer ${campaign.buyerId} during transaction`);
        }

        // c. Create Purchase record
        await tx.leadPurchase.create({
          data: {
            leadId: newLead.id,
            buyerId: campaign.buyerId,
            price: campaign.maxBid
          }
        });
      }

      return newLead;
    });
  }
}

module.exports = LeadRepository;
