/**
 * CoSight Sidebar — agent roster with last discussion preview per specialist.
 */
import React, { useState } from 'react';
import { PanelLeftClose, PanelLeft } from 'lucide-react';
import { SidebarAgentRoster } from './SidebarAgentRoster';
import './CoSightSidebar.css';

export const CoSightSidebar: React.FC = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside
      className={`cs-sidebar ${isCollapsed ? 'collapsed' : ''}`}
      onClick={(e) => {
        if (!isCollapsed) return;
        if ((e.target as HTMLElement).closest('button, a, [role="button"]')) return;
        setIsCollapsed(false);
      }}
    >
      <div className="sidebar-header">
        <div className="sidebar-logo">
          {!isCollapsed && <span className="sidebar-logo-wordmark">Cosight</span>}
        </div>
        <button
          className="sidebar-collapse-btn"
          onClick={() => setIsCollapsed(v => !v)}
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <PanelLeft size={18} /> : <PanelLeftClose size={18} />}
        </button>
      </div>

      <SidebarAgentRoster collapsed={isCollapsed} />

      <div
        className="sidebar-resize-handle"
        onClick={() => setIsCollapsed(v => !v)}
        title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      />
    </aside>
  );
};
