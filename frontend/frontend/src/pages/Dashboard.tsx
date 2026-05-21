import React, { useMemo, useState } from 'react'
import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip,
  XAxis, YAxis, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend,
} from 'recharts'
import { Sparkles, Calendar, Download, TrendingUp, TrendingDown, AlertTriangle, Activity } from 'lucide-react'
import { useDashboardData } from '../hooks/useDashboardData'
import { Skeleton } from '../components/ui/Skeleton'

const WEEK_DATA = [
  { day: 'MON', volume: 38, ai: 22 },
  { day: 'TUE', volume: 52, ai: 31 },
  { day: 'WED', volume: 78, ai: 48 },
  { day: 'THU', volume: 61, ai: 40 },
  { day: 'FRI', volume: 45, ai: 28 },
  { day: 'SAT', volume: 18, ai: 11 },
  { day: 'SUN', volume: 12, ai: 7 },
]

type ChartTab = 'Volume' | 'Sentiment' | 'Intensity'

export const DashboardPage: React.FC = () => {
  const { data, isLoading, isError } = useDashboardData()
  const [chartTab, setChartTab] = useState<ChartTab>('Volume')

  const metricCards = useMemo(() => [
    {
      label: 'TOTAL EMAILS',
      value: data ? data.inboxVolume.total.toLocaleString() : '2,842',
      trend: '+12%',
      trendDir: 'up',
      sub: 'vs last 24 hours',
      icon: '📧',
    },
    {
      label: 'OPEN THREADS',
      value: data ? data.inboxVolume.needsHuman.toString() : '43',
      trend: '+5',
      trendDir: 'up',
      sub: '8 priority tagged',
      icon: '💬',
    },
    {
      label: 'RESOLVED',
      value: data ? `${data.escalationMetrics.resolved}%` : '1,580',
      trend: '98.2%',
      trendDir: 'up',
      sub: 'efficiency score',
      icon: '✅',
    },
    {
      label: 'AVG RESPONSE',
      value: '4.2m',
      trend: '-1.5m',
      trendDir: 'down-good',
      sub: 'AI auto-suggest active',
      icon: '⏱',
    },
  ], [data])

  return (
    <div className="space-y-5">
      {/* Page header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs text-slate-500 font-medium mb-0.5">Intelligence Dashboard</p>
          <p className="text-sm text-slate-600">Welcome back. AI models have processed 1,240 events in the last hour.</p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50 transition-colors font-medium">
            <Calendar className="h-3.5 w-3.5" />
            Today, Oct 24
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700 transition-colors">
            <Download className="h-3.5 w-3.5" />
            Export Report
          </button>
        </div>
      </div>

      {/* Metric cards */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        {metricCards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm">
            <div className="flex items-start justify-between mb-3">
              <p className="text-[10px] font-bold tracking-widest text-slate-500 uppercase">{card.label}</p>
              <span className="text-lg">{card.icon}</span>
            </div>
            <p className="text-2xl font-bold text-slate-900 mb-1">{card.value}</p>
            <div className="flex items-center gap-1.5">
              <span className={`text-xs font-semibold ${
                card.trendDir === 'up' ? 'text-emerald-600' :
                card.trendDir === 'down-good' ? 'text-rose-600' : 'text-rose-600'
              }`}>
                {card.trend}
              </span>
              <span className="text-xs text-slate-400">{card.sub}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Main content grid */}
      <div className="grid xl:grid-cols-[1fr_300px] gap-5">
        {/* Left: AI Insights + Chart */}
        <div className="space-y-5">
          {/* AI Insights Summary */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 pt-4 pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-indigo-500" />
                <span className="text-sm font-semibold text-slate-900">AI Insights Summary</span>
              </div>
            </div>
            <div className="p-5 space-y-4">
              {/* Strategic Focus */}
              <div className="bg-slate-50 rounded-lg p-4 border border-slate-100">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-sm font-semibold text-slate-900">Strategic Focus</span>
                  <span className="px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 text-[10px] font-bold tracking-wide uppercase">High Confidence</span>
                </div>
                <p className="text-sm text-slate-600 leading-relaxed">
                  Our analysis shows a 15% uptick in queries regarding the "Pro Tier" feature set. This suggests a strong conversion window for users in the basic plan. I recommend activating the 'Enterprise Upgrade' nudge for the top 50 active accounts identified in the segment list.
                </p>
              </div>

              {/* Two column insights */}
              <div className="grid grid-cols-2 gap-3">
                <div className="flex gap-3 p-3 rounded-lg border border-emerald-100 bg-emerald-50">
                  <div className="flex-shrink-0 h-8 w-8 rounded-full bg-emerald-100 flex items-center justify-center">
                    <TrendingUp className="h-4 w-4 text-emerald-600" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-900 mb-0.5">Sentiment Peak</p>
                    <p className="text-xs text-slate-500 leading-relaxed">Overall customer sentiment hit a 90-day high today following the v2.4 patch release.</p>
                  </div>
                </div>
                <div className="flex gap-3 p-3 rounded-lg border border-amber-100 bg-amber-50">
                  <div className="flex-shrink-0 h-8 w-8 rounded-full bg-amber-100 flex items-center justify-center">
                    <AlertTriangle className="h-4 w-4 text-amber-600" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-900 mb-0.5">Bottleneck Warning</p>
                    <p className="text-xs text-slate-500 leading-relaxed">Response latency is increasing for 'Refund' queries. System suggests 3 new macro templates.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Communication Trends Chart */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
            <div className="px-5 pt-4 pb-3 border-b border-slate-100 flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-900">Communication Trends</p>
                <p className="text-xs text-slate-500 mt-0.5">Real-time volume analysis across all channels</p>
              </div>
              <div className="flex items-center gap-1 bg-slate-50 rounded-lg p-1">
                {(['Volume', 'Sentiment', 'Intensity'] as ChartTab[]).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setChartTab(tab)}
                    className={`px-3 py-1 rounded-md text-xs font-semibold transition-colors ${
                      chartTab === tab
                        ? 'bg-white text-slate-900 shadow-sm'
                        : 'text-slate-500 hover:text-slate-700'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>
            <div className="p-5">
              <div className="h-[220px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={WEEK_DATA} margin={{ top: 5, right: 5, left: -20, bottom: 0 }} barGap={4}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                    <XAxis
                      dataKey="day"
                      tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 500 }}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <Tooltip
                      contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 12 }}
                      cursor={{ fill: '#f8fafc' }}
                    />
                    <Bar dataKey="volume" name="Inbound" fill="#c7d2fe" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="ai" name="AI-Response" fill="#6366f1" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="flex items-center gap-4 mt-2">
                <div className="flex items-center gap-1.5">
                  <div className="h-2.5 w-2.5 rounded-full bg-indigo-200" />
                  <span className="text-xs text-slate-500">Inbound</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <div className="h-2.5 w-2.5 rounded-full bg-indigo-600" />
                  <span className="text-xs text-slate-500">AI-Response</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Risk Radar + AI Recommendation */}
        <div className="space-y-4">
          {/* Risk Radar */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
            <div className="px-4 pt-4 pb-2 flex items-center justify-between border-b border-slate-100">
              <p className="text-sm font-semibold text-slate-900">Risk Radar</p>
              <button className="text-slate-400 hover:text-slate-600">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                </svg>
              </button>
            </div>
            <div className="p-4 space-y-4">
              {/* High Churn Risk */}
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-lg bg-rose-50 border border-rose-100 flex items-center justify-center flex-shrink-0">
                  <TrendingDown className="h-4 w-4 text-rose-500" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-xs font-semibold text-slate-700">High Churn Risk</p>
                    <span className="text-xs font-bold text-rose-600">
                      {data ? `${Math.round((data.inboxVolume.escalated / Math.max(data.inboxVolume.total, 1)) * 100)}%` : '8.2%'}
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-rose-500 rounded-full" style={{ width: data ? `${Math.round((data.inboxVolume.escalated / Math.max(data.inboxVolume.total, 1)) * 100)}%` : '8.2%' }} />
                  </div>
                </div>
              </div>

              {/* Response Rate */}
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center justify-center flex-shrink-0">
                  <Activity className="h-4 w-4 text-indigo-500" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-xs font-semibold text-slate-700">Response Rate</p>
                    <span className="text-xs font-bold text-indigo-600">94.1%</span>
                  </div>
                  <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-500 rounded-full" style={{ width: '94.1%' }} />
                  </div>
                </div>
              </div>

              {/* At-risk accounts */}
              {data && data.atRiskAccounts.length > 0 && (
                <div className="pt-2 border-t border-slate-100">
                  <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">At-Risk Accounts</p>
                  {data.atRiskAccounts.slice(0, 3).map((acc) => (
                    <div key={acc.company} className="flex items-center justify-between py-1.5">
                      <p className="text-xs font-medium text-slate-700 truncate">{acc.company}</p>
                      <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                        acc.churnRisk === 'High' ? 'bg-rose-100 text-rose-700' :
                        acc.churnRisk === 'Medium' ? 'bg-amber-100 text-amber-700' :
                        'bg-emerald-100 text-emerald-700'
                      }`}>{acc.churnRisk}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* AI Recommendation */}
          <div className="bg-indigo-600 rounded-xl p-4 text-white relative overflow-hidden">
            <div className="absolute inset-0 opacity-10">
              <svg viewBox="0 0 200 200" className="w-full h-full">
                <circle cx="160" cy="40" r="80" fill="white" />
                <circle cx="40" cy="160" r="60" fill="white" />
              </svg>
            </div>
            <div className="relative">
              <p className="text-[10px] font-bold tracking-widest uppercase text-indigo-200 mb-2">AI RECOMMENDATION</p>
              <p className="text-sm font-semibold mb-3">Generate Weekly Executive Summary?</p>
              <button className="w-full flex items-center justify-center gap-2 bg-white text-indigo-700 rounded-lg py-2 text-xs font-bold hover:bg-indigo-50 transition-colors">
                <Sparkles className="h-3.5 w-3.5" />
                Generate Now
              </button>
            </div>
          </div>

          {/* Team Performance */}
          {data && (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">Team Performance</p>
              <div className="space-y-3">
                {data.teamPerformance.map((team) => (
                  <div key={team.team}>
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-xs font-semibold text-slate-700">{team.team}</p>
                      <span className="text-xs text-slate-500">{team.resolutionRate}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-indigo-500 rounded-full transition-all duration-700"
                        style={{ width: `${team.resolutionRate}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {isLoading && <Skeleton rows={4} />}
        </div>
      </div>
    </div>
  )
}

export default DashboardPage
