import React from 'react';
import { UsersIcon } from '../icons';
import { TEAM_MEMBERS, PROJECT_TITLE } from '../data';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';
import Reveal from '../Reveal';

export default function Team() {
  return (
    <PageTransition>
    <PageHeader
      icon={<UsersIcon />}
      title="Team & Contact"
      subtitle="Edit the placeholders below in data.js with your real project details."
    />
    <div className="main-container">
      <div className="card">
        <div className="card-dark-header">
          <UsersIcon />
          <div className="card-dark-header-title">Meet the team</div>
        </div>
        <div className="card-content">
        <div className="mission-quote">
          <span className="mission-quote-mark">&ldquo;</span>
          Built by students who believe technology should reach people fastest when they need it most —
          in the middle of a crisis, with no internet, in a language they trust.
        </div>

        <div className="team-grid">
          {TEAM_MEMBERS.map((m, i) => (
            <Reveal key={m.name + m.role} delay={i * 0.1} className="team-card">
              <div className="team-avatar">{m.name.charAt(0)}</div>
              <div className="team-name">{m.name}</div>
              <div className="team-role">{m.role}</div>
              <div className="team-meta">{m.meta}</div>
            </Reveal>
          ))}
        </div>

        <div className="contact-block">
          <div className="contact-row">
            <span className="contact-label">Project</span>
            <span className="contact-value">{PROJECT_TITLE}</span>
          </div>
          <div className="contact-row">
            <span className="contact-label">Guide</span>
            <span className="contact-value">Er. Aayush Pratap Singh</span>
          </div>
          <div className="contact-row">
            <span className="contact-label">Department</span>
            <span className="contact-value">AI &amp; ML Department</span>
          </div>
          <div className="contact-row">
            <span className="contact-label">Institution</span>
            <span className="contact-value">Shri Ramswaroop Memorial College of Engineering and Management</span>
          </div>
          <div className="contact-row">
            <span className="contact-label">Academic year</span>
            <span className="contact-value">2023-2027</span>
          </div>
          <div className="contact-row">
            <span className="contact-label">Email</span>
            <span className="contact-value">zannatfeb23@gmail.com</span>
          </div>
        </div>
        </div>
    </div>
    </div>
    </PageTransition>
  );
}