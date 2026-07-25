import React, { useState } from 'react';
import { Star, ArrowRight, ShieldCheck, Zap, Fan, Flame, Settings } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import PhoneInput from '../components/PhoneInput';
import './B2CFunnel.css';

const STEPS = ['Service', 'Location', 'Details', 'Contact'];

export default function B2CFunnel() {
  const [step, setStep] = useState(0); // 0 = hero, 1-4 = funnel, 5 = thank you
  const [loading, setLoading] = useState(false);
  const [winners, setWinners] = useState([]);
  
  const [formData, setFormData] = useState({
    serviceType: 'HVAC',
    zipCode: '33101',
    propertyType: 'Residential',
    isOwner: true,
    urgency: 'Emergency',
    name: 'John Doe',
    phone: '(555) 123-4567',
    email: 'john@example.com',
    tcpa: true
  });

  const handleNext = () => setStep(s => s + 1);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3001';
      const response = await fetch(`${apiUrl}/api/leads`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setWinners(data.winners || []);
      setStep(5);
    } catch (error) {
      console.error('Error submitting lead:', error);
      alert('Error submitting lead. Make sure API server is running.');
    } finally {
      setLoading(false);
    }
  };

  if (step === 0) {
    return (
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        className="hero-section"
      >
        <div className="social-proof">
          <div className="stars"><Star fill="#00b67a" color="#00b67a" size={20}/><Star fill="#00b67a" color="#00b67a" size={20}/><Star fill="#00b67a" color="#00b67a" size={20}/><Star fill="#00b67a" color="#00b67a" size={20}/><Star fill="#00b67a" color="#00b67a" size={20}/></div>
          <span>Trustpilot 4.9/5 (12,000+ Reviews)</span>
        </div>
        <h1 className="hero-title">Find Top-Rated HVAC Pros in Minutes</h1>
        <p className="hero-sub">Get free, no-obligation estimates from local certified contractors.</p>
        
        <div className="search-box glass-card">
          <input type="text" placeholder="What type of pro is needed? (e.g. AC Repair)" defaultValue="HVAC" disabled />
          <button className="btn-primary" onClick={() => setStep(1)}>
            Find Pros <ArrowRight size={18} />
          </button>
        </div>
        
        <div className="trust-badges delay-200">
          <span><ShieldCheck size={16} /> Vetted Pros</span>
          <span><Zap size={16} /> Fast Response</span>
        </div>
      </motion.div>
    );
  }

  if (step === 5) {
    return (
      <motion.div 
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="thank-you-section glass-card"
      >
        <div className="success-icon">✅</div>
        <h2>Request Submitted!</h2>
        
        {winners.length > 0 ? (
          <>
            <div className="urgency-badge">🔥 {winners.length} contractor(s) matched and may call now</div>
            <p>Keep your phone nearby. These top-rated pros are reviewing your details:</p>
            <div className="winners-list" style={{ marginTop: '20px', textAlign: 'left' }}>
              {winners.map((w, idx) => (
                <div key={idx} className="winner-card" style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '10px' }}>
                  <strong>{w.companyName}</strong>
                </div>
              ))}
            </div>
          </>
        ) : (
          <>
            <div className="urgency-badge" style={{ background: '#fef3c7', color: '#b45309' }}>⏳ We are finding the best pros in your area</div>
            <p>Our team is manually matching your request with local pros. We will contact you shortly.</p>
          </>
        )}
        
        <button className="btn-secondary" onClick={() => setStep(0)} style={{marginTop: '24px'}}>Start Over</button>
      </motion.div>
    );
  }

  return (
    <div className="funnel-container animate-slide-up">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${(step / 4) * 100}%` }}></div>
      </div>
      <div className="progress-labels">
        {STEPS.map((s, i) => (
          <span key={s} className={i < step ? 'done' : i + 1 === step ? 'active' : ''}>{s}</span>
        ))}
      </div>

      <div className="funnel-card glass-card">
        <AnimatePresence mode="wait">
        {step === 1 && (
          <motion.div 
            key="step1"
            initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}
            className="step-content"
          >
            <h2>What do you need help with?</h2>
            <div className="tiles-grid">
              <button className="tile-btn" onClick={() => { setFormData({...formData, serviceType: 'AC Repair'}); handleNext(); }}>
                <Fan size={32} />
                <span>AC Repair</span>
              </button>
              <button className="tile-btn" onClick={() => { setFormData({...formData, serviceType: 'Heating Install'}); handleNext(); }}>
                <Flame size={32} />
                <span>Heating Install</span>
              </button>
              <button className="tile-btn" onClick={() => { setFormData({...formData, serviceType: 'Maintenance'}); handleNext(); }}>
                <Settings size={32} />
                <span>Maintenance</span>
              </button>
            </div>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div 
            key="step2"
            initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}
            className="step-content"
          >
            <h2>Where is the property?</h2>
            <input type="text" className="input-lg" placeholder="Enter ZIP Code" value={formData.zipCode} onChange={(e) => setFormData({...formData, zipCode: e.target.value})} />
            <div className="radio-group" style={{marginTop: '20px'}}>
              <label><input type="radio" name="owner" checked={formData.isOwner} onChange={() => setFormData({...formData, isOwner: true})} /> I am the homeowner</label>
              <label><input type="radio" name="owner" checked={!formData.isOwner} onChange={() => setFormData({...formData, isOwner: false})} /> I am renting (Soft Exit Trigger)</label>
            </div>
            <button className="btn-primary mt-4" onClick={handleNext}>Continue</button>
          </motion.div>
        )}

        {step === 3 && (
          <motion.div 
            key="step3"
            initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}
            className="step-content"
          >
            <h2>How urgent is this project?</h2>
            <div className="tiles-list">
              <button className="tile-row" onClick={() => { setFormData({...formData, urgency: 'Emergency'}); handleNext(); }}>
                <span className="emoji">🚨</span>
                <div className="tile-text">
                  <strong>Emergency (Today)</strong>
                  <span>High priority exclusive routing</span>
                </div>
              </button>
              <button className="tile-row" onClick={() => { setFormData({...formData, urgency: 'This Week'}); handleNext(); }}>
                <span className="emoji">📅</span>
                <div className="tile-text">
                  <strong>This Week</strong>
                  <span>Standard shared routing</span>
                </div>
              </button>
            </div>
          </motion.div>
        )}

        {step === 4 && (
          <motion.div 
            key="step4"
            initial={{ opacity: 0, x: 50 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -50 }}
            className="step-content"
          >
            <h2>Who should we contact?</h2>
            <div className="form-group">
              <input type="text" placeholder="Full Name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} />
              <PhoneInput 
                value={formData.phone} 
                onChange={(val) => setFormData({...formData, phone: val})} 
              />
              <span className="form-hint">Twilio Lookup validation active</span>
              <input type="email" placeholder="Email Address" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} />
            </div>
            <div className="tcpa-box">
              <input type="checkbox" id="tcpa" checked={formData.tcpa} onChange={(e) => setFormData({...formData, tcpa: e.target.checked})} />
              <label htmlFor="tcpa">I agree to receive calls and texts. (TrustedForm Cert: <i>https://cert.trustedform.com/abc...</i>)</label>
            </div>
            <button className="btn-primary mt-4 w-full" onClick={handleSubmit} disabled={loading}>
              {loading ? 'Processing...' : 'Get Free Quotes'}
            </button>
          </motion.div>
        )}
        </AnimatePresence>
      </div>
    </div>
  );
}
