import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Home, LayoutDashboard, Zap } from 'lucide-react';
import B2CFunnel from './pages/B2CFunnel';
import B2BPortal from './pages/B2BPortal';
import './index.css';

function Navigation() {
  const location = useLocation();
  
  return (
    <header className="app-header">
      <div className="logo">
        <Zap size={28} color="var(--primary)" fill="var(--primary)" />
        Unicorn Pro MVP
      </div>
      <nav className="nav-links">
        <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
          B2C Funnel (Домовласник)
        </Link>
        <Link to="/portal" className={location.pathname === '/portal' ? 'active' : ''}>
          B2B Portal (Контрактор)
        </Link>
      </nav>
    </header>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="container">
        <Navigation />
        <main>
          <Routes>
            <Route path="/" element={<B2CFunnel />} />
            <Route path="/portal" element={<B2BPortal />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
