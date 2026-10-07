import React from 'react';

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
  duration: string;
  difficulty: string;
  objectives: Objective[];
  bonus?: string;
  xp: number;
}

export const MOCK_QUEST: Quest = {
  id: 'quest_1',
  title: 'Urban Naturalist',
  description: 'Explore your surroundings with fresh eyes and find nature hiding in the city.',
  duration: '20 MIN',
  difficulty: 'EASY',
  objectives: [
    { id: 'obj_1', description: 'Find a plant you have never noticed before.', completed: false },
    { id: 'obj_2', description: 'Find a naturally repeating pattern.', completed: false },
    { id: 'obj_3', description: 'Find something in nature changed by humans.', completed: false },
  ],
  bonus: 'Find something yellow that isn\'t manufactured.',
  xp: 100,
};
