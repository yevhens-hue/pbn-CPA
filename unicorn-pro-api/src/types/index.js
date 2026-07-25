/**
 * @typedef {Object} Lead
 * @property {string} serviceType - The service requested (e.g., 'HVAC')
 * @property {string} zipCode - The ZIP code of the property
 * @property {string} urgency - 'Emergency' or 'This Week'
 * @property {string} [status] - The sale status (Exclusive, Shared, Unsold)
 */

/**
 * @typedef {Object} Buyer
 * @property {number} id - Buyer ID
 * @property {string} name - Company name
 * @property {number} balance - Current wallet balance
 */

/**
 * @typedef {Object} Campaign
 * @property {number} id - Campaign ID
 * @property {number} buyerId - ID of the buyer owning this campaign
 * @property {string} vertical - 'HVAC', 'Solar', etc.
 * @property {string} zipCodes - Comma separated zip codes or 'all'
 * @property {string} leadType - 'Exclusive' or 'Shared'
 * @property {number} maxBid - Maximum amount willing to pay per lead
 * @property {boolean} isActive - Is the campaign active
 * @property {Buyer} [buyer] - The buyer object (joined)
 */

/**
 * @typedef {Object} AuctionResult
 * @property {string} status - 'Exclusive', 'Shared', or 'Unsold'
 * @property {Campaign[]} winners - List of winning campaigns
 * @property {number} maxExclusiveBid - Highest exclusive bid evaluated
 * @property {number} topSharedSum - Sum of top shared bids evaluated
 */

module.exports = {};
