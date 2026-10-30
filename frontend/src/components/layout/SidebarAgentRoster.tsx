import React, { useEffect, useState } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import { MessageSquarePlus } from 'lucide-react';
import { AgentDotAvatar } from '../shared/AgentDotAvatar';
import { useChatStore } from '../../stores/chatStore';
import { getAgent, type AgentId } from '../../agents/registry';
import { fetchAgentActivity, type AgentActivityItem } from '../../services/api';
import './SidebarAgentRoster.css';

const PLACEHOLDER = 'No recent discussion yet';

export const SIDEBAR_AGENTS: {
  path: string;
  agentId: AgentId;
  end?: boolean;
}[] = [
  { path: '/', agentId: 'overview', end: true },
  { path: '/web', agentId: 'web' },
  { path: '/seo', agentId: 'search' },
  { path: '/email', agentId: 'email' },
  { path: '/social', agentId: 'social' },
  { path: '/reports', agentId: 'reports' },
];

interface Props {
  collapsed: boolean;
}

export const SidebarAgentRoster: React.FC<Props> = ({ collapsed }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const setActiveDiscussion = useChatStore(s => s.setActiveDiscussion);
  const [activity, setActivity] = useState<Record<string, AgentActivityItem>>({});

  useEffect(() => {
    let cancelled = false;
    fetchAgentActivity()
      .then(rows => {
        if (cancelled) return;
        const map: Record<string, AgentActivityItem> = {};
        for (const row of rows) map[row.agent_id] = row;
        setActivity(map);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [location.pathname]);

  const openNewChat = (e: React.MouseEvent) => {
    e.preventDefault();
    setActiveDiscussion(null);
    navigate('/chat', {
      state: { freshChat: true },
      replace: location.pathname === '/chat',
    });
  };

  return (
    <nav className="sidebar-agent-roster" aria-label="Agents">
      <button
        type="button"
        className={`sidebar-new-chat-row${location.pathname === '/chat' ? ' sidebar-new-chat-row--active' : ''}`}
        onClick={openNewChat}
        title="New chat"
      >
        <span className="sidebar-new-chat-row__icon" aria-hidden>
          <MessageSquarePlus size={collapsed ? 18 : 20} strokeWidth={2} />
        </span>
        {!collapsed && <span className="sidebar-new-chat-row__label">New chat</span>}
      </button>
      <ul className="sidebar-agent-roster__list">
        {SIDEBAR_AGENTS.map(({ path, agentId, end }) => {
          const agent = getAgent(agentId);
          const item = activity[agentId];
          const snippet = item?.snippet?.trim() || PLACEHOLDER;

          return (
            <li key={path}>
              <NavLink
                to={path}
                end={end}
                className={({ isActive }) =>
                  `sidebar-agent-row${isActive ? ' sidebar-agent-row--active' : ''}`
                }
                title={collapsed ? agent.shortLabel : undefined}
              >
                <AgentDotAvatar agentId={agentId} size={collapsed ? 28 : 36} />
                {!collapsed && (
                  <div className="sidebar-agent-row__text">
                    <div className="sidebar-agent-row__title">{agent.shortLabel}</div>
                    <div className="sidebar-agent-row__snippet">{snippet}</div>
                  </div>
                )}
              </NavLink>
            </li>
          );
        })}
      </ul>
    </nav>
  );
};
