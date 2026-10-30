/**
 * CoSight specialist agents — mirrors backend app.core.agents (IDs, labels, colors).
 */
export type AgentId =
  | 'overview'
  | 'web'
  | 'search'
  | 'email'
  | 'social'
  | 'reports'
  | 'chat';

export interface AgentMeta {
  id: AgentId;
  displayName: string;
  shortLabel: string;
  /** Shown after · on overview roster (e.g. "SEO / Search Console") */
  role: string;
  domain: string;
  /** Dot cluster + ring accent */
  accent: string;
  /** Soft fill behind the three dots */
  surface: string;
}

export const AGENTS: Record<AgentId, AgentMeta> = {
  overview: {
    id: 'overview',
    displayName: 'Overview Analyst',
    shortLabel: 'Overview',
    role: 'Cross-channel performance',
    domain: 'Cross-channel marketing performance',
    accent: '#4f46e5',
    surface: '#eef2ff',
  },
  web: {
    id: 'web',
    displayName: 'Web Analyst',
    shortLabel: 'Web',
    role: 'GA4 & site analytics',
    domain: 'Google Analytics 4',
    accent: '#c2410c',
    surface: '#fff7ed',
  },
  search: {
    id: 'search',
    displayName: 'Search Analyst',
    shortLabel: 'Search',
    role: 'Search Console & SEO',
    domain: 'Google Search Console',
    accent: '#1d4ed8',
    surface: '#eff6ff',
  },
  email: {
    id: 'email',
    displayName: 'Email Analyst',
    shortLabel: 'Email',
    role: 'Emma campaigns',
    domain: 'Emma email marketing',
    accent: '#7e22ce',
    surface: '#faf5ff',
  },
  social: {
    id: 'social',
    displayName: 'Social Analyst',
    shortLabel: 'Social',
    role: 'Sprout & social channels',
    domain: 'Sprout Social',
    accent: '#15803d',
    surface: '#f0fdf4',
  },
  reports: {
    id: 'reports',
    displayName: 'Reports Agent',
    shortLabel: 'Reports',
    role: 'Exports & summaries',
    domain: 'Report artifacts & exports',
    accent: '#334155',
    surface: '#f1f5f9',
  },
  chat: {
    id: 'chat',
    displayName: 'CoSight Orchestrator',
    shortLabel: 'Chat',
    role: 'Multi-channel Q&A',
    domain: 'Multi-channel Q&A',
    accent: '#0f766e',
    surface: '#f0fdfa',
  },
};

export function getAgent(id: string): AgentMeta {
  return AGENTS[id as AgentId] ?? AGENTS.chat;
}

/** Dashboard channel slug → agent id */
export function agentIdForChannel(channel: string): AgentId {
  if (channel === 'seo') return 'search';
  if (channel in AGENTS) return channel as AgentId;
  return 'overview';
}

export const OVERVIEW_ROSTER_AGENTS = ['web', 'search', 'email', 'social', 'reports'] as const;

export function pathForAgent(agentId: string): string {
  const paths: Record<string, string> = {
    web: '/web',
    search: '/seo',
    email: '/email',
    social: '/social',
    reports: '/reports',
  };
  return paths[agentId] ?? '/';
}
