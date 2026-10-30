import React from 'react';
import { AgentDotAvatar } from '../shared/AgentDotAvatar';
import { useDashboardAgentId } from './DashboardAgentContext';

interface Props {
  title: string;
  children?: React.ReactNode;
}

/** Page header row with the channel’s specialist avatar */
export const DashboardPageTitle: React.FC<Props> = ({ title, children }) => {
  const agentId = useDashboardAgentId();
  return (
    <div className="cs-page__header">
      <AgentDotAvatar agentId={agentId} size={28} className="cs-page__agent" />
      <h1>{title}</h1>
      {children}
    </div>
  );
};
