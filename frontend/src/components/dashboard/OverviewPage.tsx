import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMetricsStore } from '../../stores/metricsStore';
import { TrendChart } from './TrendChart';
import { DashboardPageShell } from './DashboardPageShell';
import { DateRangePicker } from './DateRangePicker';
import { LoadingSkeleton, ErrorState } from './ChannelStatus';
import { OverviewChannelStatus } from './OverviewChannelStatus';
import { ChibiAvatars } from '../shared/ChibiAvatars';
import { OVERVIEW_PROMPTS } from '../shared/dashboardPrompts';
import type { ScopedContext, NormalizedMetric, ChannelMetrics } from '../../types';
import './Page.css';
import './OverviewPage.css';

export const OverviewPage: React.FC = () => {
  const { dateRange, setDateRange, overview, loading, errors, fetchOverview } = useMetricsStore();
  const navigate = useNavigate();

  useEffect(() => { fetchOverview(); }, [dateRange]);

  const handleDrillIn = (ctx: ScopedContext) => {
    navigate('/chat', { state: { scopedContext: ctx, dateRange } });
  };

  const channelMetrics: ChannelMetrics[] = [
    overview?.web,
    overview?.search,
    overview?.email,
    overview?.social,
  ].filter((c): c is ChannelMetrics => !!c);
  const allSummaryKpis = channelMetrics.flatMap(c =>
    c!.summary.filter((m: NormalizedMetric) => !m.date_bucket && !m.dimension)
  );

  const isLoading = loading['overview'];
  const error = errors['overview'];

  return (
    <DashboardPageShell
      channel="overview"
      dateRange={dateRange}
      metricsReady={!isLoading && !!overview}
      summaryKpis={allSummaryKpis.slice(0, 8)}
      header={(
        <>
          <div className="overview-header">
            <ChibiAvatars size={48} />
            <div className="overview-header__main">
              <div className="overview-header__top">
                <h1>Overview</h1>
                <OverviewChannelStatus channels={channelMetrics} />
                <DateRangePicker value={dateRange} onChange={setDateRange} />
              </div>
            </div>
          </div>
          {isLoading && <LoadingSkeleton rows={2} />}
          {!isLoading && error && <ErrorState message={error} />}
        </>
      )}
      quickPrompts={OVERVIEW_PROMPTS}
      inputPlaceholder="Ask CoSight anything about your marketing data…"
      onDrillIn={handleDrillIn}
    >
      {overview?.web && overview?.search && (
        <TrendChart
          title="Web Sessions vs Search Clicks"
          timeseries={[...(overview.web.timeseries || []), ...(overview.search.timeseries || [])]}
          series={[
            { key: 'sessions', label: 'Sessions', color: '#001b5e' },
            { key: 'clicks', label: 'Search Clicks', color: '#5b9bd5', yAxisId: 'right' },
          ]}
        />
      )}
    </DashboardPageShell>
  );
};
