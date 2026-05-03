import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, NavLink, Link, useLocation } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import ChatPage from './pages/ChatPage'
import DashboardPage from './pages/DashboardPage'
import MatchPage from './pages/MatchPage'
import AdminPage from './pages/AdminPage'
import CommunityPage from './pages/CommunityPage'
import './App.css'

function AppContent() {
  const [navOpen, setNavOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Reveal Animation Logic
  useEffect(() => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        }
      });
    }, observerOptions);

    const observeElements = () => {
      const revealElements = document.querySelectorAll('.reveal');
      revealElements.forEach(el => observer.observe(el));
    };

    observeElements();

    // Use MutationObserver to handle dynamically added content (e.g., tab changes)
    const mutationObserver = new MutationObserver(() => {
      observeElements();
    });

    mutationObserver.observe(document.body, { childList: true, subtree: true });

    return () => {
      observer.disconnect();
      mutationObserver.disconnect();
    };
  }, [location.pathname]);

  return (
    <div className="app-layout">
      {/* Header */}
      <header className={`app-header ${scrolled ? 'scrolled' : ''}`}>
        <div className="header-inner">
          {/* Left: Logo + Icon */}
          <Link to="/" className="logo-group">
            <div className="logo-icon">
              <svg width="24" height="24" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="2" width="28" height="28" rx="6" fill="currentColor"/>
                <path d="M8 10L16 22L24 10" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                <circle cx="16" cy="10" r="2.5" fill="white"/>
              </svg>
            </div>
            <span className="logo-name">VenueIQ</span>
          </Link>

          {/* Center: Navigation */}
          <nav className={`header-nav ${navOpen ? 'nav-open' : ''}`}>
            <NavLink to="/" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`} end>
              Home
            </NavLink>
            <NavLink to="/dashboard" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              Live Status
            </NavLink>
            <NavLink to="/match" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              Match
            </NavLink>
            <NavLink to="/community" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              Community
            </NavLink>
            <NavLink to="/chat" className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`}>
              Concierge
            </NavLink>
          </nav>

          {/* Right: Ask AI Button */}
          <div className="header-right">
            <Link to="/chat" className="header-cta-btn">
              Ask AI
            </Link>
          </div>

          {/* Mobile Toggle */}
          <button className="menu-toggle" onClick={() => setNavOpen(!navOpen)} aria-label="Menu">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/match" element={<MatchPage />} />
          <Route path="/community" element={<CommunityPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  )
}

export default App
