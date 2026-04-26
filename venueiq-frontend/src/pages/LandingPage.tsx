import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

const LandingPage: React.FC = () => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Intersection Observer for scroll-based reveals
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
    );

    const elements = document.querySelectorAll('.reveal-on-scroll');
    elements.forEach((el) => observer.observe(el));

    return () => {
      observer.disconnect();
    };
  }, []);

  // Stats
  const stats = [
    { value: '50K+', label: 'Fans Guided' },
    { value: '<2min', label: 'Avg Wait Time' },
    { value: '4', label: 'AI Agents Live' },
    { value: '98%', label: 'Satisfaction' },
  ];

  const showcaseCards = [
      {
      num: '01',
      title: 'THE PROBLEM',
      description: '50,000 fans pour into the stadium. Zero real-time guidance. Gates bottleneck. Food courts overflow. Every minute feels like a queue that never ends.',
      image: '/images/crowd-energy.png',
      accent: 'We saw the chaos. We built the answer.',
    },
    {
      num: '02',
      title: 'FOOD INTELLIGENCE',
      description: 'Queries live Firestore data for queue lengths, menu availability, and occupancy across every food court. Recommends the fastest option before you even ask.',
      image: '/images/food-court.png',
      accent: 'Skip the line. Not the meal.',
    },
    {
      num: '03',
      title: 'NAVIGATION AGENT',
      description: 'Step-by-step directions to any zone, facility, or seat. Cross-references crowd density before routing — so you always take the clear path.',
      image: '/images/navigation-corridor.png',
      accent: 'Every corridor, mapped in real time.',
    },
    {
      num: '04',
      title: 'CROWD INTELLIGENCE',
      description: 'Monitors gate density, entry wait times, and exit flow. Alerts you to surges before they happen and routes you to the least crowded gate.',
      image: '/images/gate-entrance.png',
      accent: 'See the crowd. Beat the crowd.',
    },
  ];

  return (
    <div className="landing-page">

      {/* ═══════════════════════════════════════════════════════
          HERO SECTION — White bg, text → image → stats
          ═══════════════════════════════════════════════════════ */}
      <section className="hero">
        <div className="hero-inner">
          {/* Live Badge */}
          <div className="hero-badge">
            <span className="hero-badge-dot"></span>
            <span>VenueIQ Agent — Live</span>
          </div>

          {/* Headline */}
          <h1 className="hero-headline">THE STADIUM THINKS FOR YOU</h1>

          {/* Subtext */}
          <p className="hero-subtext">AI-powered venue intelligence that eliminates queues, predicts crowd surges, and guides 50,000 fans — in real time.</p>

          {/* CTA Buttons */}
          <div className="hero-actions">
            <Link to="/chat" className="hero-btn-primary">
              Initialize Agent
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </Link>
            <Link to="/dashboard" className="hero-btn-secondary">
              View Live Status
            </Link>
          </div>

          {/* Hero Image */}
          <div className="hero-image-block">
            <img
              src="/images/hero-stadium.png"
              alt="VenueIQ — Smart Stadium Experience"
              className="hero-image"
            />
          </div>

          {/* Stats */}
          <div className="hero-stats">
            {stats.map((stat, idx) => (
              <div className="hero-stat" key={idx}>
                <span className="hero-stat-value">{stat.value}</span>
                <span className="hero-stat-label">{stat.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>


      {/* ═══════════════════════════════════════════════════════
          MANIFESTO — Scrolling news ticker
          ═══════════════════════════════════════════════════════ */}
      <section className="manifesto-ticker">
        <div className="ticker-row">
          <div className="ticker-track ticker-track-1">
            <span className="ticker-text">A STADIUM ISN'T JUST A PLACE — IT'S FIFTY THOUSAND STORIES HAPPENING AT ONCE.</span>
            <span className="ticker-text">A STADIUM ISN'T JUST A PLACE — IT'S FIFTY THOUSAND STORIES HAPPENING AT ONCE.</span>
            <span className="ticker-text">A STADIUM ISN'T JUST A PLACE — IT'S FIFTY THOUSAND STORIES HAPPENING AT ONCE.</span>
          </div>
        </div>
        <div className="ticker-row">
          <div className="ticker-track ticker-track-2">
            <span className="ticker-text">VENUEIQ IS THE INTELLIGENCE LAYER THAT MAKES EVERY ONE OF THEM SEAMLESS.</span>
            <span className="ticker-text">VENUEIQ IS THE INTELLIGENCE LAYER THAT MAKES EVERY ONE OF THEM SEAMLESS.</span>
            <span className="ticker-text">VENUEIQ IS THE INTELLIGENCE LAYER THAT MAKES EVERY ONE OF THEM SEAMLESS.</span>
          </div>
        </div>
      </section>


      {/* ═══════════════════════════════════════════════════════
          HORIZONTAL SHOWCASE — Image-first storytelling cards
          ═══════════════════════════════════════════════════════ */}
      <section className="showcase">
        <div className="showcase-header reveal-on-scroll">
          <span className="showcase-label">The Intelligence</span>
          <h2 className="showcase-title">FOUR AGENTS. ONE EXPERIENCE.</h2>
          <p className="showcase-subtitle">Drag to explore how VenueIQ orchestrates the perfect match day.</p>
        </div>

        <div className="showcase-scroll-wrapper" ref={scrollRef}>
          <div className="showcase-track">
            {showcaseCards.map((card, idx) => (
              <article className="showcase-card" key={idx}>
                <div className="showcase-card-image">
                  <img src={card.image} alt={card.title} loading="lazy" />
                  <div className="showcase-card-num">{card.num}</div>
                </div>
                <div className="showcase-card-body">
                  <h3 className="showcase-card-title">{card.title}</h3>
                  <p className="showcase-card-desc">{card.description}</p>
                  <span className="showcase-card-accent">{card.accent}</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>


      {/* ═══════════════════════════════════════════════════════
          FEATURES GRID
          ═══════════════════════════════════════════════════════ */}
      <section className="features">
        <div className="features-inner">
          <div className="features-header reveal-on-scroll">
            <span className="features-label">Capabilities</span>
            <h2 className="features-title">BUILT FOR SCALE. DESIGNED FOR DELIGHT.</h2>
          </div>

          <div className="features-grid">
            <div className="feature-card reveal-on-scroll">
              <div className="feature-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
              </div>
              <h3>MULTI-AGENT ARCHITECTURE</h3>
              <p>Four specialized AI agents — food, navigation, crowd, and match — coordinated by a root orchestrator using Google ADK.</p>
            </div>
            <div className="feature-card reveal-on-scroll">
              <div className="feature-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              </div>
              <h3>REAL-TIME FIRESTORE</h3>
              <p>Live venue data streams every 5 seconds. Queue lengths, occupancy rates, and gate density — always current, always accurate.</p>
            </div>
            <div className="feature-card reveal-on-scroll">
              <div className="feature-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              </div>
              <h3>CONVERSATIONAL INTERFACE</h3>
              <p>Natural language queries. Ask "Where's the fastest food?" and the AI returns ranked options with live wait times.</p>
            </div>
            <div className="feature-card reveal-on-scroll">
              <div className="feature-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              </div>
              <h3>CROWD PREDICTION</h3>
              <p>Anticipates bottlenecks before they form. Route suggestions update as crowd patterns shift throughout the match.</p>
            </div>
            <div className="feature-card reveal-on-scroll">
              <div className="feature-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              </div>
              <h3>LIVE MATCH SCORES</h3>
              <p>CricketData.org API integration with Firestore fallback. Ball-by-ball updates rendered on a dedicated match view.</p>
            </div>
            <div className="feature-card reveal-on-scroll">
              <div className="feature-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              </div>
              <h3>INCIDENT REPORTS</h3>
              <p>Safety-first design. The AI can flag incidents, and the admin dashboard tracks resolution in real time.</p>
            </div>
          </div>
        </div>
      </section>


      {/* ═══════════════════════════════════════════════════════
          CTA FOOTER
          ═══════════════════════════════════════════════════════ */}
      <section className="cta-section">
        <div className="cta-bg-container">
          <img src="/images/crowd-energy.png" alt="" className="cta-bg-img" />
          <div className="cta-bg-overlay"></div>
        </div>
        <div className="cta-content reveal-on-scroll">
          <h2 className="cta-headline">Ready to skip<br/>the queue?</h2>
          <p className="cta-subtext">Your AI concierge is standing by. Ask anything about the venue.</p>
          <Link to="/chat" className="cta-btn">
            Connect to Agent
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </Link>
        </div>
      </section>

    </div>
  );
};

export default LandingPage;
