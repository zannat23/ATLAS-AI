import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import './App.css';

import Navbar from './Navbar';
import Home from './pages/Home';
import Voice from './pages/Voice';
import Medical from './pages/Medical';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import How from './pages/How';
import Team from './pages/Team';
import About from './pages/About';
import { PROJECT_TITLE, NAV_ITEMS } from './data';
import { Link } from 'react-router-dom';

function AnimatedRoutes() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/voice" element={<Voice />} />
        <Route path="/medical" element={<Medical />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/how" element={<How />} />
        <Route path="/team" element={<Team />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div>
        <Navbar />
        <AnimatedRoutes />
        <div className="footer">
          <div className="footer-inner">
            <div className="footer-col footer-col-wide">
              <div className="footer-brand">ATLAS<span>AI</span></div>
              <div className="footer-title">{PROJECT_TITLE}</div>
              <p className="footer-desc">
                An offline-first system built to help displaced people, aid workers, and disaster
                response teams overcome language, medical, and geographic barriers in a crisis.
              </p>
              <div className="footer-badges">
                <span className="footer-badge">100% Offline</span>
                <span className="footer-badge">60+ Languages</span>
                <span className="footer-badge">Open Source</span>
              </div>
            </div>
            <div className="footer-col">
              <div className="footer-heading">Modules</div>
              {NAV_ITEMS.slice(0, 3).map(item => (
                <Link key={item.path} to={item.path} className="footer-link">{item.label}</Link>
              ))}
            </div>
            <div className="footer-col">
              <div className="footer-heading">Project</div>
              {NAV_ITEMS.slice(3).map(item => (
                <Link key={item.path} to={item.path} className="footer-link">{item.label}</Link>
              ))}
            </div>
          </div>
          <div className="footer-bottom">
            <span>© 2027 ATLAS AI — B.Tech final year project · AI &amp; ML Department</span>
            <span>SRMCEM, Lucknow (AKTU)</span>
          </div>
        </div>
      </div>
    </BrowserRouter>
  );
}