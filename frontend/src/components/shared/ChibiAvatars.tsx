/**
 * Row of channel agents from the fuzzy sprite sheet (overview hero).
 */
import React from 'react';
import { getAgent } from '../../agents/registry';
import { AgentDotAvatar } from './AgentDotAvatar';
import './ChibiAvatars.css';

import { OVERVIEW_ROSTER_AGENTS } from '../../agents/registry';

export function ChibiAvatars({
  count,
  size = 52,
}: { count?: number; size?: number } = {}) {
  const list = count != null ? OVERVIEW_ROSTER_AGENTS.slice(0, count) : OVERVIEW_ROSTER_AGENTS;
  return (
    <div className="chibi-avatars">
      {list.map((id, i) => (
        <div
          key={id}
          className="chibi-avatar-wrap"
          title={getAgent(id).shortLabel}
          style={{ '--i': i } as React.CSSProperties}
        >
          <AgentDotAvatar agentId={id} size={size} />
        </div>
      ))}
    </div>
  );
}
