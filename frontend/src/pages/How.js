import React from 'react';
import { FlowIcon, MicIcon, PulseIcon, PinIcon } from '../icons';
import { VOICE_PIPELINE, MEDICAL_PIPELINE, RESOURCE_PIPELINE } from '../data';
import PageTransition from '../PageTransition';
import PageHeader from '../PageHeader';
import Reveal from '../Reveal';

function PipelineBlock({ icon, title, sub, badges, steps }) {
  return (
    <Reveal>
      <div className="pipeline-block">
        <div className="pipeline-title">{icon} {title}</div>
        <div className="pipeline-sub">{sub}</div>
        <div className="tech-badges">
          {badges.map(b => <span key={b} className="tech-badge">{b}</span>)}
        </div>
        <div className="pipeline-steps">
          {steps.map((step, i) => (
            <React.Fragment key={step.name}>
              <Reveal delay={i * 0.08} y={14} className="pipeline-step">
                <div className="pipeline-step-num">{i + 1}</div>
                <div className="pipeline-step-name">{step.name}</div>
                <div className="pipeline-step-desc">{step.desc}</div>
              </Reveal>
              {i < steps.length - 1 && <div className="pipeline-arrow">&rarr;</div>}
            </React.Fragment>
          ))}
        </div>
      </div>
    </Reveal>
  );
}

export default function How() {
  return (
    <PageTransition>
    <PageHeader
      icon={<FlowIcon />}
      title="How It Works"
      subtitle="The processing pipeline behind each module."
    />
    <div className="main-container">
      <div className="card">
        <div className="card-dark-header">
          <FlowIcon />
          <div className="card-dark-header-title">Processing pipelines</div>
        </div>
        <div className="card-content">
        <PipelineBlock
          icon={<MicIcon />}
          title="Voice Bridge"
          sub="Speech-to-text, translation, and speech synthesis working together"
          badges={['Whisper', 'NLLB-200', 'gTTS']}
          steps={VOICE_PIPELINE}
        />
        <PipelineBlock
          icon={<PulseIcon />}
          title="Medical Triage"
          sub="Image classification trained to recognize 6 wound categories"
          badges={['EfficientNet-B0', 'PyTorch', '224x224 input']}
          steps={MEDICAL_PIPELINE}
        />
        <PipelineBlock
          icon={<PinIcon />}
          title="Resource Locator"
          sub="Keyword intent detection with offline database lookup"
          badges={['SQLite', 'Haversine formula', 'Keyword matching']}
          steps={RESOURCE_PIPELINE}
        />
        </div>
    </div>
    </div>
    </PageTransition>
  );
}