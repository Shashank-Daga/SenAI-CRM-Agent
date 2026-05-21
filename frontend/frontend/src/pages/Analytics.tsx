import React, { useState } from 'react'
import {
  Bar, BarChart, CartesianGrid, ResponsiveContainer,
  Tooltip, XAxis, YAxis,
} from 'recharts'
import { Download, Filter, MoreHorizontal, Star, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { useAnalytics } from '../hooks/useAnalytics'
import { Skeleton } from '../components/ui/Skeleton'

type Period = 'Last 30 Days' | 'Quarterly'

const EMAIL_ACTIVITY = [
  { date: '01 May', inbound: 120, ai: 80 },
  { date: '08 May', inbound: 180, ai: 110 },
  { date: '15 May', inbound: 150, ai: 130 },
  { date: '22 May', inbound: 240, ai: 170 },
  { date: '29 May', inbound: 200, ai: 180 },
]

// Sentiment heatmap - 8 cols x 8 rows
const HEATMAP = Array.from({ length: 64 }, (_, i) => {
  const val = Math.random()
  return val > 0.7 ? 'high' : val > 0.35 ? 'mid' : 'low'
})

const TEAM_MEMBERS = [
  { initials: 'SC', name: 'Sarah Chen', role: 'Senior Analyst', processed: '1,420 items', satisfaction: 4.9, aiUsage: 92, status: 'Peak Performer', statusColor: 'bg-emerald-100 text-emerald-700' },
  { initials: 'MJ', name: 'Marcus Jordan', role: 'Support Lead', processed: '2,840 items', satisfaction: 4.7, aiUsage: 88, status: 'High Volume', statusColor: 'bg-indigo-100 text-indigo-700' },
  { initials: 'EL', name: 'Elena Lopez', role: 'UX Researcher', processed: '850 items', satisfaction: 5.0, aiUsage: 64, status: 'Quality Focus', statusColor: 'bg-amber-100 text-amber-700' },
]

const avatarColors = ['bg-slate-200 text-slate-700', 'bg-blue-200 text-blue-700', 'bg-orange-200 text-orange-700']

export const AnalyticsPage: React.FC = () => {
  const { data, isLoading, isError } = useAnalytics()
  const [period, setPeriod] = useState<Period>('Last 30 Days')

  if (isLoading) return <div className="p-8"><Skeleton rows={12} /></div>

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Advanced Analytics</h1>
          <p className="text-sm text-slate-500 mt-0.5">Real-time performance metrics and AI-driven insights across all departments.</p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <div className="flex items-center bg-white border border-slate-200 rounded-lg overflow-hidden">
            {(['Last 30 Days', 'Quarterly'] as Period[]).map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`px-3 py-1.5 text-xs font-semibold transition-colors ${
                  period === p ? 'bg-indigo-600 text-white' : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                {p}
              </button>
            ))}
          </div>
          <button className="flex items-center gap-1.5 px-3 py-1.5 border border-slate-200 bg-white rounded-lg text-sm text-slate-600 hover:bg-slate-50 font-medium">
            <Filter className="h-3.5 w-3.5" />
            Teams
          </button>
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700">
            <Download className="h-3.5 w-3.5" />
            Export Report
          </button>
        </div>
      </div>

      {/* AI Executive Summary banner */}
      <div className="bg-indigo-600 rounded-xl p-5 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <svg viewBox="0 0 400 160" className="w-full h-full">
            <circle cx="350" cy="20" r="120" fill="white" />
            <circle cx="50" cy="140" r="80" fill="white" />
          </svg>
        </div>
        <div className="relative grid xl:grid-cols-[1fr_auto] gap-4 items-start">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-indigo-200 font-bold text-[10px] tracking-widest">✦_ΨRK AI EXECUTIVE SUMMARY</span>
            </div>
            <h2 className="text-xl font-bold mb-2">Productivity increased by 14.2% this month</h2>
            <p className="text-sm text-indigo-100 max-w-lg">
              Response times are at an all-time low. AI-assisted drafting has reduced manual workload by approximately 22 hours per team member.
            </p>
            <div className="flex items-center gap-2 mt-4">
              <button className="px-3 py-1.5 bg-white text-indigo-700 text-xs font-bold rounded-lg hover:bg-indigo-50 transition-colors">View Details</button>
              <button className="px-3 py-1.5 border border-indigo-400 text-white text-xs font-bold rounded-lg hover:bg-indigo-700 transition-colors">Dismiss</button>
            </div>
          </div>
          <div className="flex gap-4">
            {/* Response Accuracy */}
            <div className="bg-white/10 rounded-xl p-4 min-w-[150px]">
              <p className="text-xs text-indigo-200 font-medium mb-1">Response Accuracy</p>
              <p className="text-3xl font-bold">98.4%</p>
              <div className="flex items-center gap-1 mt-1">
                <TrendingUp className="h-3 w-3 text-emerald-300" />
                <span className="text-xs text-emerald-300 font-semibold">+2.1%</span>
              </div>
              <div className="mt-2 h-1 bg-white/20 rounded-full">
                <div className="h-full bg-white rounded-full" style={{ width: '98.4%' }} />
              </div>
            </div>
            {/* Total Interactions */}
            <div className="bg-white/10 rounded-xl p-4 min-w-[150px]">
              <p className="text-xs text-indigo-200 font-medium mb-1">Total Interactions</p>
              <p className="text-3xl font-bold">1.2M</p>
              <div className="flex items-center gap-1 mt-1">
                <TrendingUp className="h-3 w-3 text-emerald-300" />
                <span className="text-xs text-emerald-300 font-semibold">+12%</span>
              </div>
              <div className="mt-2 h-1 bg-white/20 rounded-full">
                <div className="h-full bg-white rounded-full" style={{ width: '72%' }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts row */}
      <div className="grid xl:grid-cols-[1fr_340px] gap-5">
        {/* Email Activity & Response Trends */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="px-5 pt-5 pb-3 border-b border-slate-100 flex items-center justify-between">
            <p className="text-sm font-semibold text-slate-900">Email Activity & Response Trends</p>
            <div className="flex items-center gap-3">
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
          <div className="p-5">
            <div className="h-[260px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={data?.sentimentTrend?.length ? data.sentimentTrend : EMAIL_ACTIVITY}
                  margin={{ top: 5, right: 5, left: -20, bottom: 0 }}
                  barGap={4}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis
                    dataKey={data?.sentimentTrend?.length ? 'timestamp' : 'date'}
                    tick={{ fill: '#94a3b8', fontSize: 11 }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip
                    contentStyle={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 12 }}
                    cursor={{ fill: '#f8fafc' }}
                  />
                  {data?.sentimentTrend?.length ? (
                    <>
                      <Bar dataKey="positive" name="Positive" fill="#c7d2fe" radius={[3, 3, 0, 0]} />
                      <Bar dataKey="negative" name="Negative" fill="#6366f1" radius={[3, 3, 0, 0]} />
                    </>
                  ) : (
                    <>
                      <Bar dataKey="inbound" name="Inbound" fill="#c7d2fe" radius={[3, 3, 0, 0]} />
                      <Bar dataKey="ai" name="AI-Response" fill="#6366f1" radius={[3, 3, 0, 0]} />
                    </>
                  )}
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Sentiment Analysis heatmap */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="px-5 pt-5 pb-3 border-b border-slate-100">
            <p className="text-sm font-semibold text-slate-900">Sentiment Analysis</p>
          </div>
          <div className="p-5">
            {/* Heatmap grid */}
            <div className="grid gap-1 mb-4" style={{ gridTemplateColumns: 'repeat(8, 1fr)' }}>
              {HEATMAP.map((level, i) => (
                <div
                  key={i}
                  className={`h-7 rounded ${
                    level === 'high' ? 'bg-indigo-600' :
                    level === 'mid' ? 'bg-indigo-200' :
                    'bg-slate-100'
                  }`}
                />
              ))}
            </div>
            {/* Overall Vibe */}
            <div className="space-y-2 pt-3 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-500">Overall Vibe</span>
                <span className="px-2 py-0.5 bg-emerald-100 text-emerald-700 text-[10px] font-bold rounded-full">Highly Positive</span>
              </div>
              <p className="text-xs text-slate-500 italic leading-relaxed">
                "Most customers are expressing satisfaction with the speed of ticket resolution this week."
              </p>
            </div>
            {/* Key metrics */}
            {data && (
              <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-100">
                <div className="text-center">
                  <p className="text-lg font-bold text-slate-900">{data.escalationMetrics?.escalated ?? 0}%</p>
                  <p className="text-[10px] text-slate-400">Escalated</p>
                </div>
                <div className="text-center">
                  <p className="text-lg font-bold text-slate-900">{data.automationMetrics?.autoReplyRate ?? 0}%</p>
                  <p className="text-[10px] text-slate-400">Auto-Reply Rate</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Team Performance Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
        <div className="px-5 pt-5 pb-3 border-b border-slate-100 flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-900">Team Performance Comparison</p>
          <button className="text-slate-400 hover:text-slate-600">
            <MoreHorizontal className="h-4 w-4" />
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-100">
                {['TEAM MEMBER', 'PROCESSED', 'SATISFACTION', 'AI USAGE', 'STATUS'].map(col => (
                  <th key={col} className="px-5 py-3 text-left text-[10px] font-bold text-slate-400 tracking-wider uppercase">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {TEAM_MEMBERS.map((member, i) => (
                <tr key={member.name} className={`border-b border-slate-50 hover:bg-slate-50/50 transition-colors ${i === 1 ? 'bg-indigo-50/30' : ''}`}>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 ${avatarColors[i]}`}>
                        {member.initials}
                      </div>
                      <div>
                        <p className="text-sm font-semibold text-slate-900">{member.name}</p>
                        <p className="text-xs text-slate-400">{member.role}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <span className="text-sm text-slate-700 font-medium">{member.processed}</span>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-1">
                      <Star className="h-3.5 w-3.5 text-amber-400 fill-amber-400" />
                      <span className="text-sm font-semibold text-slate-900">{member.satisfaction}</span>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden min-w-[60px]">
                        <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${member.aiUsage}%` }} />
                      </div>
                      <span className="text-sm text-slate-600 font-medium">{member.aiUsage}%</span>
                    </div>
                  </td>
                  <td className="px-5 py-4">
                    <span className={`px-2 py-1 rounded-full text-[10px] font-bold ${member.statusColor}`}>
                      {member.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* At-risk accounts */}
      {data?.atRiskAccounts && data.atRiskAccounts.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
          <div className="px-5 pt-5 pb-3 border-b border-slate-100">
            <p className="text-sm font-semibold text-slate-900">At-Risk Accounts</p>
            <p className="text-xs text-slate-500 mt-0.5">Churn risk and negative sentiment exposure</p>
          </div>
          <div className="p-5 grid md:grid-cols-3 gap-4">
            {data.atRiskAccounts.map((account) => (
              <div key={account.company} className="border border-slate-200 rounded-xl p-4">
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div>
                    <p className="text-sm font-semibold text-slate-900">{account.company}</p>
                    <p className="text-xs text-slate-400 mt-0.5">Churn Risk</p>
                    <p className="text-base font-bold text-slate-900 mt-1">{account.churnRisk}</p>
                  </div>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                    account.churnRisk === 'High' ? 'bg-rose-100 text-rose-700' :
                    account.churnRisk === 'Medium' ? 'bg-amber-100 text-amber-700' :
                    'bg-emerald-100 text-emerald-700'
                  }`}>{account.churnRisk}</span>
                </div>
                <div className="text-xs text-slate-600 space-y-1">
                  <p>Unresolved escalations: <strong>{account.unresolvedEscalations}</strong></p>
                  <p>Negative trend: <strong>{account.negativeSentimentTrend}%</strong></p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default AnalyticsPage
