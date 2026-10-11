import React from 'react';
import { InfoIcon, MicIcon, PulseIcon, PinIcon } from '../icons';
import { PROJECT_TITLE } from '../data';
import aboutImg from '../assets/about.jpg';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';

export default function About() {
  return (
    <PageTransition>
    <PageHeader
      icon={<InfoIcon />}
      title="About This Project"
      subtitle={PROJECT_TITLE}
      image={aboutImg}
    />
    <div className="main-container">
      <div className="page-layout">
      <div className="card">
        <div className="card-dark-header">
          <InfoIcon />
          <div className="card-dark-header-title">Mission</div>
        </div>
        <div className="card-content">
        <div className="about-body">
          <p className="about-intro">
            <strong>This project</strong> is an offline multilingual AI system designed to help displaced
            people, refugees, and crisis victims overcome three barriers at once.
          </p>

          <div className="about-row">
            <MicIcon />
            <div>
              <div className="about-row-title">Language barrier</div>
              <div className="about-row-desc">Real-time translation across 60+ languages</div>
            </div>
          </div>
          <div className="about-row">
            <PulseIcon />
            <div>
              <div className="about-row-title">Medical barrier</div>
              <div className="about-row-desc">Wound triage and first aid guidance</div>
            </div>
          </div>
          <div className="about-row">
            <PinIcon />
            <div>
              <div className="about-row-title">Geographic barrier</div>
              <div className="about-row-desc">Offline resource and shelter locator</div>
            </div>
          </div>

          <div className="tech-stack">
            <strong>Tech stack: </strong>
            PyTorch, Whisper, NLLB-200, FastAPI, React.js, RTX 3050 GPU
          </div>
        </div>
        </div>
      </div>

      <div className="sidebar-card">
        <div className="sidebar-card-header">
          <InfoIcon />
          <div className="sidebar-title">Quick facts</div>
        </div>
        <div className="sidebar-card-body">
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">1</div>
          <div className="sidebar-tip-text"><strong>3 AI models</strong> working together — Whisper, NLLB-200, EfficientNet-B0.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">2</div>
          <div className="sidebar-tip-text">Runs entirely on a <strong>local GPU</strong> — no internet connection needed.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">3</div>
          <div className="sidebar-tip-text">Built as a <strong>B.Tech final year project</strong>, AI &amp; ML Department.</div>
        </div>
        </div>
      </div>
      </div>
    </div>
    </PageTransition>
  );
}