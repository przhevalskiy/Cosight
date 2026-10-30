import type { AgentId } from './registry';

/** 4×4 fuzzy agent icon sheet (1024×1024) */
export const AGENT_SPRITE_SHEET = '/agent-sprites.png';

/** Grid cell per specialist (col, row — 0-indexed, top-left) */
export const AGENT_SPRITE: Record<AgentId, { col: number; row: number }> = {
  overview: { col: 3, row: 3 }, // gold laurel — main cross-channel
  web:      { col: 1, row: 0 }, // orange cube / traffic
  search:   { col: 3, row: 1 }, // compass stone — discovery
  email:    { col: 0, row: 2 }, // cloud + quill
  social:   { col: 2, row: 1 }, // star mascot
  reports:  { col: 1, row: 3 }, // d20 / structured output
  chat:     { col: 0, row: 0 }, // monocle analyst — orchestrator
};

export function spriteBackgroundPosition(col: number, row: number): string {
  const x = col === 0 ? '0%' : col === 3 ? '100%' : `${(col / 3) * 100}%`;
  const y = row === 0 ? '0%' : row === 3 ? '100%' : `${(row / 3) * 100}%`;
  return `${x} ${y}`;
}

export function getAgentSpriteCell(agentId: string): { col: number; row: number } {
  const cell = AGENT_SPRITE[agentId as AgentId];
  return cell ?? AGENT_SPRITE.chat;
}
