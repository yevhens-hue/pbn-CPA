import React, { useState, useEffect } from 'react';
import { Inbox, Target, CreditCard, RotateCcw, AlertTriangle, CheckCircle2 } from 'lucide-react';
import './B2BPortal.css';

export default function B2BPortal() {
  const [activeTab, setActiveTab] = useState('inbox');
  const [leads, setLeads] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [balance, setBalance] = useState(0);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001';
      const [leadsRes, campaignsRes, balanceRes] = await Promise.all([
        fetch(`${apiUrl}/api/leads/inbox`),
        fetch(`${apiUrl}/api/campaigns`),
        fetch(`${apiUrl}/api/buyers/balance`)
      ]);
      const leadsData = await leadsRes.json();
      const campaignsData = await campaignsRes.json();
      const balanceData = await balanceRes.json();

      setLeads(leadsData);
      setCampaigns(campaignsData);
      setBalance(balanceData.balance);
    } catch (err) {
      console.error("Failed to fetch portal data", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const toggleCampaign = async (id) => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001';
      await fetch(`${apiUrl}/api/campaigns/${id}/toggle`, { method: 'POST' });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="portal-layout animate-slide-up">
      {/* Sidebar */}
      <aside className="portal-sidebar glass-card">
        <div className="contractor-profile">
          <div className="avatar">HV</div>
          <div>
            <strong>HVAC Masters LLC</strong>
            <div className="balance"><CreditCard size={12}/> Balance: ${balance.toFixed(2)}</div>
          </div>
        </div>
        
        <nav className="portal-nav">
          <button className={activeTab === 'inbox' ? 'active' : ''} onClick={() => { setActiveTab('inbox'); fetchData(); }}>
            <Inbox size={18} /> Lead Inbox <span className="badge">{leads.length}</span>
          </button>
          <button className={activeTab === 'campaigns' ? 'active' : ''} onClick={() => setActiveTab('campaigns')}>
            <Target size={18} /> Campaigns
          </button>
          <button className={activeTab === 'billing' ? 'active' : ''} onClick={() => setActiveTab('billing')}>
            <CreditCard size={18} /> Wallet & Billing
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="portal-main">
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'white' }}>Loading data...</div>
        ) : (
          <>
            {activeTab === 'inbox' && (
              <div className="inbox-view">
                <header className="view-header">
                  <h2>Lead Inbox</h2>
                  <div className="status-indicator">
                    <span className="dot online"></span> Receiving Leads
                  </div>
                </header>
                
                <div className="leads-list">
                  {leads.length === 0 && <p style={{color: '#a0a0a0'}}>No leads purchased yet. Run the B2C funnel to buy leads!</p>}
                  {leads.map(lead => (
                    <div key={lead.purchaseId} className="lead-card glass-card">
                      <div className="lead-header">
                        <div className="lead-tags">
                          <span className={`tag ${lead.status === 'Exclusive' ? 'tag-primary' : 'tag-secondary'}`}>
                            {lead.status === 'Exclusive' ? '🎯 Exclusive' : '👥 Shared'}
                          </span>
                          {lead.urgency === 'Emergency' && <span className="tag tag-danger">🚨 Emergency</span>}
                        </div>
                        <div className="lead-time">{new Date(lead.time).toLocaleString()}</div>
                      </div>
                      
                      <div className="lead-body">
                        <h3>{lead.name}</h3>
                        <div className="lead-details">
                          <span><strong>Service:</strong> {lead.type}</span>
                          <span><strong>Location:</strong> ZIP {lead.zip}</span>
                          <span><strong>Cost:</strong> ${lead.price} (deducted)</span>
                        </div>
                      </div>
                      
                      <div className="lead-footer">
                        <div style={{fontSize: '14px', color: '#ccc'}}>
                          📞 {lead.phone} | ✉️ {lead.email}
                        </div>
                        <button className="btn-return">
                          <RotateCcw size={14} /> Request Return
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'campaigns' && (
              <div className="campaigns-view glass-card">
                <header className="view-header">
                  <h2>Active Campaigns</h2>
                  <button className="btn-primary">+ New Campaign</button>
                </header>
                <div className="campaign-list">
                  {campaigns.map(camp => (
                    <div key={camp.id} className="campaign-row" style={{ opacity: camp.isActive ? 1 : 0.6 }}>
                      <div className="camp-info">
                        <strong>{camp.name}</strong>
                        <span>Target: {camp.zipCodes} | {camp.leadType}</span>
                      </div>
                      <div className="camp-bid">
                        <strong>Max Bid: ${camp.maxBid}</strong>
                      </div>
                      <div className="camp-status">
                        <button 
                          className="btn-secondary" 
                          style={{ padding: '6px 12px', fontSize: '12px' }}
                          onClick={() => toggleCampaign(camp.id)}
                        >
                          {camp.isActive ? 'Pause' : 'Activate'}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'billing' && (
              <div className="billing-view glass-card">
                <h2>Wallet & Billing</h2>
                <div className="wallet-card">
                  <div className="wallet-bal">
                    <span>Current Balance</span>
                    <strong>${balance.toFixed(2)}</strong>
                  </div>
                  <button className="btn-primary">Add Funds</button>
                </div>
                <p className="hint">Auto-recharge is enabled when balance falls below $100.</p>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
