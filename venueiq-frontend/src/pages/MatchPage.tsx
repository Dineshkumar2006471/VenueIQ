import React from 'react';
import './MatchPage.css';

const MatchPage: React.FC = () => {
  return (
    <div className="match-container">
      {/* ─── Match Header / Scoreboard ─────────────────────────── */}
      <section className="scoreboard-section reveal active">
        <div className="scoreboard-bg">
          <img src="/cricket_match_live_scores_1777152561896.png" alt="Live Match Scores Editorial" />
          <div className="sb-overlay"></div>
        </div>
        
        <div className="scoreboard-main">
          <div className="team-left">
            <span className="team-location">HOME</span>
            <h2 className="team-name">GUJARAT TITANS</h2>
            <div className="score-wrap">
              <span className="runs">214</span>
              <span className="wickets">/ 4</span>
            </div>
            <span className="overs">20.0 OVERS</span>
          </div>

          <div className="vs-divider">
            <div className="vs-line"></div>
            <span className="vs-text">VS</span>
            <div className="vs-line"></div>
          </div>

          <div className="team-right">
            <span className="team-location">AWAY</span>
            <h2 className="team-name">MUMBAI INDIANS</h2>
            <div className="score-wrap">
              <span className="target-label">TARGET</span>
              <span className="target-runs">215</span>
            </div>
            <span className="status">LIVE • SECOND INNINGS</span>
          </div>
        </div>
      </section>

      {/* ─── Match Hero ─────────────────────────────────────────── */}
      <section className="match-hero reveal active">
        <div className="pitch-visual-wrapper">
          <img 
            src="/modi_stadium_pitch_match_day_1777154945593.png" 
            alt="Pitch View" 
            className="pitch-img"
          />
          <div className="hud-overlay">
            <div className="hud-box top-left">
              <span className="hud-label">PITCH CONDITION</span>
              <span className="hud-value">DRY / TURNING</span>
            </div>
            <div className="hud-box bottom-right">
              <span className="hud-label">PREDICTIVE WIN %</span>
              <span className="hud-value">GT 64%</span>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Intelligence Hub ──────────────────────────────────── */}
      <section className="intel-grid">
        <div className="intel-panel analysis reveal active">
          <div className="panel-bg">
            <img src="/stadium_crowd_monitoring_neural_1777155660879.png" alt="Analysis Background" />
            <div className="p-overlay"></div>
          </div>
          <div className="panel-content">
            <span className="section-label">OVER ANALYSIS</span>
            <div className="over-timeline technical-grid">
              {[
                { over: 18, balls: ['1', '4', '6', 'W', '0', '1'], label: 'Rashid Khan' },
                { over: 17, balls: ['1', '1', '2', '4', '1', '1'], label: 'Mohit Sharma' },
                { over: 16, balls: ['6', '6', '1', 'W', '1', '4'], label: 'Rashid Khan' }
              ].map((o, i) => (
                <div key={i} className="over-row technical-row">
                  <div className="over-meta">
                    <span className="over-num">OVER {o.over}</span>
                    <span className="over-bowler">{o.label}</span>
                  </div>
                  <div className="ball-list">
                    {o.balls.map((b, j) => (
                      <span key={j} className={`ball ${b === '6' ? 'six' : b === 'W' ? 'wicket' : ''}`}>{b}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="intel-panel lineups reveal active" style={{ transitionDelay: '200ms' }}>
          <div className="panel-bg">
            <img src="/cinematic_food_court_intelligence_1777155646352.png" alt="Lineup Background" />
            <div className="p-overlay"></div>
          </div>
          <div className="panel-content">
          <span className="section-label">BATTING LEDGER</span>
          <div className="lineup-split technical-blueprint">
            <div className="batting-side">
              <span className="side-title">ON STRIKE</span>
              <div className="player-card active">
                <span className="p-name">SHUBMAN GILL</span>
                <span className="p-stats">89* (45) // 4x7, 6x5</span>
              </div>
              <div className="player-card">
                <span className="p-name">SAI SUDHARSAN</span>
                <span className="p-stats">42 (32) // 4x4, 6x1</span>
              </div>
            </div>
            <div className="bowling-side">
              <span className="side-title">ATTACK</span>
              <div className="player-card active">
                <span className="p-name">JASPRIT BUMRAH</span>
                <span className="p-stats">3.4 - 0 - 24 - 1</span>
              </div>
            </div>
          </div>
        </div>
        </div>
      </section>

      {/* ─── Match Events ──────────────────────────────────────── */}
      <section className="event-ticker reveal active">
        <div className="ticker-wrap">
          <div className="ticker-item">GILL REACHES 500 RUNS THIS SEASON</div>
          <div className="ticker-item">STADIUM ATTENDANCE: 112,482</div>
          <div className="ticker-item">NEURAL ENGINE PREDICTS SURGE AT GATE 4</div>
          <div className="ticker-item">WEATHER: 32°C CLEAR SKY</div>
        </div>
      </section>
      
      <div style={{ height: '100px' }}></div>
    </div>
  );
};

export default MatchPage;
