import { useState, useEffect } from 'react'
import axios from 'axios'
import { QRCodeSVG } from 'qrcode.react'
import './AdminPage.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080'

interface Incident {
  id: string; type: string; location: string; description: string
  status: string; priority: string; reported_at: string
}

export default function AdminPage() {
  const [incidents, setIncidents] = useState<Incident[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'incidents'|'qr'|'heatmap'>('incidents')
  const [filterStatus, setFilterStatus] = useState('all')

  const fetchIncidents = async () => {
    try {
      const res = await axios.get(`${API_URL}/admin/incidents`)
      setIncidents(res.data.incidents || [])
    } catch (error) {
      console.warn('Using fallback incident data', error)
      setIncidents([
        { id:'1', type:'cleanliness', location:'Toilet Block A', description:'Water on floor', status:'in_progress', priority:'medium', reported_at: new Date().toISOString() },
        { id:'2', type:'safety', location:'Stand C Row 22', description:'Broken handrail', status:'open', priority:'high', reported_at: new Date().toISOString() },
        { id:'3', type:'maintenance', location:'Food Court A', description:'Display not working', status:'resolved', priority:'low', reported_at: new Date().toISOString() },
      ])
    } finally { setLoading(false) }
  }

  useEffect(() => { 
    const initialFetch = window.setTimeout(fetchIncidents, 0)
    const i = setInterval(fetchIncidents, 20000); 
    return () => {
      window.clearTimeout(initialFetch)
      clearInterval(i)
    }
  }, [])

  const updateStatus = async (id: string, s: string) => {
    try { await axios.patch(`${API_URL}/admin/incidents/${id}`, { status: s }) } catch (error) { console.warn('Incident status update failed', error) }
    setIncidents(prev => prev.map(inc => inc.id === id ? { ...inc, status: s } : inc))
  }

  const getIcon = (t: string) => ({ cleanliness:'🧹', safety:'⚠️', maintenance:'🔧', noise:'🔊' }[t] || '📋')
  const priCls = (p: string) => `priority-${p}`

  const filtered = filterStatus === 'all' ? incidents : incidents.filter(i => i.status === filterStatus)
  const counts = { 
    open: incidents.filter(i=>i.status==='open').length, 
    prog: incidents.filter(i=>i.status==='in_progress').length, 
    res: incidents.filter(i=>i.status==='resolved').length 
  }

  return (
    <div className="admin-page">
      <header className="admin-header">
        <h1 className="admin-title">Operations Console</h1>
        <p className="admin-subtitle">VenueIQ Command Center — Real-time Intelligence</p>
      </header>

      <nav className="admin-tabs">
        {(['incidents','heatmap','qr'] as const).map(t => (
          <button 
            key={t} 
            className={`admin-tab ${activeTab===t?'active':''}`} 
            onClick={()=>setActiveTab(t)}
          >
            {t === 'incidents' ? `Tasks (${incidents.length})` : t === 'heatmap' ? 'Live Heatmap' : 'Access Node'}
          </button>
        ))}
      </nav>

      {activeTab === 'incidents' && (
        <section className="incidents-section">
          <div className="incident-stats">
            <div className="incident-stat">
              <span className="stat-num">{counts.open}</span>
              <span className="stat-desc">Pending Response</span>
            </div>
            <div className="incident-stat">
              <span className="stat-num">{counts.prog}</span>
              <span className="stat-desc">In Active Resolution</span>
            </div>
            <div className="incident-stat">
              <span className="stat-num">{counts.res}</span>
              <span className="stat-desc">Closed Tickets</span>
            </div>
            <div className="incident-stat">
              <span className="stat-num">{incidents.length}</span>
              <span className="stat-desc">Total Volume (24H)</span>
            </div>
          </div>

          <div className="incident-filters">
            {['all','open','in_progress','resolved'].map(s => (
              <button 
                key={s} 
                className={`filter-btn ${filterStatus===s?'active':''}`} 
                onClick={()=>setFilterStatus(s)}
              >
                {s==='all'?'All Logs':s==='in_progress'?'In Progress':s}
              </button>
            ))}
          </div>

          {loading ? (
            <div className="dashboard-loading"><div className="loading-spinner"></div></div>
          ) : (
            <div className="incidents-list">
              {filtered.map((inc) => (
                <article key={inc.id} className={`incident-card`}>
                  <div className="incident-card-left">
                    <div className="incident-icon">{getIcon(inc.type)}</div>
                    <div className="incident-details">
                      <h3 className="incident-desc">{inc.description}</h3>
                      <div className="incident-meta">
                        <span className="incident-location">SECTOR: {inc.location}</span>
                        <span className={`incident-priority ${priCls(inc.priority)}`}>[{inc.priority}]</span>
                        <span className="incident-type">{inc.type}</span>
                      </div>
                    </div>
                  </div>
                  <div className="incident-card-right">
                    <span className={`incident-status`}>
                      {inc.status.replace('_', ' ')}
                    </span>
                    <div className="incident-actions">
                      {inc.status==='open' && <button className="action-btn" onClick={()=>updateStatus(inc.id,'in_progress')}>Authorize Start</button>}
                      {inc.status==='in_progress' && <button className="action-btn" onClick={()=>updateStatus(inc.id,'resolved')}>Mark Resolved</button>}
                      {inc.status==='resolved' && <button className="action-btn" onClick={()=>updateStatus(inc.id,'open')}>Reopen Entry</button>}
                    </div>
                  </div>
                </article>
              ))}
              {filtered.length === 0 && (
                <div className="empty-state">
                  <span>CLEAN</span>
                  <p>No active incidents found for this filter.</p>
                </div>
              )}
            </div>
          )}
        </section>
      )}

      {activeTab === 'heatmap' && (
        <section className="heatmap-tab">
          <div className="heatmap-header">
            <h2 className="admin-title">Spatial Intelligence</h2>
            <p className="section-desc">Real-time crowd density across all venue sectors. predictive flow modeling active.</p>
          </div>
          
          <div className="venue-map-container">
            <div className="venue-map-wrapper">
              <div className="stadium-oval">
                {/* Gate Markers */}
                <div className="gate-marker gate-n uppercase">Exit Gate 1</div>
                <div className="gate-marker gate-e uppercase">Exit Gate 2</div>
                <div className="gate-marker gate-s uppercase">Exit Gate 3</div>
                <div className="gate-marker gate-w uppercase">Exit Gate 4</div>

                {/* Stands with individual sections */}
                <div className="stand-group north-group">
                  <div className="stadium-stand stand-n1"><div className="stand-heat heat-warm"></div><span className="stand-label">N1</span></div>
                  <div className="stadium-stand stand-n2"><div className="stand-heat heat-hot"></div><span className="stand-label">N2</span></div>
                  <div className="stadium-stand stand-n3"><div className="stand-heat heat-warm"></div><span className="stand-label">N3</span></div>
                </div>

                <div className="stand-group east-group">
                  <div className="stadium-stand stand-e1"><div className="stand-heat heat-cool"></div><span className="stand-label">E1</span></div>
                  <div className="stadium-stand stand-e2"><div className="stand-heat heat-cool"></div><span className="stand-label">E2</span></div>
                </div>

                <div className="stand-group south-group">
                  <div className="stadium-stand stand-s1"><div className="stand-heat heat-cool"></div><span className="stand-label">S1</span></div>
                  <div className="stadium-stand stand-s2"><div className="stand-heat heat-warm"></div><span className="stand-label">S2</span></div>
                  <div className="stadium-stand stand-s3"><div className="stand-heat heat-cool"></div><span className="stand-label">S3</span></div>
                </div>

                <div className="stand-group west-group">
                  <div className="stadium-stand stand-w1"><div className="stand-heat heat-hot"></div><span className="stand-label">W1</span></div>
                  <div className="stadium-stand stand-w2"><div className="stand-heat heat-warm"></div><span className="stand-label">W2</span></div>
                </div>

                <div className="stadium-center">
                  <div className="pitch-inner">
                    <span className="pitch-label">FIELD</span>
                  </div>
                </div>
              </div>
            </div>

            <aside className="heatmap-legend">
              <div className="legend-section">
                <h3 className="legend-title uppercase">Density Index</h3>
                <div className="legend-items">
                  <div className="legend-item"><span className="legend-color heat-hot"></span><span>High (90%+)</span></div>
                  <div className="legend-item"><span className="legend-color heat-warm"></span><span>Moderate (60%)</span></div>
                  <div className="legend-item"><span className="legend-color heat-cool"></span><span>Optimal (30%)</span></div>
                </div>
              </div>

              <div className="legend-section">
                <h3 className="legend-title uppercase">Live Alerts</h3>
                <div className="alert-pills">
                  <div className="alert-pill-mini">GATE 4 SURGE</div>
                  <div className="alert-pill-mini">WEST SECTOR FULL</div>
                </div>
              </div>
            </aside>
          </div>
        </section>
      )}

      {activeTab === 'qr' && (
        <section className="qr-tab">
          <div className="qr-card">
            <h2 className="qr-title">V-IQ Access</h2>
            <p className="qr-subtitle">Public AI Concierge Interface Protocol</p>
            <div className="qr-code-wrapper">
              <QRCodeSVG 
                value="http://localhost:5173" 
                size={220} 
                bgColor="transparent" 
                fgColor="#000000" 
                level="H" 
              />
            </div>
            <p className="qr-url">NODE: LOCALHOST:5173</p>
            <div className="qr-features">
              {['CONCIERGE','NAV_SYSTEM','LIVE_FEED','V_LOG'].map(f => (
                <div key={f} className="qr-feature"><span>{f}</span></div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  )
}
