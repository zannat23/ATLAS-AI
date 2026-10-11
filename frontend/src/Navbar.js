import React from 'react';
import { NavLink } from 'react-router-dom';
import { NAV_ITEMS } from './data';

export default function Navbar() {
  return (
    <nav className="navbar">
      <NavLink to="/" className="navbar-brand" style={{ textDecoration: 'none' }}>
        ATLAS<span>AI</span>
      </NavLink>
      <div className="navbar-links">
        {NAV_ITEMS.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `nav-btn ${isActive ? 'active' : ''}`}
          >{item.label}</NavLink>
        ))}
      </div>
    </nav>
  );
}