import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [text, setText] = useState('');
  const [targetLang, setTargetLang] = useState('Hindi');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const languages = [
    'Hindi', 'Arabic', 'Bengali', 'Urdu',
    'French', 'German', 'Spanish', 'Russian',
    'Turkish', 'Swahili', 'Tamil', 'Telugu',
    'Marathi', 'Gujarati', 'Punjabi', 'English'
  ];

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/api/voice/full-pipeline`, {
        text: text,
        src_lang: 'hi',
        target_language: targetLang
      });
      setResponse(res.data);
    } catch (err) {
      console.error(err);
      setResponse({ error: 'Failed to connect to ATLAS API' });
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f0c29, #302b63, #24243e)',
      color: 'white',
      fontFamily: 'Arial, sans-serif'
    }}>

      {/* Header */}
      <div style={{ textAlign: 'center', padding: '40px 20px 20px' }}>
        <h1 style={{ fontSize: '3rem', margin: 0 }}>🌍 ATLAS AI</h1>
        <p style={{ fontSize: '1.2rem', opacity: 0.8, marginTop: '10px' }}>
          Offline Multilingual Crisis Assistance System
        </p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '15px' }}>
          {['Voice Bridge', 'Medical Triage', 'Resource Locator'].map(tag => (
            <span key={tag} style={{
              background: 'rgba(255,255,255,0.1)',
              padding: '5px 15px',
              borderRadius: '20px',
              fontSize: '0.85rem'
            }}>{tag}</span>
          ))}
        </div>
      </div>

      {/* Main Card */}
      <div style={{
        maxWidth: '800px',
        margin: '30px auto',
        padding: '30px',
        background: 'rgba(255,255,255,0.05)',
        borderRadius: '20px',
        border: '1px solid rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)'
      }}>

        <h2 style={{ marginBottom: '20px' }}>🎤 Voice Bridge</h2>

        {/* Text Input */}
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Type in any language... (मुझे पानी चाहिए)"
          style={{
            width: '100%',
            height: '100px',
            background: 'rgba(255,255,255,0.08)',
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: '10px',
            padding: '15px',
            color: 'white',
            fontSize: '1rem',
            resize: 'none',
            boxSizing: 'border-box'
          }}
        />

        {/* Language Selector */}
        <div style={{ marginTop: '15px', display: 'flex', gap: '15px', alignItems: 'center' }}>
          <label>Respond in:</label>
          <select
            value={targetLang}
            onChange={e => setTargetLang(e.target.value)}
            style={{
              background: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '8px',
              padding: '8px 15px',
              color: 'white',
              fontSize: '1rem'
            }}
          >
            {languages.map(lang => (
              <option key={lang} value={lang}
                style={{ background: '#302b63' }}>
                {lang}
              </option>
            ))}
          </select>
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            marginTop: '20px',
            width: '100%',
            padding: '15px',
            background: loading
              ? 'rgba(255,255,255,0.1)'
              : 'linear-gradient(135deg, #667eea, #764ba2)',
            border: 'none',
            borderRadius: '10px',
            color: 'white',
            fontSize: '1.1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontWeight: 'bold'
          }}
        >
          {loading ? '⏳ Processing...' : '🚀 Send to ATLAS'}
        </button>

        {/* Response */}
        {response && !response.error && (
          <div style={{
            marginTop: '25px',
            padding: '20px',
            background: 'rgba(255,255,255,0.05)',
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.1)'
          }}>
            <h3 style={{ color: '#a78bfa', marginBottom: '15px' }}>
              ✅ ATLAS Response
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <div>
                <span style={{ opacity: 0.6, fontSize: '0.85rem' }}>You said:</span>
                <p style={{ margin: '3px 0', fontSize: '1.1rem' }}>
                  {response.original_text}
                </p>
              </div>
              <div>
                <span style={{ opacity: 0.6, fontSize: '0.85rem' }}>In English:</span>
                <p style={{ margin: '3px 0', fontSize: '1.1rem' }}>
                  {response.english_text}
                </p>
              </div>
              <div>
                <span style={{ opacity: 0.6, fontSize: '0.85rem' }}>
                  Response in {response.target_language}:
                </span>
                <p style={{
                  margin: '3px 0',
                  fontSize: '1.1rem',
                  color: '#a78bfa',
                  fontWeight: 'bold'
                }}>
                  {response.response_translated}
                </p>
              </div>
            </div>
          </div>
        )}

        {response?.error && (
          <div style={{
            marginTop: '20px',
            padding: '15px',
            background: 'rgba(255,0,0,0.1)',
            borderRadius: '10px',
            color: '#ff6b6b'
          }}>
            ❌ {response.error}
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{ textAlign: 'center', padding: '20px', opacity: 0.5 }}>
        ATLAS AI — B.Tech Final Year Project | AI & ML Department
      </div>
    </div>
  );
}

export default App;