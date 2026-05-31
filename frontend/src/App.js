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
  { icon:'🎤', name:'Voice Bridge',     desc:'Real-time multilingual translation', active:true },
  { icon:'🏥', name:'Medical Triage',   desc:'Wound classification & first aid',   active:true },
  { icon:'🗺️', name:'Resource Locator', desc:'Find nearby help & shelter',         active:true },
];

export default function App() {
  const [page,       setPage]       = useState('voice');
  const [text,       setText]       = useState('');
  const [targetLang, setTargetLang] = useState('Hindi');
  const [response,   setResponse]   = useState(null);
  const [loading,    setLoading]    = useState(false);
  const [medImage,   setMedImage]   = useState(null);
  const [medFile,    setMedFile]    = useState(null);
  const [medResult,  setMedResult]  = useState(null);
  const [medLoading, setMedLoading] = useState(false);
  const [resQuery,   setResQuery]   = useState('');
  const [resType,    setResType]    = useState(null);
  const [resResults, setResResults] = useState([]);
  const [resLoading, setResLoading] = useState(false);

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
      setResponse({ error: 'Could not connect to ATLAS API.' });
    }
    setLoading(false);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setMedFile(file);
    setMedResult(null);
    const reader = new FileReader();
    reader.onload = (ev) => setMedImage(ev.target.result);
    reader.readAsDataURL(file);
  };

  const handleMedicalClassify = async () => {
    if (!medFile) return;
    setMedLoading(true);
    setMedResult(null);
    try {
      const formData = new FormData();
      formData.append('file', medFile);
      const res = await axios.post(
        `${API_URL}/api/medical/classify`,
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setMedResult(res.data);
    } catch (err) {
      setMedResult({ error: 'Could not connect to ATLAS API.' });
    }
    setMedLoading(false);
  };

  const getSeverityColor = (severity) => {
    const colors = { 1:'#4ade80', 2:'#a3e635', 3:'#facc15', 4:'#fb923c', 5:'#f87171' };
    return colors[severity] || 'white';
  };

  const getSeverityLabel = (severity) => {
    const labels = { 1:'Minimal', 2:'Minor', 3:'Moderate', 4:'Serious', 5:'Critical' };
    return labels[severity] || '';
  };

  const handleResourceSearch = async (type = null) => {
    setResLoading(true);
    try {
      const res = await axios.post(
        `${API_URL}/api/resources/search`,
        {
          query:         resQuery || null,
          resource_type: type || resType || null,
          lat:           18.5204,
          lon:           73.8567,
          limit:         8
        }
      );
      setResResults(res.data.results);
    } catch (err) {
      console.error(err);
    }
    setResLoading(false);
  };

  const getResourceIcon = (type) => {
    const icons = { hospital:'🏥', water:'💧', shelter:'🏠', food:'🍱', ngo:'🤝' };
    return icons[type] || '📍';
  };

  return (
    <div>
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-logo">🌍 ATLAS AI</div>
        <div className="navbar-links">
          <button className={`nav-btn ${page==='voice'    ?'active':''}`} onClick={()=>setPage('voice')}>🎤 Voice</button>
          <button className={`nav-btn ${page==='medical'  ?'active':''}`} onClick={()=>setPage('medical')}>🏥 Medical</button>
          <button className={`nav-btn ${page==='resources'?'active':''}`} onClick={()=>setPage('resources')}>🗺️ Resources</button>
          <button className={`nav-btn ${page==='about'    ?'active':''}`} onClick={()=>setPage('about')}>ℹ️ About</button>
        </div>
      </nav>

      {/* Hero */}
      <div className="hero">
        <h1>ATLAS AI</h1>
        <p>Offline Multilingual Crisis Assistance — helping displaced people communicate, get medical help, and find resources</p>
        <div className="hero-tags">
          <span className="hero-tag">🌍 60+ Languages</span>
          <span className="hero-tag">📴 Works Offline</span>
          <span className="hero-tag">⚡ GPU Accelerated</span>
          <span className="hero-tag">🔒 Privacy First</span>
        </div>
      </div>

      <div className="main-container">

        {/* Module Cards — only once */}
        <div className="modules-grid">
          {MODULES.map(m => (
            <div
              key={m.name}
              className={`module-card ${
                (page==='voice'     && m.name==='Voice Bridge')     ||
                (page==='medical'   && m.name==='Medical Triage')   ||
                (page==='resources' && m.name==='Resource Locator') ? 'active' : ''
              }`}
              onClick={() => {
                if (m.name==='Voice Bridge')     setPage('voice');
                if (m.name==='Medical Triage')   setPage('medical');
                if (m.name==='Resource Locator') setPage('resources');
              }}
            >
              <div className="module-icon">{m.icon}</div>
              <div className="module-name">{m.name}</div>
              <div className="module-desc">{m.desc}</div>
            </div>
          ))}
        </div>

        {/* VOICE PAGE */}
        {page === 'voice' && (
          <div className="card">
            <h2>🎤 Voice Bridge</h2>
            <textarea
              className="input-area"
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="Type in any language... (मुझे पानी चाहिए)"
              onKeyDown={e => { if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); handleSubmit(); }}}
            />
            <div className="examples">
              {EXAMPLES.map(ex => (
                <button key={ex} className="example-btn" onClick={()=>setText(ex)}>{ex}</button>
              ))}
            </div>
            <div className="controls">
              <label style={{color:'rgba(255,255,255,0.6)'}}>Respond in:</label>
              <select className="lang-select" value={targetLang} onChange={e=>setTargetLang(e.target.value)}>
                {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
              </select>
              <button className="send-btn" onClick={handleSubmit} disabled={loading}>
                {loading
                  ? <div className="loading-dots"><div className="dot"/><div className="dot"/><div className="dot"/></div>
                  : '🚀 Send to ATLAS'}
              </button>
            </div>
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
                  <div className="response-label">Response in {response.target_language}</div>
                  <div className="response-text highlight">{response.response_translated}</div>
                </div>
              </div>
            )}
            {response?.error && <div className="error-card">❌ {response.error}</div>}
          </div>
        )}

        {/* MEDICAL PAGE */}
        {page === 'medical' && (
          <div className="card">
            <h2>🏥 Medical Triage</h2>
            <p style={{color:'rgba(255,255,255,0.5)', marginBottom:'20px'}}>
              Upload a wound photo — ATLAS classifies it and gives first aid instructions
            </p>
            <div
              style={{
                border:'2px dashed rgba(255,255,255,0.15)',
                borderRadius:'16px', padding:'40px',
                textAlign:'center', cursor:'pointer',
                background: medImage ? 'rgba(102,126,234,0.05)' : 'transparent'
              }}
              onClick={() => document.getElementById('wound-upload').click()}
            >
              {medImage
                ? <img src={medImage} alt="wound" style={{maxHeight:'250px', maxWidth:'100%', borderRadius:'12px'}}/>
                : <>
                    <div style={{fontSize:'3rem', marginBottom:'10px'}}>📷</div>
                    <p style={{color:'rgba(255,255,255,0.5)'}}>Click to upload wound photo</p>
                    <p style={{color:'rgba(255,255,255,0.3)', fontSize:'0.85rem'}}>JPG, PNG supported</p>
                  </>
              }
            </div>
            <input id="wound-upload" type="file" accept="image/*"
              style={{display:'none'}} onChange={handleImageUpload}/>
            {medImage && (
              <button className="send-btn" style={{marginTop:'15px'}}
                onClick={handleMedicalClassify} disabled={medLoading}>
                {medLoading
                  ? <div className="loading-dots"><div className="dot"/><div className="dot"/><div className="dot"/></div>
                  : '🔍 Classify Wound'}
              </button>
            )}
            {medResult && !medResult.error && (
              <div className="response-card" style={{marginTop:'20px'}}>
                <div className="response-title">🏥 Medical Analysis</div>
                <div style={{marginBottom:'15px'}}>
                  <div className="response-label">Severity Level</div>
                  <div style={{display:'flex', gap:'8px', marginTop:'8px', alignItems:'center'}}>
                    {[1,2,3,4,5].map(n => (
                      <div key={n} style={{
                        width:'40px', height:'40px', borderRadius:'50%',
                        background: n<=medResult.severity ? getSeverityColor(medResult.severity) : 'rgba(255,255,255,0.1)',
                        display:'flex', alignItems:'center', justifyContent:'center',
                        fontWeight:'bold', fontSize:'0.9rem'
                      }}>{n}</div>
                    ))}
                    <span style={{marginLeft:'10px', color:getSeverityColor(medResult.severity), fontWeight:600}}>
                      {getSeverityLabel(medResult.severity)}
                    </span>
                  </div>
                </div>
                <div className="response-row">
                  <div className="response-label">Wound Type</div>
                  <div className="response-text" style={{textTransform:'capitalize'}}>
                    {medResult.wound_type.replace('_',' ')}
                    <span style={{marginLeft:'10px', fontSize:'0.85rem', color:'rgba(255,255,255,0.4)'}}>
                      ({(medResult.confidence*100).toFixed(1)}% confidence)
                    </span>
                  </div>
                </div>
                <div className="response-row">
                  <div className="response-label">First Aid Instructions</div>
                  <div className="response-text highlight">{medResult.first_aid}</div>
                </div>
                {medResult.severity >= 4 && (
                  <div style={{
                    marginTop:'15px', padding:'12px 16px',
                    background:'rgba(255,59,59,0.1)',
                    border:'1px solid rgba(255,59,59,0.3)',
                    borderRadius:'10px', color:'#ff6b6b', fontWeight:600
                  }}>🚨 URGENT — Seek medical help immediately!</div>
                )}
              </div>
            )}
            {medResult?.error && <div className="error-card">❌ {medResult.error}</div>}
          </div>
        )}

        {/* RESOURCES PAGE */}
        {page === 'resources' && (
          <div className="card">
            <h2>🗺️ Crisis Resource Locator</h2>
            <p style={{color:'rgba(255,255,255,0.5)', marginBottom:'20px'}}>
              Find nearest hospitals, water points, shelters and NGOs
            </p>
            <div style={{display:'flex', gap:'10px', marginBottom:'15px'}}>
              <input
                type="text"
                value={resQuery}
                onChange={e => setResQuery(e.target.value)}
                placeholder="Type: I need water / hospital / shelter..."
                style={{
                  flex:1, background:'rgba(255,255,255,0.05)',
                  border:'1px solid rgba(255,255,255,0.1)',
                  borderRadius:'10px', padding:'12px 15px',
                  color:'white', fontSize:'0.95rem'
                }}
                onKeyDown={e => e.key==='Enter' && handleResourceSearch()}
              />
              <button className="send-btn" style={{flex:'0 0 auto', padding:'12px 20px'}}
                onClick={() => handleResourceSearch()} disabled={resLoading}>
                {resLoading ? '⏳' : '🔍 Search'}
              </button>
            </div>
            <div style={{display:'flex', gap:'8px', flexWrap:'wrap', marginBottom:'20px'}}>
              {[
                {id:'hospital', label:'🏥 Hospital'},
                {id:'water',    label:'💧 Water'},
                {id:'shelter',  label:'🏠 Shelter'},
                {id:'food',     label:'🍱 Food'},
                {id:'ngo',      label:'🤝 NGO'},
              ].map(t => (
                <button key={t.id} className="example-btn"
                  style={{
                    background: resType===t.id ? 'rgba(102,126,234,0.3)' : 'rgba(255,255,255,0.05)',
                    borderColor: resType===t.id ? '#667eea' : 'rgba(255,255,255,0.1)'
                  }}
                  onClick={() => { setResType(t.id); handleResourceSearch(t.id); }}
                >{t.label}</button>
              ))}
            </div>
            {resResults.length > 0 && (
              <div>
                <div style={{fontSize:'0.85rem', color:'rgba(255,255,255,0.4)', marginBottom:'12px'}}>
                  Found {resResults.length} resources nearby
                </div>
                <div style={{display:'flex', flexDirection:'column', gap:'10px'}}>
                  {resResults.map(r => (
                    <div key={r.id} style={{
                      background:'rgba(255,255,255,0.03)',
                      border:'1px solid rgba(255,255,255,0.08)',
                      borderRadius:'12px', padding:'15px',
                      display:'flex', gap:'15px', alignItems:'flex-start'
                    }}>
                      <div style={{fontSize:'2rem'}}>{getResourceIcon(r.type)}</div>
                      <div style={{flex:1}}>
                        <div style={{fontWeight:600, fontSize:'1rem', marginBottom:'4px'}}>{r.name}</div>
                        <div style={{fontSize:'0.85rem', color:'rgba(255,255,255,0.5)', marginBottom:'4px'}}>{r.description}</div>
                        {r.address && <div style={{fontSize:'0.8rem', color:'rgba(255,255,255,0.4)'}}>📍 {r.address}</div>}
                        {r.phone   && <div style={{fontSize:'0.8rem', color:'#667eea', marginTop:'4px'}}>📞 {r.phone}</div>}
                      </div>
                      <div style={{textAlign:'right', flexShrink:0}}>
                        <div style={{
                          background:'rgba(102,126,234,0.15)',
                          border:'1px solid rgba(102,126,234,0.3)',
                          borderRadius:'20px', padding:'4px 12px',
                          fontSize:'0.85rem', color:'#a78bfa', fontWeight:600
                        }}>{r.distance_km} km</div>
                        <div style={{fontSize:'0.75rem', color:'rgba(255,255,255,0.3)', marginTop:'4px', textTransform:'capitalize'}}>{r.type}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {resResults.length === 0 && !resLoading && (
              <div style={{textAlign:'center', padding:'40px', color:'rgba(255,255,255,0.3)'}}>
                <div style={{fontSize:'3rem', marginBottom:'10px'}}>🔍</div>
                <p>Search for resources or click a filter above</p>
              </div>
            )}
          </div>
        )}

        {/* ABOUT PAGE */}
        {page === 'about' && (
          <div className="card">
            <h2>ℹ️ About ATLAS AI</h2>
            <div style={{color:'rgba(255,255,255,0.7)', lineHeight:'1.8'}}>
              <p style={{marginBottom:'15px'}}>
                <strong style={{color:'white'}}>ATLAS</strong> is an offline multilingual AI system
                designed to help displaced people, refugees, and crisis victims.
              </p>
              {[
                ['🎤','Language barrier','Real-time translation in 60+ languages'],
                ['🏥','Medical barrier','Wound triage and first aid guidance'],
                ['🗺️','Geographic barrier','Offline resource and shelter locator'],
              ].map(([icon,title,desc]) => (
                <div key={title} style={{
                  display:'flex', gap:'15px', marginBottom:'15px',
                  padding:'15px', background:'rgba(255,255,255,0.03)', borderRadius:'10px'
                }}>
                  <span style={{fontSize:'1.5rem'}}>{icon}</span>
                  <div>
                    <div style={{color:'white', fontWeight:600}}>{title}</div>
                    <div style={{fontSize:'0.9rem'}}>{desc}</div>
                  </div>
                </div>
              ))}
              <div style={{
                marginTop:'20px', padding:'15px',
                background:'rgba(102,126,234,0.1)',
                borderRadius:'10px', border:'1px solid rgba(102,126,234,0.2)'
              }}>
                <strong style={{color:'#a78bfa'}}>Tech Stack: </strong>
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