# MVP / Demo Checklist

## Core Loop (The Vertical Slice)
- [ ] **Generate Quest**: AI creates a structured quest with multiple objectives.
- [ ] **Start Quest**: User initiates the quest and sees the "Phone Down" screen.
- [ ] **Go Outside**: User physically completes objectives (manual verification for demo).
- [ ] **Submit Evidence**: User takes/uploads photos for each objective.
- [ ] **Vision Verification**: Local vision model accepts/rejects evidence.
- [ ] **Complete Quest**: User finishes all objectives and receives XP.
- [ ] **Progress**: XP and streak are updated and visible on the home screen.

## Technical Requirements
- [ ] **PWA Support**: App is installable and responsive on mobile.
- [ ] **Local AI**: All generation and verification run via Ollama.
- [ ] **Persistence**: Quest state and progress are saved in SQLite.
- [ ] **Deployment**: App is hosted on Render.

## UI/UX Quality
- [ ] **Home Screen**: Simple "Start a Quest" with XP/Streak.
- [ ] **Quest Screen**: Clear objectives and a distinct "Start" action.
- [ ] **Evidence Screen**: Mobile-optimized camera/upload flow.
- [ ] **Completion Screen**: Playful success message and XP gain.
- [ ] **Visual Personality**: "Field notebook / Outdoor adventure" aesthetic.
