import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MicIcon, PulseIcon, PinIcon } from '../icons';
import { MODULES, PROJECT_TITLE } from '../data';
import heroImg from '../assets/hero.jpg';
import PageTransition from '../PageTransition';
import AnimatedText from '../AnimatedText';
import Reveal from '../Reveal';

const ICONS = { mic: <MicIcon />, pulse: <PulseIcon />, pin: <PinIcon /> };

const cardContainer = {
  initial: {},
  animate: { transition: { staggerChildren: 0.08, delayChildren: 0.25 } },
};
const cardItem = {
  initial: { opacity: 0, y: 22 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] } },
};

export default function Home() {
  return (
    <PageTransition>
      <div className="hero">
        <div>
          <div className="formal-title">{PROJECT_TITLE}</div>
          <h1>
            <AnimatedText text="Help that works" tag="span" className="block-line" />
            <br />
            <AnimatedText text="when nothing else does" tag="span" className="block-line" />
          </h1>
          <p>
            Translation, medical triage, and resource location — fully offline.
          </p>
          <div className="hero-actions">
            <Link to="/voice" className="hero-cta primary">Open Voice Bridge</Link>
            <Link to="/how" className="hero-cta">How it works</Link>
          </div>
        </div>

        <div>
          <div className="hero-image hero-image-full">
            <img src={heroImg} alt="Community support" />
          </div>
        </div>
      </div>

      <div className="marquee">
        <div className="marquee-track">
          <span>Real-time translation</span>
          <span>Medical triage</span>
          <span>Resource locator</span>
          <span>Offline-first</span>
          <span>60+ languages</span>
          <span>Real-time translation</span>
          <span>Medical triage</span>
          <span>Resource locator</span>
          <span>Offline-first</span>
          <span>60+ languages</span>
        </div>
      </div>

      <div className="main-container">
        <Reveal>
          <div className="impact-band">
            <div className="impact-item">
              <div className="impact-num">60+</div>
              <div className="impact-label">Languages bridged in real time</div>
            </div>
            <div className="impact-item">
              <div className="impact-num">3</div>
              <div className="impact-label">AI systems working offline together</div>
            </div>
            <div className="impact-item">
              <div className="impact-num">6</div>
              <div className="impact-label">Wound categories auto-classified</div>
            </div>
            <div className="impact-item">
              <div className="impact-num">0</div>
              <div className="impact-label">Internet connection required</div>
            </div>
          </div>
        </Reveal>

        <motion.div className="modules-grid" variants={cardContainer} initial="initial" animate="animate">
          {MODULES.map(m => (
            <motion.div key={m.path} variants={cardItem} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Link to={m.path} className="module-card" style={{ textDecoration: 'none', color: 'inherit', display: 'block' }}>
                <div className="module-image">
                  <m.Illustration />
                </div>
                <div className="module-icon">{ICONS[m.iconKey]}</div>
                <div className="module-name">{m.name}</div>
                <div className="module-desc">{m.desc}</div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </PageTransition>
  );
}