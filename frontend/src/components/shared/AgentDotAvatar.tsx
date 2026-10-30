/**
 * Fuzzy agent icon from the 4×4 sprite sheet (one character per specialist).
 */
import React from 'react';
import { getAgent } from '../../agents/registry';
import {
  AGENT_SPRITE_SHEET,
  getAgentSpriteCell,
  spriteBackgroundPosition,
} from '../../agents/spriteSheet';
import './AgentDotAvatar.css';

interface Props {
  agentId: string;
  size?: number;
  pulse?: boolean;
  className?: string;
}

export const AgentDotAvatar: React.FC<Props> = ({
  agentId,
  size = 18,
  pulse = false,
  className = '',
}) => {
  const agent = getAgent(agentId);
  const { col, row } = getAgentSpriteCell(agentId);

  return (
    <span
      className={`agent-dot-avatar ${pulse ? 'agent-dot-avatar--pulse' : ''} ${className}`.trim()}
      style={{
        width: size,
        height: size,
        backgroundImage: `url(${AGENT_SPRITE_SHEET})`,
        backgroundSize: '400% 400%',
        backgroundPosition: spriteBackgroundPosition(col, row),
      }}
      title={`${agent.displayName} — ${agent.domain}`}
      role="img"
      aria-label={agent.displayName}
    />
  );
};
