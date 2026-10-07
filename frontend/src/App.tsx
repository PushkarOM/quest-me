import React, { useState } from 'react';
import { MOCK_QUEST, QuestStatus } from './types/quest';

const App: React.FC = () => {
  const [status, setStatus] = useState<QuestStatus>('IDLE');
  const [activeQuest, setActiveQuest] = useState(MOCK_QUEST);

  const renderHome = () => (
    <div className="home-container">
      <header>
        <h1>QUEST ME</h1>
        <p className="tagline">Touch Grass. Literally.</p>
      </header>

      <div className="stats-card">
        <div className="stat">
          <span className="value">12</span>
          <span className="label">Quests Completed</span>
        </div>
        <div className="stat">
          <span className="value">340 XP</span>
          <span className="label">Current Progress</span>
        </div>
        <div className="stat">
          <span className="value">🔥 4</span>
          <span className="label">Day Streak</span>
        </div>
      </div>

      <button className="primary-btn" onClick={() => setStatus('GENERATED')}>
        Start a Quest
      </button>
    </div>
  );

  const renderQuest = () => (
    <div className="quest-container">
      <div className="quest-header">
        <h2>{activeQuest.title}</h2>
        <div className="quest-meta">
          <span>{activeQuest.duration}</span>
          <span>{activeQuest.difficulty}</span>
        </div>
      </div>

      <p className="quest-desc">{activeQuest.description}</p>

      <div className="objectives-list">
        {activeQuest.objectives.map(obj => (
          <div key={obj.id} className="objective-item">
            <input type="checkbox" readOnly />
            <span>{obj.description}</span>
          </div>
        ))}
      </div>

      {activeQuest.bonus && (
        <div className="bonus-box">
          <strong>BONUS:</strong> {activeQuest.bonus}
        </div>
      )}

      <button className="primary-btn" onClick={() => setStatus('STARTED')}>
        START QUEST
      </button>
    </div>
  );

  const renderPhoneDown = () => (
    <div className="phone-down-container">
      <h1>PHONE DOWN.</h1>
      <p>Go explore.</p>
      <p className="subtext">We'll be here when you get back.</p>
      <button className="secondary-btn" onClick={() => setStatus('IDLE')}>
        I'm Back
      </button>
    </div>
  );

  return (
    <div className="app-wrapper">
      {status === 'IDLE' && renderHome()}
      {status === 'GENERATED' && renderQuest()}
      {status === 'STARTED' && renderPhoneDown()}
    </div>
  );
};

export default App;
