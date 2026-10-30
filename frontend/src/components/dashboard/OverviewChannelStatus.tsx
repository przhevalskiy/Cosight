import React from 'react';
import type { ChannelMetrics } from '../../types';
import { StaleBadge } from './ChannelStatus';
import './OverviewChannelStatus.css';

interface Props {
  channels: ChannelMetrics[];
}

/** One clear notice when every connector fails; per-channel badges only when mixed. */
export const OverviewChannelStatus: React.FC<Props> = ({ channels }) => {
  const failed = channels.filter(c => c.status !== 'ok');
  if (failed.length === 0) return null;

  if (failed.length === channels.length) {
    return (
      <div className="overview-connectors-notice" role="status">
        <strong>Live metrics need connector credentials.</strong>
        <span>
          Copy <code>backend/.env.example</code> to <code>backend/.env</code>, set Google
          (GA4 + Search Console), Emma, and Sprout keys, then restart the API server.
        </span>
      </div>
    );
  }

  return (
    <div className="cs-page__badges">
      {failed.map(c => (
        <StaleBadge
          key={c.channel}
          status={c.status}
          channel={c.channel}
          message={c.error_message}
        />
      ))}
    </div>
  );
};
