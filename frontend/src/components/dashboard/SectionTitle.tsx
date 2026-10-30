import React from 'react';
import { AgentDotAvatar } from '../shared/AgentDotAvatar';
import { useDashboardAgentId } from './DashboardAgentContext';

interface Props {
  title: string;
  className?: string;
}

/** In-content section tab (chart, table, breakdown) with matching agent */
export const SectionTitle: React.FC<Props> = ({ title, className = '' }) => {
  const agentId = useDashboardAgentId();
  return (
    <div className={`cs-section-tab ${className}`.trim()}>
      <AgentDotAvatar agentId={agentId} size={20} />
      <span>{title}</span>
    </div>
  );
};
