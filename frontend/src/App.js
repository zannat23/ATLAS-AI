import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:8000';

const EXAMPLES = [
  'मुझे पानी चाहिए',
  'I need a doctor',
  'أحتاج إلى مساعدة',
  'J\'ai besoin d\'aide',
  'Ninahitaji msaada',
  'मला मदत हवी आहे',
];

const LANGUAGES = [
  'Hindi', 'Arabic', 'Bengali', 'Urdu',
  'French', 'German', 'Spanish', 'Russian',
  'Turkish', 'Swahili', 'Tamil', 'Telugu',
  'Marathi', 'Gujarati', 'Punjabi', 'English'
];

const MODULES = [
  {
    icon: '🎤',
    name: 'Voice Bridge',
    desc: 'Real-time multilingual translation',
    active: true
  },
  {
    icon: '🏥',
    name: 'Medical Triage',
    desc: 'Wound classification & first aid',
    active: false
  },
  {
    icon: '🗺️',
    name: 'Resource Locator',
    desc: 'Find nearby help & shelter',
    active: false
  },
];

export default function App() {
  const [page, setPage]           = useState('voice');
  const [text, setText]           = useState('');
  const [targetLang, setTargetLang] = useState('Hindi');
  const [response, setResponse]   = useState(null);
  const [loading, setLoading]     = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResponse(null);
    try {
      const res = await axios.post(
        `${API_URL}/api/voice/full-pipeline`,
        { text, src_lang: 'hi', target_language: targetLang }
      );
      setResponse(res.data);
    } catch (err) {
      setResponse({ error: 'Could not connect to ATLAS API. Make sure the backend is running.' });
    }
    setLoading(false);
  };

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-logo">🌍 ATLAS AI</div>
        <div className="navbar-links">
          <button
            className={`nav-btn ${page === 'voice' ? 'active' : ''}`}
            onClick={() => setPage('voice')}
          >🎤 Voice</button>
          <button
            className={`nav-btn ${page === 'medical' ? 'active' : ''}`}
            onClick={() => setPage('medical')}
          >🏥 Medical</button>
          <button
            className={`nav-btn ${page === 'resources' ? 'active' : ''}`}
            onClick={() => setPage('resources')}
          >🗺️ Resources</button>
          <button
            className={`nav-btn ${page === 'about' ? 'active' : ''}`}
            onClick={() => setPage('about')}
          >ℹ️ About</button>
        </div>
      </nav>

      {/* Hero */}
      <div className="hero">
        <h1>ATLAS AI</h1>
        <p>Offline Multilingual Crisis Assistance — helping displaced people
           communicate, get medical help, and find resources</p>
        <div className="hero-tags">
          <span className="hero-tag">🌍 60+ Languages</span>
          <span className="hero-tag">📴 Works Offline</span>
          <span className="hero-tag">⚡ GPU Accelerated</span>
          <span className="hero-tag">🔒 Privacy First</span>
        </div>
      </div>

      <div className="main-container">

        {/* Module Cards */}
        <div className="modules-grid">
          {MODULES.map(m => (
            <div
              key={m.name}
              className={`module-card ${page === m.name.toLowerCase().replace(' ', '-') ||
                (page === 'voice' && m.name === 'Voice Bridge') ? 'active' : ''}`}
              onClick={() => {
                if (m.active) setPage('voice');
                else setPage(m.name.toLowerCase().replace(' ', '-'));
              }}
            >
              <div className="module-icon">{m.icon}</div>
              <div className="module-name">{m.name}</div>
              <div className="module-desc">{m.desc}</div>
              {!m.active && (
                <div className="coming-soon">Coming Soon</div>
              )}
            </div>
          ))}
        </div>

        {/* Voice Page */}
        {page === 'voice' && (
          <div className="card">
            <h2>🎤 Voice Bridge</h2>

            <textarea
              className="input-area"
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="Type in any language... (मुझे पानी चाहिए)"
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />

            {/* Example phrases */}
            <div className="examples">
              {EXAMPLES.map(ex => (
                <button
                  key={ex}
                  className="example-btn"
                  onClick={() => setText(ex)}
                >{ex}</button>
              ))}
            </div>

            <div className="controls">
              <label style={{ color: 'rgba(255,255,255,0.6)' }}>
                Respond in:
              </label>
              <select
                className="lang-select"
                value={targetLang}
                onChange={e => setTargetLang(e.target.value)}
              >
                {LANGUAGES.map(l => (
                  <option key={l} value={l}>{l}</option>
                ))}
              </select>
              <button
                className="send-btn"
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? (
                  <div className="loading-dots">
                    <div className="dot"/><div className="dot"/><div className="dot"/>
                  </div>
                ) : '🚀 Send to ATLAS'}
              </button>
            </div>

            {/* Response */}
            {response && !response.error && (
              <div className="response-card">
                <div className="response-title">✅ ATLAS Response</div>
                <div className="response-row">
                  <div className="response-label">You said</div>
                  <div className="response-text">{response.original_text}</div>
                </div>
                <div className="response-row">
                  <div className="response-label">In English</div>
                  <div className="response-text">{response.english_text}</div>
                </div>
                <div className="response-row">
                  <div className="response-label">
                    Response in {response.target_language}
                  </div>
                  <div className="response-text highlight">
                    {response.response_translated}
                  </div>
                </div>
              </div>
            )}

            {response?.error && (
              <div className="error-card">❌ {response.error}</div>
            )}
          </div>
        )}

        {/* Medical Page */}
        {page === 'medical' && (
          <div className="card" style={{ textAlign: 'center', padding: '60px 30px' }}>
            <div style={{ fontSize: '4rem', marginBottom: '20px' }}>🏥</div>
            <h2>Medical Triage Module</h2>
            <p style={{ color: 'rgba(255,255,255,0.5)', marginTop: '15px' }}>
              Wound classification and first aid instructions coming in Day 7.
              This module will classify wounds from photos and provide
              WHO-approved first aid in 60+ languages.
            </p>
            <div className="coming-soon" style={{ marginTop: '20px', fontSize: '0.9rem' }}>
              🔄 In Development
            </div>
          </div>
        )}

        {/* Resources Page */}
        {page === 'resources' && (
          <div className="card" style={{ textAlign: 'center', padding: '60px 30px' }}>
            <div style={{ fontSize: '4rem', marginBottom: '20px' }}>🗺️</div>
            <h2>Crisis Resource Locator</h2>
            <p style={{ color: 'rgba(255,255,255,0.5)', marginTop: '15px' }}>
              Offline maps and resource locator coming soon.
              Find nearest hospitals, water points, shelters and NGOs.
            </p>
            <div className="coming-soon" style={{ marginTop: '20px', fontSize: '0.9rem' }}>
              🔄 In Development
            </div>
          </div>
        )}

        {/* About Page */}
        {page === 'about' && (
          <div className="card">
            <h2>ℹ️ About ATLAS AI</h2>
            <div style={{ color: 'rgba(255,255,255,0.7)', lineHeight: '1.8' }}>
              <p style={{ marginBottom: '15px' }}>
                <strong style={{ color: 'white' }}>ATLAS</strong> is an offline
                multilingual AI system designed to help displaced people, refugees,
                and crisis victims break three critical barriers:
              </p>
              {[
                ['🎤', 'Language barrier', 'Real-time translation in 60+ languages'],
                ['🏥', 'Medical barrier', 'Wound triage and first aid guidance'],
                ['🗺️', 'Geographic barrier', 'Offline resource and shelter locator'],
              ].map(([icon, title, desc]) => (
                <div key={title} style={{
                  display: 'flex', gap: '15px',
                  marginBottom: '15px',
                  padding: '15px',
                  background: 'rgba(255,255,255,0.03)',
                  borderRadius: '10px'
                }}>
                  <span style={{ fontSize: '1.5rem' }}>{icon}</span>
                  <div>
                    <div style={{ color: 'white', fontWeight: 600 }}>{title}</div>
                    <div style={{ fontSize: '0.9rem' }}>{desc}</div>
                  </div>
                </div>
              ))}
              <div style={{
                marginTop: '20px',
                padding: '15px',
                background: 'rgba(102,126,234,0.1)',
                borderRadius: '10px',
                border: '1px solid rgba(102,126,234,0.2)'
              }}>
                <strong style={{ color: '#a78bfa' }}>Tech Stack: </strong>
                PyTorch · Whisper · NLLB-200 · FastAPI · React.js · RTX 3050 GPU
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="footer">
        ATLAS AI — B.Tech Final Year Project | AI & ML Department | 2025-26
      </div>
    </div>
  );
}