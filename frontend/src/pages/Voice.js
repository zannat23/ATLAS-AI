import React, { useState, useRef } from 'react';
import axios from 'axios';
import { MicIcon } from '../icons';
import { LANGUAGES, API_URL } from '../data';
import voiceImg from '../assets/voice.jpg';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';

export default function Voice() {
  const [langA, setLangA] = useState('Hindi');   // language Person A UNDERSTANDS (output target)
  const [langB, setLangB] = useState('English');  // language Person B UNDERSTANDS (output target)
  const [textA, setTextA] = useState('');
  const [textB, setTextB] = useState('');
  const [conversation, setConversation] = useState([]);
  const [recording, setRecording] = useState(null); // 'A' | 'B' | null
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // ── Voice input (Whisper auto-detects speaker's language) ──
  const startRecording = async (speaker) => {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      recorder.onstop = () => handleRecordingStop(speaker, stream);
      mediaRecorderRef.current = recorder;
      recorder.start();
      setRecording(speaker);
    } catch (err) {
      setError('Microphone access denied or unavailable.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    setRecording(null);
  };

  const handleRecordingStop = async (speaker, stream) => {
    stream.getTracks().forEach(track => track.stop());
    const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
    const targetLanguage = speaker === 'A' ? langB : langA;

    const formData = new FormData();
    formData.append('file', blob, `recording_${speaker}.webm`);
    formData.append('target_language', targetLanguage);

    setProcessing(true);
    try {
      const res = await axios.post(`${API_URL}/api/voice/converse`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      addToConversation(
        speaker,
        res.data.spoken_text,
        res.data.translated_text,
        res.data.detected_language_name,
        targetLanguage,
        res.data.audio_url
      );
    } catch (err) {
      setError('Could not process the recording. Check backend connection.');
    }
    setProcessing(false);
  };

  // ── Text input (fully automatic — no manual language selection) ──
  const handleTextSend = async (speaker) => {
    const text = speaker === 'A' ? textA : textB;
    if (!text.trim()) return;
    const targetLanguage = speaker === 'A' ? langB : langA;

    setProcessing(true);
    setError(null);
    try {
      const res = await axios.post(`${API_URL}/api/voice/converse-text`, {
        text, target_language: targetLanguage
      });
      addToConversation(
        speaker,
        res.data.spoken_text,
        res.data.translated_text,
        res.data.detected_language_name,
        targetLanguage,
        res.data.audio_url
      );
      speaker === 'A' ? setTextA('') : setTextB('');
    } catch (err) {
      setError('Could not translate. Check backend connection.');
    }
    setProcessing(false);
  };

  const addToConversation = (speaker, original, translated, spokenLangName, targetLanguage, audioUrl) => {
    const fullAudioUrl = audioUrl ? `${API_URL}${audioUrl}`: null;
    setConversation(prev => [...prev, {
      speaker,
      spokenLang: spokenLangName || '—',
      targetLang: targetLanguage,
      original,
      translated,
      audioUrl: fullAudioUrl
    }]);
    new Audio(fullAudioUrl).play();
  };

  return (
    <PageTransition>
    <PageHeader
      icon={<MicIcon />}
      title="Voice Bridge"
      subtitle="A live two-way conversation translator — speak or type in any language, the other person hears and reads it in theirs."
      image={voiceImg}
    />
    <div className="main-container">
      <div className="page-layout">
      <div className="card">
        <div className="card-dark-header">
          <MicIcon />
          <div className="card-dark-header-title">Live Conversation</div>
        </div>
        <div className="card-content">
          <h3 className="section-heading">Speak or type in any language — it's auto-detected</h3>
          <p className="section-sub">Set what each person understands below. Just speak or type naturally — the system figures out the language automatically.</p>

          {/* Person A */}
          <div className="field-label">Person A understands</div>
          <div className="controls" style={{ marginBottom: '10px' }}>
            <select className="lang-select" value={langA} onChange={e => setLangA(e.target.value)}>
              {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
            <button
              className="send-btn"
              style={{ background: recording === 'A' ? '#b23b3b' : undefined }}
              disabled={processing || (recording && recording !== 'A')}
              onClick={() => recording === 'A' ? stopRecording() : startRecording('A')}
            >
              <MicIcon /> {recording === 'A' ? 'Stop' : 'Speak'}
            </button>
          </div>
          <div className="controls" style={{ marginBottom: '20px' }}>
            <input
              className="input-area"
              style={{ minHeight: 'unset', padding: '10px' }}
              value={textA}
              onChange={e => setTextA(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') handleTextSend('A'); }}
              placeholder="Or type in any language..."
              disabled={processing}
            />
            <button className="send-btn" onClick={() => handleTextSend('A')} disabled={processing}>Send</button>
          </div>

          {/* Person B */}
          <div className="field-label">Person B understands</div>
          <div className="controls" style={{ marginBottom: '10px' }}>
            <select className="lang-select" value={langB} onChange={e => setLangB(e.target.value)}>
              {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
            <button
              className="send-btn"
              style={{ background: recording === 'B' ? '#b23b3b' : undefined }}
              disabled={processing || (recording && recording !== 'B')}
              onClick={() => recording === 'B' ? stopRecording() : startRecording('B')}
            >
              <MicIcon /> {recording === 'B' ? 'Stop' : 'Speak'}
            </button>
          </div>
          <div className="controls" style={{ marginBottom: '20px' }}>
            <input
              className="input-area"
              style={{ minHeight: 'unset', padding: '10px' }}
              value={textB}
              onChange={e => setTextB(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') handleTextSend('B'); }}
              placeholder="Or type in any language..."
              disabled={processing}
            />
            <button className="send-btn" onClick={() => handleTextSend('B')} disabled={processing}>Send</button>
          </div>

          {processing && (
            <div className="loading-dots"><div className="dot" /><div className="dot" /><div className="dot" /></div>
          )}
          {error && <div className="error-card">{error}</div>}

          <div style={{ marginTop: '24px' }}>
            {conversation.map((entry, i) => (
              <div key={i} className="response-card" style={{ marginBottom: '12px' }}>
                <div className="response-title">
                  {entry.speaker === 'A' ? 'Person A' : 'Person B'} said (detected: {entry.spokenLang})
                </div>
                <div className="response-row">
                  <div className="response-text">{entry.original}</div>
                </div>
                <div className="response-row">
                  <div className="response-label">Translated to {entry.targetLang}</div>
                  <div className="response-text highlight">{entry.translated}</div>
                </div>
                <div className="response-row">
                  <audio controls src={entry.audioUrl} style={{ width: '100%', marginTop: '6px' }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="sidebar-card">
        <div className="sidebar-card-header">
          <MicIcon />
          <div className="sidebar-title">How it works</div>
        </div>
        <div className="sidebar-card-body">
          <div className="sidebar-tip">
            <div className="sidebar-tip-num">1</div>
            <div className="sidebar-tip-text"><strong>Set what each person understands</strong> — this is the output language, not the input.</div>
          </div>
          <div className="sidebar-tip">
            <div className="sidebar-tip-num">2</div>
            <div className="sidebar-tip-text"><strong>Just speak or type</strong> — the language is detected automatically, no selection needed.</div>
          </div>
          <div className="sidebar-tip">
            <div className="sidebar-tip-num">3</div>
            <div className="sidebar-tip-text">Translated text and audio <strong>appear and play automatically</strong> for the other person.</div>
          </div>
        </div>
      </div>
      </div>
    </div>
    </PageTransition>
  );
}