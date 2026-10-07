import React, { useState, useEffect } from 'react';
import type { Quest, Objective, QuestStatus } from './types/quest';
import { MOCK_QUEST } from './types/quest';

const API_BASE = 'http://localhost:8000';

const App: React.FC = () => {
  const [status, setStatus] = useState<QuestStatus>('IDLE');
  const [activeQuest, setActiveQuest] = useState<Quest | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [verifyingObj, setVerifyingObj] = useState<string | null>(null);

  const generateQuest = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/quests/generate`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to generate quest');
      const data = await res.json();
      setActiveQuest(data);
      setStatus('GENERATED');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const startQuest = async () => {
    if (!activeQuest) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/quests/${activeQuest.id}/start`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to start quest');
      setStatus('STARTED');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const submitEvidence = async (objectiveId: string, file: File) => {
    setVerifyingObj(objectiveId);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await fetch(`${API_BASE}/api/quests/${activeQuest?.id}/objectives/${objectiveId}/evidence`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Verification failed');
      if (activeQuest) {
        setActiveQuest({
          ...activeQuest,
          objectives: activeQuest.objectives.map(obj =>
            obj.id === objectiveId ? { ...obj, completed: true } : obj
          )
        });
      }
      return data;
    } catch (e: any) {
      setError(e.message);
      throw e;
    } finally {
      setVerifyingObj(null);
    }
  };

  const completeQuest = async () => {
    if (!activeQuest) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/quests/${activeQuest?.id}/complete`, { method: 'POST' });
      if (!res.ok) throw new Error('Could not complete quest');
      setStatus('COMPLETED');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const renderHome = () => (
    <div className="flex flex-col items-start text-left gap-12 mt-16 px-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <header className="space-y-1">
        <h1 className="text-6xl font-black tracking-tighter text-quest-ink leading-none font-display">QUEST ME</h1>
        <p className="text-lg font-medium text-quest-ink opacity-60 italic">Touch Grass. Literally.</p>
      </header>

      <div className="w-full max-w-sm bg-white border-l-8 border-quest-sage p-6 shadow-[4px_4px_0px_#2C3333] border-y-2 border-r-2 border-quest-ink relative">
        <div className="absolute -top-3 -right-3 bg-quest-ink text-white text-[10px] font-black px-2 py-1 rounded-sm rotate-3">ACTIVE LOG</div>
        <h3 className="font-mono text-[10px] uppercase font-bold text-gray-400 mb-4 tracking-widest">Explorer Log // v1.0</h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="flex flex-col gap-1">
            <span className="text-3xl font-black text-quest-ink">12</span>
            <span className="text-[9px] uppercase font-bold opacity-80 text-quest-ink">Completed</span>
          </div>
          <div className="flex flex-col gap-1 border-x-2 border-gray-200 px-2">
            <span className="text-3xl font-black text-quest-ink">340</span>
            <span className="text-[9px] uppercase font-bold opacity-80 text-quest-ink">Total XP</span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-3xl font-black text-quest-ink">🔥 4</span>
            <span className="text-[9px] uppercase font-bold opacity-80 text-quest-ink">Day Streak</span>
          </div>
        </div>
      </div>

      <button
        className="group relative bg-quest-sage text-white text-xl font-black py-5 px-10 rounded-none shadow-[6px_6px_0px_#2C3333] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all w-full max-w-sm text-left uppercase tracking-tight"
        onClick={generateQuest}
        disabled={loading}
      >
        <span className="relative z-10">{loading ? 'Generating...' : 'Start a Quest →'}</span>
      </button>
    </div>
  );

  const renderQuest = () => {
    if (!activeQuest) return null;
    return (
      <div className="bg-white border-2 border-quest-ink p-8 shadow-[8px_8px_0px_#2C3333] mx-4 mt-10 animate-in zoom-in-95 duration-300 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 bg-quest-parchment -mr-12 -mt-12 rotate-45 pointer-events-none" />

        <div className="flex justify-between items-start mb-6 relative z-10">
          <h2 className="text-4xl font-black text-quest-ink tracking-tight font-display leading-none">{activeQuest.title}</h2>
          <div className="flex gap-2">
            <span className="font-mono text-[10px] font-bold px-2 py-1 border border-quest-ink text-quest-ink uppercase">{activeQuest.duration_minutes} MIN</span>
            <span className="font-mono text-[10px] font-bold px-2 py-1 border border-quest-ink text-quest-ink uppercase">{activeQuest.difficulty}</span>
          </div>
        </div>

        <p className="text-lg text-gray-600 leading-relaxed mb-10 relative z-10 italic font-medium border-l-4 border-quest-sage pl-4">
          "{activeQuest.description}"
        </p>

        <div className="space-y-4 mb-10 relative z-10">
          {activeQuest.objectives.map((obj, idx) => (
            <div key={obj.id} className={`flex items-start gap-4 p-4 rounded-lg border-2 transition-all ${obj.completed ? 'bg-gray-50 border-gray-200 opacity-50' : 'bg-white border-quest-ink'}`}>
              <div className={`mt-1 w-5 h-5 rounded-sm border-2 flex items-center justify-center transition-colors ${obj.completed ? 'bg-quest-leaf border-quest-leaf' : 'border-quest-ink bg-white'}`}>
                {obj.completed && <span className="text-white text-[10px] font-bold">✓</span>}
              </div>
              <span className={`text-base ${obj.completed ? 'line-through text-gray-400' : 'text-quest-ink font-medium'}`}>
                {obj.description}
              </span>
            </div>
          ))}
        </div>

        {activeQuest.bonus && (
          <div className="bg-quest-parchment border-2 border-dashed border-quest-earth p-5 rounded-none mb-10 relative z-10">
            <strong className="block text-quest-earth uppercase text-xs font-black mb-1 tracking-widest font-mono">Bonus Field Note:</strong>
            <p className="text-sm text-quest-ink italic font-medium">{activeQuest.bonus}</p>
          </div>
        )}

        <button
          className="w-full bg-quest-ink text-white text-2xl font-black py-5 rounded-none shadow-[6px_6px_0px_#4B6344] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all uppercase tracking-tighter"
          onClick={startQuest}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Begin Adventure'}
        </button>
      </div>
    );
  };

  const renderPhoneDown = () => (
    <div className="flex flex-col items-center justify-center h-[85vh] text-center gap-6 px-6 animate-in fade-in duration-1000">
      <div className="relative">
        <h1 className="text-7xl font-black text-quest-ink tracking-tighter leading-none font-display">PHONE<br/>DOWN.</h1>
        <div className="absolute -top-4 -right-8 text-5xl rotate-12 opacity-50">🌿</div>
      </div>
      <p className="text-2xl font-medium text-quest-ink opacity-70">Put the device away.</p>
      <p className="text-gray-500 mb-12 max-w-xs font-mono text-xs uppercase tracking-widest">The physical world is waiting.</p>
      <button className="bg-quest-base border-2 border-quest-ink py-4 px-10 rounded-none font-bold text-quest-ink hover:bg-quest-parchment transition-all shadow-[4px_4px_0px_#2C3333]" onClick={() => setStatus('IN_PROGRESS')}>
        I'm Back
      </button>
    </div>
  );

  const renderEvidence = () => {
    if (!activeQuest) return null;
    const pendingObjectives = activeQuest.objectives.filter(obj => !obj.completed);

    if (pendingObjectives.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center text-center gap-8 mt-20 px-6 animate-in slide-in-from-bottom-8 duration-500">
          <div className="text-6xl">📜</div>
          <h2 className="text-4xl font-black text-quest-ink tracking-tight font-display">Field Log Complete</h2>
          <p className="text-gray-500 text-lg font-medium">All evidence verified. Your adventure is documented.</p>
          <button className="bg-quest-sage text-white text-2xl font-black py-5 px-12 rounded-none shadow-[6px_6px_0px_#2C3333] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all uppercase" onClick={completeQuest} disabled={loading}>
            {loading ? 'Processing...' : 'Claim XP'}
          </button>
        </div>
      );
    }

    const currentObj = pendingObjectives[0];

    return (
      <div className="flex flex-col gap-8 max-w-md mx-auto mt-10 px-4 animate-in slide-in-from-right-4 duration-300">
        <div className="bg-white border-2 border-quest-ink p-8 shadow-[8px_8px_0px_#2C3333]">
          <div className="flex justify-between items-center mb-4">
             <span className="font-mono text-[10px] font-black uppercase tracking-widest text-gray-400">Entry {pendingObjectives.indexOf(currentObj) + 1} / {pendingObjectives.length}</span>
             {verifyingObj === currentObj.id && <span className="text-[10px] font-bold text-quest-sage animate-pulse uppercase">Verifying...</span>}
          </div>
          <p className="text-2xl font-black text-quest-ink leading-tight mb-8 font-display">{currentObj.description}</p>

          <label className="group flex flex-col items-center justify-center w-full h-64 border-4 border-dashed border-gray-300 rounded-none cursor-pointer hover:border-quest-sage hover:bg-green-50 transition-all">
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <div className="text-5xl mb-4 group-hover:scale-110 transition-transform">📸</div>
              <p className="text-sm font-bold text-gray-400 group-hover:text-quest-sage transition-colors uppercase tracking-widest font-mono">Capture Evidence</p>
            </div>
            <input
              type="file"
              accept="image/*"
              capture="environment"
              className="hidden"
              onChange={async (e) => {
                const file = e.target.files?.[0];
                if (file) {
                  try {
                    await submitEvidence(currentObj.id, file);
                  } catch (err) { }
                }
              }}
            />
          </label>
        </div>
        <button className="text-sm font-bold text-gray-400 hover:text-quest-earth transition-colors mx-auto underline underline-offset-4 font-mono" onClick={() => setStatus('IDLE')}>Abort Mission</button>
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-quest-base relative w-full">
      <div className="paper-texture" />
      <div className="w-full max-w-[430px] p-6">
        {error && (
          <div className="fixed top-5 left-1/2 -translate-x-1/2 bg-quest-earth text-white px-6 py-4 rounded-none z-50 flex items-center gap-3 shadow-[4px_4px_0px_#2C3333] font-bold animate-in slide-in-from-top-4">
            <span className="font-mono text-sm uppercase tracking-tighter">{error}</span> <button onClick={() => setError(null)} className="text-2xl leading-none hover:opacity-70">×</button>
          </div>
        )}
        {status === 'IDLE' && renderHome()}
        {status === 'GENERATED' && renderQuest()}
        {status === 'STARTED' && renderPhoneDown()}
        {status === 'IN_PROGRESS' && renderEvidence()}
        {status === 'COMPLETED' && (
          <div className="flex flex-col items-center justify-center text-center gap-8 mt-24 px-6 animate-in zoom-in-95 duration-500">
            <div className="text-7xl">📜</div>
            <h1 className="text-6xl font-black text-quest-ink tracking-tighter font-display">QUEST COMPLETE</h1>
            <p className="text-xl text-gray-600 font-medium italic">Log closed. You touched grass.</p>
            <button className="bg-quest-sage text-white text-2xl font-black py-5 px-12 rounded-none shadow-[6px_6px_0px_#2C3333] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all uppercase tracking-tighter" onClick={() => setStatus('IDLE')}>
              New Adventure
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
