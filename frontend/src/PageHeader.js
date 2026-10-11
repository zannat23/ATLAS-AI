import React from 'react';
import AnimatedText from './AnimatedText';

export default function PageHeader({ icon, title, subtitle, image }) {
  return (
    <div
      className={`page-header ${image ? 'page-header-photo' : ''}`}
      style={image ? { backgroundImage: `url(${image})` } : undefined}
    >
      {image && <div className="page-header-overlay" />}
      <div className="page-header-content">
        <div className="page-header-icon">{icon}</div>
        <h1><AnimatedText text={title} tag="span" /></h1>
        <p>{subtitle}</p>
      </div>
    </div>
  );
}