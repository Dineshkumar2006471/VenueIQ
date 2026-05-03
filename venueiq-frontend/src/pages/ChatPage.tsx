import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
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
      text: 'Neural Link Established. Accessing stadium core telemetry. How can I assist your operation today?',
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
    "Match prediction?"
  ];

  return (
    <div className="chat-page">
      <section className="chat-hero">
        <div className="chat-hero-bg"></div>
        <div className="chat-hero-overlay"></div>
        <div className="chat-hero-content container-narrow">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          >
            <div className="eyebrow">
              <span className="live-pulse"></span>
              NEURAL LINK ACTIVE
            </div>
            <h1 className="hero-title">Concierge <span className="accent-text">Intelligence</span></h1>
            <p className="hero-story">
              Direct access to real-time stadium telemetry. Ask about crowd flow, food queues, gate density, or incident reports.
            </p>
          </motion.div>
        </div>
      </section>

      <div className="chat-body container-narrow">
        
        {/* Sidebar Context */}
        <motion.aside 
          className="chat-sidebar"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="sidebar-info-block">
            <h3 className="eyebrow">Active Mesh Protocols</h3>
            <div className="protocol-list">
              {[
                { id: 'P-01', name: 'CROWD FLOW', status: 'ACTIVE' },
                { id: 'P-04', name: 'GATE REROUTE', status: 'READY' },
                { id: 'P-07', name: 'SENTRY MESH', status: 'STABLE' },
              ].map((p) => (
                <div key={p.id} className="protocol-card card">
                  <div className="protocol-info">
                    <span className="protocol-id">{p.id}</span>
                    <span className="protocol-name">{p.name}</span>
                  </div>
                  <span className={`protocol-status ${p.status === 'ACTIVE' ? 'status-active' : ''}`}>
                    {p.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="sidebar-info-block">
            <h3 className="eyebrow">Spatial Context</h3>
            <div className="context-card card">
              <h4 className="context-zone">Sardar Patel Zone</h4>
              <div className="context-metrics">
                <div className="metric">
                  <span className="metric-label">Occupancy</span>
                  <span className="metric-val">94.2%</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Flow Rate</span>
                  <span className="metric-val">120<span className="text-muted">/m</span></span>
                </div>
              </div>
            </div>
          </div>
        </motion.aside>

        {/* Chat Feed */}
        <motion.main 
          className="chat-main card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <div className="chat-feed">
            {messages.map((msg, i) => (
              <motion.div 
                key={i} 
                className={`message-row ${msg.role}`}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                {msg.role === 'assistant' && (
                  <div className="avatar assistant-avatar">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                  </div>
                )}
                <div className="message-content">
                  <span className="message-sender">{msg.role === 'assistant' ? 'VenueIQ AI' : 'You'}</span>
                  <div className={`bubble ${msg.role}`}>
                    <p>{msg.text}</p>
                  </div>
                  <span className="message-time">{msg.time}</span>
                </div>
              </motion.div>
            ))}
            
            {isProcessing && (
              <motion.div 
                className="message-row assistant"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <div className="avatar assistant-avatar">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                </div>
                <div className="message-content">
                  <span className="message-sender">VenueIQ AI</span>
                  <div className="bubble assistant processing-bubble">
                    <span className="dot"></span><span className="dot"></span><span className="dot"></span>
                  </div>
                </div>
              </motion.div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="chat-input-area">
            <div className="quick-queries-list">
              {quickQueries.map((q, i) => (
                <button 
                  key={i} 
                  className="suggestion-chip" 
                  onClick={() => handleSend(q)} 
                  disabled={isProcessing}
                >
                  {q}
                </button>
              ))}
            </div>
            
            <div className="input-container">
              <input 
                type="text" 
                placeholder="Message VenueIQ Concierge..." 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                disabled={isProcessing}
              />
              <button 
                className="btn-primary input-submit-btn" 
                onClick={() => handleSend()} 
                disabled={isProcessing || !input.trim()}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </button>
            </div>
            
            <p className="disclaimer-text">
              VenueIQ AI provides real-time telemetry but can make mistakes. Always verify critical evacuation routes.
            </p>
          </div>
        </motion.main>
      </div>
    </div>
  );
};

export default ChatPage;
