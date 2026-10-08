export type QuestStatus = 'IDLE' | 'GENERATED' | 'STARTED' | 'COMPLETED';

export interface Objective {
  id: string;
  description: string;
  completed: boolean;
}

export interface Quest {
  id: string;
  title: string;
  description: string;
  duration_minutes: number;
  difficulty: string;
  objectives: Objective[];
  bonus?: string;
  xp: number;
}
