import React, { useState } from 'react';
import axios from 'axios';
import { PulseIcon, UploadIcon } from '../icons';
import { API_URL, MEDICAL_LANGUAGES } from '../data';
import medicalImg from '../assets/medical.jpg';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';

export default function Medical() {
  const [medImage, setMedImage] = useState(null);
  const [medFile, setMedFile] = useState(null);
  const [medResult, setMedResult] = useState(null);
  const [medLoading, setMedLoading] = useState(false);
  const [availableItems, setAvailableItems] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('English');

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
      if (availableItems.trim()) {
        formData.append('available_items', availableItems.trim());
      }
      formData.append('target_language', targetLanguage);
      const res = await axios.post(`${API_URL}/api/medical/classify`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setMedResult(res.data);
    } catch (err) {
      setMedResult({ error: 'Could not connect to the backend API.' });
    }
    setMedLoading(false);
  };

  const getSeverityColor = (severity) => {
    const colors = { 1: '#3F7D5C', 2: '#6B9C4D', 3: '#B7862A', 4: '#C97B3D', 5: '#B8483C' };
    return colors[severity] || '#2B5F63';
  };

  const getSeverityLabel = (severity) => {
    const labels = { 1: 'Minimal', 2: 'Minor', 3: 'Moderate', 4: 'Serious', 5: 'Critical' };
    return labels[severity] || '';
  };

  return (
    <PageTransition>
    <PageHeader
      icon={<PulseIcon />}
      title="Medical Triage"
      subtitle="Upload a wound photo — the system classifies it and gives first aid instructions."
      image={medicalImg}
    />
    <div className="main-container">
      <div className="page-layout">
      <div className="card">
        <div className="card-dark-header">
          <PulseIcon />
          <div className="card-dark-header-title">Upload wound photo</div>
        </div>
        <div className="card-content">
        <h3 className="section-heading">A photo is all it takes</h3>
        <p className="section-sub">Get an instant severity score and first aid guidance.</p>
        <div className="field-label">Wound photo</div>
        <div
          className={`dropzone ${medImage ? 'has-image' : ''}`}
          onClick={() => document.getElementById('wound-upload').click()}
        >
          {medImage
            ? <img src={medImage} alt="wound" />
            : <>
                <div className="dropzone-icon"><UploadIcon /></div>
                <p className="dropzone-text">Click to upload wound photo</p>
                <p className="dropzone-sub">JPG, PNG supported</p>
              </>
          }
        </div>
        <input id="wound-upload" type="file" accept="image/*" style={{ display: 'none' }} onChange={handleImageUpload} />

        <div className="field-label" style={{ marginTop: '15px' }}>What do you have on hand? (optional)</div>
        <input
          className="input-area"
          style={{ minHeight: 'unset', padding: '10px' }}
          value={availableItems}
          onChange={e => setAvailableItems(e.target.value)}
          placeholder="e.g. bandage, ice, clean cloth, antiseptic..."
        />
        <p className="dropzone-sub" style={{ marginTop: '4px' }}>Comma-separated — instructions will suggest substitutes for items you don't have.</p>

        <div className="field-label" style={{ marginTop: '15px' }}>Hear instructions in</div>
        <select className="lang-select" value={targetLanguage} onChange={e => setTargetLanguage(e.target.value)}>
          {MEDICAL_LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
        </select>

        {medImage && (
          <button className="send-btn" style={{ marginTop: '15px', marginLeft: 0 }} onClick={handleMedicalClassify} disabled={medLoading}>
            {medLoading
              ? <div className="loading-dots"><div className="dot" /><div className="dot" /><div className="dot" /></div>
              : 'Classify Wound'}
          </button>
        )}

        {medResult && !medResult.error && (
          <div className="response-card">
            <div className="response-title">Medical analysis</div>

            <div className="response-row">
              <div className="response-label">Severity level</div>
              <div className="severity-gauge">
                <div className="severity-ring" style={{ '--severity-color': getSeverityColor(medResult.severity) }}>
                  <svg viewBox="0 0 90 90">
                    <circle cx="45" cy="45" r="38" fill="none" stroke="var(--border)" strokeWidth="8" />
                    <circle
                      cx="45" cy="45" r="38" fill="none"
                      stroke={getSeverityColor(medResult.severity)}
                      strokeWidth="8"
                      strokeLinecap="round"
                      strokeDasharray={`${(medResult.severity / 5) * 239} 239`}
                    />
                  </svg>
                  <div className="severity-ring-num">{medResult.severity}/5</div>
                </div>
                <div>
                  <div className="severity-label-big" style={{ '--severity-color': getSeverityColor(medResult.severity) }}>
                    {getSeverityLabel(medResult.severity)}
                  </div>
                  <div className="severity-sub">Based on wound classification confidence</div>
                </div>
              </div>
            </div>

            <div className="response-row">
              <div className="response-label">Wound type</div>
              <div className="response-text" style={{ textTransform: 'capitalize' }}>
                {medResult.wound_type.replace('_', ' ')}
                <span style={{ marginLeft: '10px', fontSize: '0.85rem', color: 'var(--text-faint)' }}>
                  ({(medResult.confidence * 100).toFixed(1)}% confidence)
                </span>
              </div>
            </div>

            {medResult.warning && (
              <div className="response-row">
                <div className="error-card" style={{ marginTop: 0 }}>{medResult.warning}</div>
              </div>
            )}

            {Array.isArray(medResult.first_aid) && medResult.first_aid.length > 0 && (
              <div className="response-row">
                <div className="response-label">
                  First aid instructions
                  {medResult.target_language && medResult.target_language !== 'English' && medResult.translated_first_aid
                    ? ` (${medResult.target_language})`
                    : ''}
                </div>
                <ol style={{ paddingLeft: '20px', margin: '6px 0' }}>
                  {medResult.first_aid.map((step, i) => (
                    <li key={i} style={{ marginBottom: '10px', lineHeight: '1.5' }}>
                      {step.instruction}
                      {step.item_note && (
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-faint)', marginTop: '2px' }}>
                          💡 {step.item_note}
                        </div>
                      )}
                    </li>
                  ))}
                </ol>
              </div>
            )}

            {medResult.audio_url && (
              <div className="response-row">
                <div className="response-label">Listen in {medResult.target_language}</div>
                <audio
                  controls
                  autoPlay
                  src={`${API_URL}${medResult.audio_url}`}
                  style={{ width: '100%', marginTop: '6px' }}
                >
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}

            {medResult.severity >= 4 && (
              <div className="urgent-banner">Urgent — seek medical help immediately</div>
            )}
          </div>
        )}
        {medResult?.error && <div className="error-card">{medResult.error}</div>}
        </div>
      </div>

      <div className="sidebar-card">
        <div className="sidebar-card-header">
          <PulseIcon />
          <div className="sidebar-title">Tips for a good scan</div>
        </div>
        <div className="sidebar-card-body">
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">1</div>
          <div className="sidebar-tip-text"><strong>Use good lighting.</strong> Natural daylight gives the clearest classification.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">2</div>
          <div className="sidebar-tip-text"><strong>Get close</strong> — fill the frame with the wound, avoid excess background.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">3</div>
          <div className="sidebar-tip-text">Classifies across <strong>6 wound categories</strong> using EfficientNet-B0.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">4</div>
          <div className="sidebar-tip-text">Instructions can be <strong>read or heard aloud</strong> in your chosen language — helpful if reading isn't easy right now.</div>
        </div>
        </div>
      </div>
      </div>
    </div>
    </PageTransition>
  );
}