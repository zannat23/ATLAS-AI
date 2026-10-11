import React from 'react';
import { BarChartIcon } from '../icons';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';
import Reveal from '../Reveal';

export default function Dashboard() {
  return (
    <PageTransition>
    <PageHeader
      icon={<BarChartIcon />}
      title="Evaluation Dashboard"
      subtitle="Measured accuracy for each module, from automated evaluation scripts."
    />
    <div className="main-container">
      <div className="card">
        <div className="card-dark-header">
          <BarChartIcon />
          <div className="card-dark-header-title">Evaluation results</div>
        </div>
        <div className="card-content">
        <div className="metric-note">
          These numbers come from <code>evaluate_resources.py</code>, <code>evaluate_medical.py</code> and
          <code> evaluate_voice.py</code>, saved to the <code>results/</code> folder. Re-run them any time to refresh.
        </div>

        <div className="metric-grid">
          <Reveal delay={0}>
            <div className="metric-card">
              <div className="metric-card-header">
                <div className="metric-card-title">Resource intent detection</div>
              </div>
              <div className="metric-card-body">
                <div className="metric-value signal">94.1%</div>
                <div className="metric-bar-track">
                  <div className="metric-bar-fill signal" style={{ width: '94.1%' }} />
                </div>
                <div className="metric-status">17 labeled queries tested</div>
                <div className="metric-caveat">
                  One false positive: "weather" matched the "food" keyword "eat" via substring search —
                  a known limitation of naive keyword matching.
                </div>
              </div>
            </div>
          </Reveal>

          <Reveal delay={0.12}>
            <div className="metric-card">
              <div className="metric-card-header">
                <div className="metric-card-title">Medical wound classifier</div>
              </div>
              <div className="metric-card-body">
                <div className="metric-value flare">100%</div>
                <div className="metric-bar-track">
                  <div className="metric-bar-fill flare" style={{ width: '100%' }} />
                </div>
                <div className="metric-status">240 validation images (6 classes)</div>
                <div className="metric-caveat">
                  Evaluated on a procedurally-generated synthetic dataset where each class has a distinct
                  color signature — this measures learnability of the synthetic task, not real-world
                  generalization. Real clinical image validation is planned as future work.
                </div>
              </div>
            </div>
          </Reveal>

          <Reveal delay={0.24}>
            <div className="metric-card">
              <div className="metric-card-header">
                <div className="metric-card-title">Voice language detection</div>
              </div>
              <div className="metric-card-body">
                <div className="metric-value faint">Pending</div>
                <div className="metric-bar-track">
                  <div className="metric-bar-fill faint striped" style={{ width: '100%' }} />
                </div>
                <div className="metric-status">5 audio samples queued for evaluation</div>
                <div className="metric-caveat">
                  Run <code>evaluate_voice.py</code> to measure Whisper's language detection accuracy
                  across the sample audio set.
                </div>
              </div>
            </div>
          </Reveal>
        </div>
        </div>
    </div>
    </div>
    </PageTransition>
  );
}