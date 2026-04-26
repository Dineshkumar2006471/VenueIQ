import React, { useState, useEffect, useRef } from 'react';
import './ChatPage.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

interface Message {
  role: 'assistant' | 'user';
  text: string;
  time: string;
}

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'assistant', 
      text: 'Neural Link Established. Accessing Narendra Modi Stadium core telemetry. How can I assist your operation?',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const assistantTextRef = useRef('');

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  const handleSend = async (messageOverride?: string) => {
    const messageText = (messageOverride ?? input).trim();
    if (!messageText || isProcessing) return;

    const userMessage: Message = {
      role: 'user',
      text: messageText,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageText,
          session_id: 'browser_user_1'
        })
      });

      if (!response.body) throw new Error("No response body");
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      assistantTextRef.current = "";
      
      // Add empty assistant message to start streaming into
      const initialAssistantMessage: Message = {
        role: 'assistant',
        text: "",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, initialAssistantMessage]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        assistantTextRef.current += chunk;
        
        // Update the last message with the cumulative text
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].text = assistantTextRef.current;
          return newMessages;
        });
      }

    } catch (error) {
      console.error("Chat Error:", error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: "Error: Communication with Intelligence Mesh interrupted.",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const quickQueries = [
    "What is the live score?",
    "Shortest queue for food?",
    "Quickest gate to exit?",
    "Match prediction?",
    "Report a spill in Sector B"
  ];

  return (
    <div className="chat-container">
      {/* ─── Page Background ───────────────────────────────────── */}
      <div className="neural-bg">
        <img src="/abstract_neural_mesh_dark_1777155688379.png" alt="Neural Mesh" />
        <div className="bg-overlay"></div>
      </div>

      <div className="terminal-grid">
        {/* ─── Sidebar: Protocols ──────────────────────────────── */}
        <aside className="terminal-sidebar protocols reveal active">
          <div className="sidebar-bg">
            <img src="/stadium_crowd_monitoring_neural_1777155660879.png" alt="Monitoring" />
            <div className="sidebar-overlay"></div>
          </div>
          <div className="sidebar-content">
            <div className="sidebar-header">
              <span className="section-label">SYSTEM PROTOCOLS</span>
            </div>
            <nav className="protocol-nav technical-blueprint">
              {[
                { id: 'P-01', name: 'CROWD FLOW', status: 'ACTIVE' },
                { id: 'P-04', name: 'GATE REROUTE', status: 'READY' },
                { id: 'P-07', name: 'SENTRY MESH', status: 'STABLE' },
                { id: 'P-12', name: 'EVAC PROTOCOL', status: 'STANDBY' }
              ].map((p) => (
                <div key={p.id} className={`protocol-item ${p.status === 'ACTIVE' ? 'active' : ''}`}>
                  <span className="p-id">{p.id}</span>
                  <span className="p-name">{p.name}</span>
                  <span className="p-status">{p.status}</span>
                </div>
              ))}
            </nav>
            <div className="connection-status">
              <div className="pulse-dot"></div>
              <span>STADIUM MESH LINKED</span>
            </div>
          </div>
        </aside>

        {/* ─── Main: Intelligence Feed ─────────────────────────── */}
        <main className="terminal-main reveal active">
          <div className="terminal-header">
            <div className="header-top">
              <h1 className="terminal-title">NEURAL CONCIERGE</h1>
              <div className="live-tag">LIVE FEED</div>
            </div>
            <span className="terminal-subtitle">Direct Access to VenueIQ Core Intelligence Mesh</span>
          </div>

          <div className="chat-window">
            {messages.map((msg, i) => (
              <div key={i} className={`message-row ${msg.role}`}>
                <div className="message-meta">
                  <span className="msg-sender">{msg.role === 'assistant' ? 'VENUE_IQ' : 'OPERATOR'}</span>
                  <span className="msg-time">{msg.time}</span>
                </div>
                <div className="message-content">
                  <p>{msg.text}</p>
                </div>
              </div>
            ))}
            {isProcessing && (
              <div className="message-row assistant processing">
                <div className="message-meta">
                  <span className="msg-sender">VENUE_IQ</span>
                  <span className="msg-time">SYS_PROG</span>
                </div>
                <div className="message-content">
                  <div className="loading-dots">
                    <span>.</span><span>.</span><span>.</span>
                  </div>
                  <p className="processing-text">NEURAL PROCESSING...</p>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="quick-queries">
            {quickQueries.map((q, i) => (
              <button 
                key={i} 
                className="query-chip"
                onClick={() => handleSend(q)}
                disabled={isProcessing}
              >
                {q}
              </button>
            ))}
          </div>

          <div className="chat-input-area">
            <div className="input-wrapper">
              <div className="input-prompt">IQ_SYS:/&gt;</div>
              <input 
                type="text" 
                placeholder="QUERY NEURAL MESH..." 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                disabled={isProcessing}
              />
              <button className="send-btn" onClick={() => handleSend()} disabled={isProcessing}>
                {isProcessing ? 'BUSY' : 'EXECUTE'}
              </button>
            </div>
          </div>
        </main>

        {/* ─── Right: Spatial Context ──────────────────────────── */}
        <aside className="terminal-sidebar context reveal active">
          <div className="sidebar-bg">
            <img src="/stadium_security_command_center_1777155705835.png" alt="Command Center" />
            <div className="sidebar-overlay"></div>
          </div>
          <div className="sidebar-content">
            <div className="sidebar-header">
              <span className="section-label">SPATIAL CONTEXT</span>
            </div>
            <div className="context-card technical-blueprint">
              <h4 className="card-title">SARDAR PATEL ZONE</h4>
              <div className="context-metrics">
                <div className="c-metric">
                  <span className="c-label">OCCUPANCY</span>
                  <span className="c-val">94.2%</span>
                </div>
                <div className="c-metric">
                  <span className="c-label">FLOW RATE</span>
                  <span className="c-val">120P/M</span>
                </div>
              </div>
              <div className="mini-map">
                <div className="map-grid"></div>
                <div className="map-radar"></div>
                <div className="map-dot"></div>
              </div>
            </div>

            <div className="history-list technical-blueprint">
              <span className="history-label">RECENT ACTIONS</span>
              <div className="history-item">
                <span className="h-time">14:15</span>
                <span className="h-text">SYSTEM INITIATED GATE REROUTE AT ZONE 4</span>
              </div>
              <div className="history-item">
                <span className="h-time">14:10</span>
                <span className="h-text">HVAC OPTIMIZED - SECTOR D</span>
              </div>
              <div className="history-item">
                <span className="h-time">14:02</span>
                <span className="h-text">ANOMALY DETECTED IN NORTH STAND - RESOLVED</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default ChatPage;
