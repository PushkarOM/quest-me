import React, { useState, useEffect } from 'react';
import type { Quest } from './types/quest';
import './sw-register';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

type Screen = 'home' | 'quest' | 'phoneDown' | 'evidence' | 'complete';

const App: React.FC = () => {
  const [screen, setScreen] = useState<Screen>('home');
  const [activeQuest, setActiveQuest] = useState<Quest | null>(null);
  const [userStats, setUserStats] = useState<{total_xp: number, streak: number, completed_quests: number} | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [verifyingObj, setVerifyingObj] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      setLoading(true);
      try {
        const [meRes, activeRes] = await Promise.all([
          fetch(`${API_BASE}/api/me`),
          fetch(`${API_BASE}/api/quests/active`)
        ]);

        if (meRes.ok) setUserStats(await meRes.json());

        if (activeRes.ok) {
          const quest = await activeRes.json();
          if (quest) {
            setActiveQuest(quest);

            // Strict State Machine Mapping:
            // Backend Status -> Frontend Screen
            switch (quest.status) {
              case 'GENERATED':
                setScreen('quest');
                break;
              case 'STARTED':
                setScreen('evidence');
                break;
              case 'COMPLETED':
                setScreen('home');
                break;
              default:
                setScreen('home');
            }
          } else {
            setScreen('home');
          }
        }
      } catch (e: any) {
        console.error("Init failed", e);
        setError("Failed to restore your adventure. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const generateQuest = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/quests/generate`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to generate quest');
      const data = await res.json();
      setActiveQuest(data);
      setScreen('quest');
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
      setScreen('phoneDown');
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

      if (!res.ok) {
        throw new Error(data.detail || 'Verification failed');
      }

      if (data.valid && activeQuest) {
        // Update local state immediately to reflect verification
        const updatedQuest = {
          ...activeQuest,
          objectives: activeQuest.objectives.map(obj =>
            obj.id === objectiveId ? { ...obj, completed: true } : obj
          )
        };
        setActiveQuest(updatedQuest);
      } else {
        setError(`Verification failed: ${data.reason || 'Try a clearer photo'}`);
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
      const data = await res.json();

      setUserStats(prev => ({
        total_xp: data.total_xp,
        streak: data.streak,
        completed_quests: prev?.completed_quests ? prev.completed_quests + 1 : 1
      }));

      setScreen('complete');
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const renderHome = () => {
    const fieldNotes = [
      "The world is more interesting when you're looking for something.",
      "Nature is the greatest artist; we are just the observers.",
      "Look closer. The ordinary is where the extraordinary hides.",
      "The best way to find yourself is to get lost in the right direction.",
      "Silence is not the absence of sound, but the presence of nature."
    ];
    const todayNote = fieldNotes[Math.floor(Math.random() * fieldNotes.length)];

    return (
      <div className="flex flex-col items-start text-left gap-12 mt-16 px-4 animate-in fade-in slide-in-from-bottom-4 duration-700 w-full max-w-lg mx-auto">
        <header className="space-y-1 w-full">
          <h1 className="text-6xl font-black tracking-tighter text-quest-ink leading-none font-display">QUEST ME</h1>
          <p className="text-lg font-medium text-quest-ink opacity-60 italic font-serif">Touch Grass. Literally.</p>
        </header>

        <div className="flex flex-col gap-6 w-full">
          <div className="space-y-2 text-center">
            <p className="text-sm font-bold text-quest-ink opacity-60 uppercase tracking-widest font-mono">Your screen time ends here.</p>
            <h2 className="text-2xl font-black text-quest-ink font-display">Your next adventure is waiting.</h2>
          </div>

          <button
            className="group relative bg-quest-sage text-white text-xl font-black py-6 px-10 rounded-none shadow-[6px_6px_0px_var(--color-quest-ink)] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all w-full text-center uppercase tracking-tight font-display"
            onClick={generateQuest}
            disabled={loading}
          >
            <div className="flex flex-col items-center gap-1">
              <span>{loading ? 'Generating...' : 'START EXPLORING →'}</span>
              <span className="text-[10px] font-mono opacity-80 lowercase normal-case font-medium tracking-normal">20 minutes • No equipment needed</span>
            </div>
          </button>
        </div>

        <div className="w-full flex flex-col gap-8">
          <div className="flex justify-center gap-8 py-4 border-y border-quest-ink opacity-60 font-mono text-[11px] uppercase font-bold text-quest-ink">
            <div className="flex flex-col items-center gap-1">
              <span className="text-lg font-black font-display">{userStats?.completed_quests ?? 0}</span>
              <span>Quests</span>
            </div>
            <div className="flex flex-col items-center gap-1 border-x border-quest-ink px-8">
              <span className="text-lg font-black font-display">{userStats?.total_xp ?? 0}</span>
              <span>XP</span>
            </div>
            <div className="flex flex-col items-center gap-1">
              <span className="text-lg font-black font-display">🔥 {userStats?.streak ?? 0}</span>
              <span>Days</span>
            </div>
          </div>

          <div className="bg-quest-parchment border-l-4 border-quest-sage p-6 shadow-[4px_4px_0px_var(--color-quest-ink)] border-y-2 border-r-2 border-quest-ink relative">
            <span className="absolute -top-2 -right-2 bg-quest-ink text-white text-[8px] font-black px-1 py-0.5 rounded-sm rotate-3 uppercase font-mono">Field Note</span>
            <h3 className="font-mono text-[10px] uppercase font-bold text-gray-400 mb-3 tracking-widest">Today's Insight</h3>
            <p className="text-lg italic font-medium font-serif text-quest-ink opacity-90 leading-relaxed">
              "{todayNote}"
            </p>
          </div>
        </div>
      </div>
    );
  };

  const renderQuest = () => {
    if (!activeQuest) return null;
    return (
      <div className="bg-quest-parchment border-2 border-quest-ink p-6 sm:p-8 shadow-[8px_8px_0px_var(--color-quest-ink)] mx-4 mt-10 animate-in zoom-in-95 duration-300 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 bg-quest-base -mr-12 -mt-12 rotate-45 pointer-events-none" />

        <div className="flex flex-col gap-1 mb-8 relative z-10">
          <h2 className="text-4xl sm:text-5xl font-black text-quest-ink tracking-tighter font-display leading-none">{activeQuest.title}</h2>
          <div className="flex gap-2 items-center">
            <span className="font-mono text-[10px] font-bold px-2 py-0.5 bg-quest-ink text-white uppercase">{activeQuest.duration_minutes} MIN</span>
            <span className="font-mono text-[10px] font-bold px-2 py-0.5 border border-quest-ink text-quest-ink uppercase">{activeQuest.difficulty}</span>
          </div>
        </div>

        <div className="mb-10 relative z-10">
          <p className="text-lg sm:text-xl text-quest-ink font-black uppercase tracking-tight font-display mb-2">MISSION BRIEFING</p>
          <p className="text-base sm:text-lg text-quest-ink opacity-80 leading-relaxed italic font-medium border-l-4 border-quest-sage pl-4 font-serif">
            "{activeQuest.description}"
          </p>
          <p className="mt-4 text-sm font-bold text-quest-ink opacity-60 font-mono uppercase tracking-widest">Your mission is to notice what everyone else ignores.</p>
        </div>

        <div className="space-y-4 mb-10 relative z-10">
          {activeQuest.objectives.map((obj, idx) => (
            <div key={obj.id} className={`flex items-start gap-4 p-4 rounded-none border-2 transition-all ${obj.completed ? 'bg-gray-100 border-gray-300 opacity-50' : 'bg-white border-quest-ink'}`}>
              <span className="font-mono text-sm font-black text-quest-sage mt-1">{String(idx + 1).padStart(2, '0')}</span>
              <span className={`text-sm sm:text-base ${obj.completed ? 'line-through text-gray-400' : 'text-quest-ink font-medium font-serif'}`}>
                {obj.description}
              </span>
            </div>
          ))}
        </div>

        {activeQuest.bonus && (
          <div className="bg-quest-base border-2 border-dashed border-quest-earth p-5 rounded-none mb-10 relative z-10">
            <strong className="block text-quest-earth uppercase text-xs font-black mb-1 tracking-widest font-mono">Bonus Field Note:</strong>
            <p className="text-sm text-quest-ink italic font-medium font-serif">{activeQuest.bonus}</p>
          </div>
        )}

        <div className="flex flex-col items-center gap-4 relative z-10">
          <button
            className="w-full bg-quest-ink text-white text-2xl font-black py-5 rounded-none shadow-[6px_6px_0px_var(--color-quest-sage)] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all uppercase tracking-tighter font-display"
            onClick={startQuest}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'ACCEPT QUEST →'}
          </button>
          <p className="text-[10px] font-mono uppercase text-quest-ink opacity-60 font-bold tracking-widest">Once you start, put your phone away.</p>
        </div>
      </div>
    );
  };

  const renderPhoneDown = () => (
    <div className="flex flex-col items-center justify-center h-[85vh] text-center gap-6 px-6 animate-in fade-in duration-1000">
      <div className="relative">
        <h1 className="text-6xl font-black text-quest-ink tracking-tighter leading-none font-display">FIELD<br/>MODE.</h1>
        <div className="absolute -top-4 -right-8 text-5xl rotate-12 opacity-50">🌿</div>
      </div>
      <p className="text-2xl font-medium text-quest-ink opacity-70 font-serif">Eyes up. Phone in pocket.</p>
      <p className="text-quest-ink opacity-50 mb-12 max-w-xs font-mono text-xs uppercase tracking-widest">Only bring the device out to document your findings.</p>
      <button className="bg-quest-base border-2 border-quest-ink py-4 px-10 rounded-none font-bold text-quest-ink hover:bg-quest-parchment transition-all shadow-[4px_4px_0px_var(--color-quest-ink)] font-display" onClick={() => setScreen('evidence')}>
        I've Found Something
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
          <p className="text-quest-ink opacity-70 text-lg font-medium font-serif">All evidence verified. Your adventure is documented.</p>
          <button className="bg-quest-sage text-white text-2xl font-black py-5 px-12 rounded-none shadow-[6px_6px_0px_var(--color-quest-ink)] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all uppercase font-display" onClick={completeQuest} disabled={loading}>
            {loading ? 'Processing...' : 'Claim XP'}
          </button>
        </div>
      );
    }

    const currentObj = pendingObjectives[0];

    return (
      <div className="flex flex-col gap-8 max-w-md mx-auto mt-10 px-4 animate-in slide-in-from-right-4 duration-300">
        <div className="bg-quest-parchment border-2 border-quest-ink p-8 shadow-[8px_8px_0px_var(--color-quest-ink)]">
          <div className="flex justify-between items-center mb-4">
             <span className="font-mono text-[10px] font-black uppercase tracking-widest text-gray-400">Entry {pendingObjectives.indexOf(currentObj) + 1} / {activeQuest.objectives.length}</span>
             {verifyingObj === currentObj.id && <span className="text-[10px] font-bold text-quest-sage animate-pulse uppercase font-mono">Verifying...</span>}
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
        <button className="text-sm font-bold text-gray-400 hover:text-quest-earth transition-colors mx-auto underline underline-offset-4 font-mono" onClick={() => { setScreen('home'); }}>Abort Mission</button>
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center min-h-screen bg-quest-base relative w-full overflow-x-hidden">
      <div className="paper-texture" />

      {/* Atmospheric Decor: Pressed Leaf */}
      <div className="fixed bottom-10 right-[-20px] w-32 h-32 opacity-20 rotate-12 pointer-events-none z-0">
        <svg viewBox="0 0 100 100" fill="currentColor" className="text-quest-sage">
          <path d="M50 10 C30 30 20 50 50 90 C80 50 70 30 50 10 Z" />
          <path d="M50 10 L50 90 M50 30 L70 20 M50 50 L75 40 M50 70 L65 60 M50 30 L30 20 M50 50 L25 40 M50 70 L35 60" stroke="currentColor" strokeWidth="2" fill="none" />
        </svg>
      </div>

      <div className="w-full max-w-[430px] p-6 z-10">
        {error && (
          <div className="fixed top-5 left-1/2 -translate-x-1/2 bg-quest-earth text-white px-6 py-4 rounded-none z-50 flex items-center gap-3 shadow-[4px_4px_0px_#2C3333] font-bold animate-in slide-in-from-top-4">
            <span className="font-mono text-sm uppercase tracking-tighter">{error}</span> <button onClick={() => setError(null)} className="text-2xl leading-none hover:opacity-70">×</button>
          </div>
        )}
    {screen === 'home' && renderHome()}
    {screen === 'quest' && renderQuest()}
    {screen === 'phoneDown' && renderPhoneDown()}
    {screen === 'evidence' && renderEvidence()}
    {screen === 'complete' && (
          <div className="flex flex-col items-center justify-center text-center gap-8 mt-24 px-6 animate-in zoom-in-95 duration-500">
            <div className="text-7xl">📜</div>
            <h1 className="text-6xl font-black text-quest-ink tracking-tighter font-display">QUEST COMPLETE</h1>
            <p className="text-xl text-quest-ink opacity-80 font-medium italic font-serif">Log closed. You touched grass.</p>
            <button className="bg-quest-sage text-white text-2xl font-black py-5 px-12 rounded-none shadow-[6px_6px_0px_var(--color-quest-ink)] active:translate-x-1 active:translate-y-1 active:shadow-none transition-all uppercase tracking-tighter font-display" onClick={() => { setScreen('home'); }}>
              New Adventure
            </button>
          </div>
        )}
      </div>

      {/* MLH & Hacktoberfest Branding Footer */}
      <footer className="mt-auto mb-8 flex flex-col items-center gap-4 opacity-60">
        <div className="flex items-center gap-3 px-4 py-2 border-2 border-quest-ink bg-quest-parchment rotate-[-1deg] shadow-[2px_2px_0px_var(--color-quest-ink)]">
          <span className="text-[10px] font-black uppercase tracking-widest font-mono text-quest-ink">Built for MLH & Hacktoberfest 2026</span>
        </div>
        <p className="text-[10px] font-mono uppercase text-quest-ink opacity-40">QuestMe // Field Log v1.0</p>
      </footer>
    </div>
  );
};

export default App;
