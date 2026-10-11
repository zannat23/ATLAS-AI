import React, { useState } from 'react';
import axios from 'axios';
import { PinIcon, SearchIcon } from '../icons';
import { RESOURCE_TYPES, API_URL } from '../data';
import resourcesImg from '../assets/resources.jpg';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';

export default function Resources() {
  const [resQuery, setResQuery] = useState('');
  const [resType, setResType] = useState(null);
  const [resResults, setResResults] = useState([]);
  const [resLoading, setResLoading] = useState(false);

  const handleResourceSearch = async (type = null) => {
    setResLoading(true);
    const useType = type !== null ? type : resType;
    try {
      const res = await axios.post(`${API_URL}/api/resources/search`, {
        query: resQuery || null,
        resource_type: useType || null,
        lat: 18.5204,
        lon: 73.8567,
        limit: 8
      });
      setResResults(res.data.results);
    } catch (err) {
      console.error(err);
    }
    setResLoading(false);
  };

  const toggleResourceType = (id) => {
    const next = resType === id ? null : id;
    setResType(next);
    handleResourceSearch(next);
  };

  return (
    <PageTransition>
    <PageHeader
      icon={<PinIcon />}
      title="Crisis Resource Locator"
      subtitle="Find the nearest hospitals, water points, shelters and NGOs."
      image={resourcesImg}
    />
    <div className="main-container">
      <div className="page-layout">
      <div className="card">
        <div className="card-dark-header">
          <PinIcon />
          <div className="card-dark-header-title">Search resources</div>
        </div>
        <div className="card-content">
        <h3 className="section-heading">Help, wherever you are</h3>
        <p className="section-sub">Search hospitals, water points, shelters, and more — ranked by distance.</p>
        <div className="field-label">What do you need?</div>
        <div className="search-row">
          <input
            type="text"
            className="search-input"
            value={resQuery}
            onChange={e => setResQuery(e.target.value)}
            placeholder="Type: I need water / hospital / shelter..."
            onKeyDown={e => e.key === 'Enter' && handleResourceSearch()}
          />
          <button className="send-btn" style={{ marginLeft: 0 }} onClick={() => handleResourceSearch()} disabled={resLoading}>
            <SearchIcon />
          </button>
        </div>

        <div className="filter-chips">
          {RESOURCE_TYPES.map(t => (
            <button
              key={t.id}
              className={`filter-chip ${resType === t.id ? 'active' : ''}`}
              onClick={() => toggleResourceType(t.id)}
            >{t.label}</button>
          ))}
        </div>

        {resResults.length > 0 && (
          <div className="resource-list">
            {resResults.map(r => (
              <div key={r.id} className="resource-item">
                <div>
                  <div className="resource-name">{r.name}</div>
                  {r.address && <div className="resource-address">{r.address}</div>}
                  {r.phone && <div className="resource-phone">{r.phone}</div>}
                </div>
                <div className="resource-meta">
                  <div className="resource-distance">{r.distance_km} km</div>
                  <div className="resource-type">{r.type}</div>
                </div>
              </div>
            ))}
          </div>
        )}

        {resResults.length === 0 && !resLoading && (
          <div className="empty-state">
            <SearchIcon />
            <p>Search for resources or select a filter above</p>
          </div>
        )}
        </div>
      </div>

      <div className="sidebar-card">
        <div className="sidebar-card-header">
          <PinIcon />
          <div className="sidebar-title">How the search works</div>
        </div>
        <div className="sidebar-card-body">
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">1</div>
          <div className="sidebar-tip-text">Type your need in <strong>plain language</strong> — "I need water" works fine.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">2</div>
          <div className="sidebar-tip-text">Use the <strong>category filters</strong> for faster, more precise results.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">3</div>
          <div className="sidebar-tip-text">Results are ranked by <strong>distance</strong> using the Haversine formula.</div>
        </div>
        <div className="sidebar-tip">
          <div className="sidebar-tip-num">4</div>
          <div className="sidebar-tip-text">Works fully <strong>offline</strong> against the local SQLite database.</div>
        </div>
        </div>
      </div>
      </div>
    </div>
    </PageTransition>
  );
}