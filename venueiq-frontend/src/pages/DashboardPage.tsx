import React, { useState } from 'react';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const stats = [
    { label: 'CURRENT ATTENDANCE', value: '112,482', change: '+4.2%', detail: 'NEAR CAPACITY' },
    { label: 'NEURAL SENTIMENT', value: '89.4', change: 'OPTIMAL', detail: 'FAN ENGAGEMENT' },
    { label: 'QUEUE VELOCITY', value: '2.4M/S', change: 'SWIFT', detail: 'ENTRY POINTS' },
    { label: 'PROTOCOL STATUS', value: 'ACTIVE', change: 'STABLE', detail: 'NEURAL MESH' }
  ];

  return (
    <div className="dashboard-container">
      {/* ─── Hero Section ───────────────────────────────────────── */}
      <section className="dashboard-hero reveal active">
        <div className="hero-bg-wrapper">
          <img 
            src="/editorial_stadium_telemetry_bw_1777156156927.png" 
            alt="Stadium Telemetry Editorial" 
            className="hero-bg-img"
          />
          <div className="hero-bg-overlay"></div>
        </div>
        <div className="hero-grid">
          <div className="hero-content">
            <span className="section-label">GLOBAL TELEMETRY</span>
            <h1 className="hero-title">NARENDRA MODI<br/>STADIUM HUB</h1>
            <p className="hero-subtitle">
              LIVE NEURAL TELEMETRY FROM THE WORLD'S LARGEST CRICKET ARENA. 
              REAL-TIME CROWD ORCHESTRATION AND SPATIAL INTELLIGENCE.
            </p>
            <div className="venue-meta">
              <div className="meta-item">
                <span className="meta-label">LOCATION</span>
                <span className="meta-value">AHMEDABAD, INDIA</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">MATCH</span>
                <span className="meta-value">GT VS MI • IPL FINAL</span>
              </div>
            </div>

            {/* Enhanced Content to fill space below */}
            <div className="hero-enhanced-content">
              <div className="content-block">
                <span className="block-label">NEURAL NODE DENSITY</span>
                <div className="density-grid">
                  {[...Array(12)].map((_, i) => (
                    <div key={i} className={`node ${i < 8 ? 'active' : ''}`}></div>
                  ))}
                </div>
              </div>
              <div className="content-block">
                <span className="block-label">CROWD DYNAMICS</span>
                <p className="block-text">High-density flow detected at North Stand Gate 3. Redirection protocols active.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Quick Stats ────────────────────────────────────────── */}
      <section className="stats-strip">
        {stats.map((stat, i) => (
          <div key={i} className="stat-card reveal active" style={{ transitionDelay: `${i * 100}ms` }}>
            <span className="stat-label">{stat.label}</span>
            <div className="stat-main">
              <span className="stat-value">{stat.value}</span>
              <span className="stat-change">{stat.change}</span>
            </div>
            <span className="stat-detail">{stat.detail}</span>
          </div>
        ))}
      </section>

      {/* ─── Neural Surge Drilldown ─────────────────────────────── */}
      <section className="neural-drilldown reveal active">
        <div className="section-bg-container">
           <img src="/stadium_crowd_monitoring_neural_1777155660879.png" alt="Crowd Neural" className="section-bg-img" />
           <div className="section-bg-overlay"></div>
        </div>
        
        <div className="drilldown-header">
          <div className="tabs">
            {['overview', 'facilities', 'concourse', 'security'].map(tab => (
              <button 
                key={tab} 
                className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>

        <div className="drilldown-content">
          <div className="visual-panel">
            <div className="heatmap-placeholder">
              <div className="pulse-point p1"></div>
              <div className="pulse-point p2"></div>
              <div className="pulse-point p3"></div>
              <div className="grid-overlay"></div>
              <img src="/venue_analytics_dashboard_1777152579382.png" alt="Analytics" className="panel-bg-img" />
            </div>
            <div className="panel-label">SPATIAL HEATMAP [REAL-TIME]</div>
          </div>

          <div className="data-panel">
            <h3 className="panel-title">ZONE INTELLIGENCE MESH</h3>
            <div className="zone-list technical-blueprint">
              {[
                { name: 'ADANI PAVILION', load: '92%', status: 'CRITICAL', gate: 'GATE 1' },
                { name: 'RELIANCE END', load: '78%', status: 'OPTIMAL', gate: 'GATE 4' },
                { name: 'SARDAR PATEL STAND', load: '65%', status: 'STABLE', gate: 'GATE 2' },
                { name: 'NORTH TERRACE', load: '88%', status: 'HIGH', gate: 'GATE 3' }
              ].map((zone, i) => (
                <div key={i} className="zone-item">
                  <div className="zone-info">
                    <span className="zone-name">{zone.name}</span>
                    <span className="zone-gate">{zone.gate}</span>
                  </div>
                  <div className="zone-metrics">
                    <span className="zone-load">{zone.load}</span>
                    <span className={`zone-status ${zone.status.toLowerCase()}`}>{zone.status}</span>
                  </div>
                  <div className="load-bar"><div className="fill" style={{ width: zone.load }}></div></div>
                </div>
              ))}
            </div>
            <button className="protocol-btn">DEPLOY SURGE PROTOCOL</button>
          </div>
        </div>
      </section>

      {/* ─── Security Section ───────────────────────────────────── */}
      <section className="security-section reveal active">
        <div className="security-bg">
          <img src="/stadium_security_command_center_1777155705835.png" alt="Security Command" />
          <div className="security-overlay"></div>
        </div>
        <div className="security-content">
          <span className="section-label">SECURITY MESH</span>
          <h2 className="security-title">COMMAND CENTER ACCESS</h2>
          <p className="security-desc">MONITORING 1,200+ NEURAL-LINKED CAMERAS AND ENTRY POINTS ACROSS ALL ZONES.</p>
          <div className="security-status-grid">
             <div className="s-status"><span>CAMERAS</span><strong>ACTIVE</strong></div>
             <div className="s-status"><span>MESH</span><strong>STABLE</strong></div>
             <div className="s-status"><span>GATES</span><strong>ENFORCED</strong></div>
          </div>
        </div>
      </section>

      <div style={{ height: '100px' }}></div>
    </div>
  );
};

export default DashboardPage;
