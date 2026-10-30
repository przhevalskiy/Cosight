import React, { createContext, useContext } from 'react';
import { agentIdForChannel } from '../../agents/registry';
import type { AgentId } from '../../agents/registry';

const DashboardAgentContext = createContext<AgentId>('overview');

export function DashboardAgentProvider({
  channel,
  children,
}: {
  channel: string;
  children: React.ReactNode;
}) {
  return (
    <DashboardAgentContext.Provider value={agentIdForChannel(channel)}>
      {children}
    </DashboardAgentContext.Provider>
  );
}

export function useDashboardAgentId(): AgentId {
  return useContext(DashboardAgentContext);
}
