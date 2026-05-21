import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Share2, CheckCircle, Paperclip, MoreHorizontal, ChevronRight, Sparkles, Tag } from 'lucide-react'
import { useInbox } from '../hooks/useInbox'
import { Skeleton } from '../components/ui/Skeleton'
import { EmailItem } from '../types'

const tabs = [
  { key: 'all', label: 'All' },
  { key: 'needs_human', label: 'Needs Human' },
  { key: 'escalated', label: 'Escalated' },
  { key: 'auto_replied', label: 'Auto-Replied' },
  { key: 'spam', label: 'Spam' },
]

const urgencyBadge = (urgency: string, escalation: boolean) => {
  const base = 'px-2 py-0.5 rounded-full text-[10px] font-bold'
  if (urgency === 'Critical' || escalation) return <span className={`${base} bg-rose-100 text-rose-700 border border-rose-200`}>⚠ Critical Priority</span>
  if (urgency === 'High') return <span className={`${base} bg-orange-100 text-orange-700`}>High</span>
  if (urgency === 'Medium') return <span className={`${base} bg-amber-100 text-amber-700`}>Medium</span>
  return <span className={`${base} bg-slate-100 text-slate-600`}>Low</span>
}

const sentimentColor = (s: string) => {
  if (s === 'Negative') return 'text-rose-500'
  if (s === 'Positive') return 'text-emerald-500'
  return 'text-slate-400'
}

// Mock focused email for the detail panel (matches the design screenshot)
const FOCUS_EMAIL = {
  sender: 'Sarah Jenkins',
  role: 'Global Operations Director • Nexus Corp',
  subject: 'Contract Renewal: Project Catalyst',
  body: `Hi Alex,

We've reviewed the latest proposal for Project Catalyst. While the core technical architecture aligns with our requirements, the projected rollout timeline for Phase 2 is currently a blocker for our Q4 objectives.

We need to see if there's any flexibility in the resource allocation to move the deployment up by at least 3 weeks. If we can't solve this by Friday, we might have to revisit the vendor list for the extension.

Looking forward to your quick thoughts on this.

Best,
Sarah`,
  time: '2 hours ago',
  urgency: 'Critical',
  sentiment: 'Assertive / Urgent',
  detection: 'High-Value Contract',
  tags: ['#ProjectCatalyst', '#ResourceAllocation', '#Negotiation'],
  aiSummary: `Core Issue: Timeline friction for Q4 objectives.

Sarah is pressuring for a 3-week acceleration in Phase 2 deployment. High churn risk if Friday deadline for solutioning is missed. Nexus Corp is a top-tier account ($1.2M ARR).`,
  suggestedActions: [
    { label: 'Fast-Track Solution', text: '"Acknowledge the timeline concern and propose an internal resource shift…"', confidence: 92, highlight: true },
    { label: 'Meeting Request', text: '"Request a 15-minute sync with the Technical Lead to discuss acceleration…"', confidence: 85, highlight: false },
    { label: 'Clarification', text: '"Ask for specific Q4 milestones that are being impacted by the delay…"', confidence: 78, highlight: false },
  ],
}

const SENTIMENT_TREND = [
  { day: 'MON', val: 30 },
  { day: 'TUE', val: 45 },
  { day: 'WED', val: 40 },
  { day: 'THU', val: 60 },
  { day: 'TODAY', val: 75 },
]

export const InboxPage: React.FC = () => {
  const [search, setSearch] = useState('')
  const [active, setActive] = useState('all')
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const { data, isLoading } = useInbox(search)

  const filtered = useMemo(() => {
    if (!data) return []
    switch (active) {
      case 'needs_human': return data.filter((e: EmailItem) => e.needs_human)
      case 'escalated': return data.filter((e: EmailItem) => e.escalation)
      case 'auto_replied': return data.filter((e: EmailItem) => e.auto_replied)
      case 'spam': return data.filter((e: EmailItem) => e.spam)
      default: return data
    }
  }, [data, active])

  const selectedEmail = filtered.find(e => e.id === selectedId) || filtered[0]

  return (
    <div className="h-[calc(100vh-56px)] flex flex-col">
      {/* Breadcrumb + Title */}
      <div className="flex-shrink-0 mb-4">
        <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
          <span>Inbox</span>
          <ChevronRight className="h-3 w-3" />
          <span className="text-slate-600 font-medium">Focus View</span>
        </div>
        <div className="flex items-center justify-between gap-4">
          <h1 className="text-2xl font-bold text-slate-900">
            {selectedEmail ? selectedEmail.subject : 'Select an email'}
          </h1>
          {selectedEmail && (
            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 bg-white text-sm text-slate-700 hover:bg-slate-50 font-medium">
                <Share2 className="h-3.5 w-3.5" />
                Share Intelligence
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700">
                <CheckCircle className="h-3.5 w-3.5" />
                Mark as Resolved
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex items-center gap-2 mb-4 flex-shrink-0">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActive(tab.key)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              active === tab.key
                ? 'bg-indigo-600 text-white'
                : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Main 3-col layout */}
      <div className="flex-1 grid grid-cols-[280px_1fr_300px] gap-4 min-h-0">
        {/* Email list */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-y-auto shadow-sm">
          {isLoading && <div className="p-4"><Skeleton rows={6} /></div>}
          {!isLoading && filtered.length === 0 && (
            <div className="p-8 text-center text-slate-400">
              <p className="font-medium">No emails found</p>
              <p className="text-xs mt-1">Try a different filter</p>
            </div>
          )}
          {filtered.map((email) => (
            <button
              key={email.id}
              onClick={() => setSelectedId(email.id)}
              className={`w-full text-left px-4 py-3 border-b border-slate-100 hover:bg-slate-50 transition-colors ${
                selectedId === email.id || (!selectedId && email === filtered[0]) ? 'bg-indigo-50 border-l-2 border-l-indigo-500' : ''
              }`}
            >
              <div className="flex items-start gap-2 mb-1">
                <div className="h-7 w-7 rounded-full bg-indigo-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-[10px] font-bold text-indigo-700">{email.sender[0]}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-semibold text-slate-900 truncate">{email.sender}</p>
                  <p className="text-[10px] text-slate-500 truncate">{email.subject}</p>
                </div>
              </div>
              <div className="flex items-center justify-between pl-9">
                <span className={`text-[10px] font-semibold ${
                  email.urgency === 'Critical' || email.escalation ? 'text-rose-600' :
                  email.urgency === 'High' ? 'text-orange-500' : 'text-slate-400'
                }`}>
                  {email.escalation ? '⚠ Critical' : email.urgency}
                </span>
                <span className="text-[10px] text-slate-400">{new Date(email.timestamp).toLocaleDateString()}</span>
              </div>
            </button>
          ))}
        </div>

        {/* Email detail */}
        <div className="bg-white rounded-xl border border-slate-200 overflow-y-auto shadow-sm flex flex-col">
          {selectedEmail ? (
            <>
              {/* Email header */}
              <div className="px-6 py-5 border-b border-slate-100">
                <div className="flex items-start gap-3 mb-4">
                  <div className="h-10 w-10 rounded-xl bg-indigo-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-sm font-bold text-indigo-700">{selectedEmail.sender[0]}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2">
                      <p className="text-sm font-bold text-slate-900">{selectedEmail.sender}</p>
                      <div className="flex items-center gap-2">
                        {urgencyBadge(selectedEmail.urgency, selectedEmail.escalation)}
                        <span className="text-xs text-slate-400">{new Date(selectedEmail.timestamp).toLocaleString()}</span>
                      </div>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">Global Operations Director • Nexus Corp</p>
                  </div>
                </div>
              </div>

              {/* Email body */}
              <div className="px-6 py-5 flex-1">
                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">{FOCUS_EMAIL.body}</p>

                {/* Attachment */}
                <div className="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Paperclip className="h-4 w-4 text-slate-400" />
                    <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg">
                      <span className="text-xs text-slate-600 font-medium">📄 proposal_v4.pdf</span>
                    </div>
                  </div>
                  <button className="text-slate-400 hover:text-slate-600">
                    <MoreHorizontal className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Suggested Actions */}
              <div className="px-6 py-4 border-t border-slate-100 bg-slate-50/50">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles className="h-3.5 w-3.5 text-indigo-500" />
                  <p className="text-xs font-bold text-slate-700">Suggested Actions</p>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {FOCUS_EMAIL.suggestedActions.map((action) => (
                    <button
                      key={action.label}
                      className={`text-left p-3 rounded-lg border transition-colors ${
                        action.highlight
                          ? 'border-indigo-200 bg-white'
                          : 'border-slate-200 bg-white hover:border-indigo-200'
                      }`}
                    >
                      <p className={`text-[10px] font-bold mb-1 ${action.highlight ? 'text-indigo-600' : 'text-slate-500'}`}>{action.label}</p>
                      <p className="text-[10px] text-slate-600 leading-relaxed mb-2">{action.text}</p>
                      <p className="text-[10px] text-slate-400 font-semibold">{action.confidence}% Confidence</p>
                    </button>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-slate-400">
              <div className="text-center">
                <p className="font-medium">Select an email</p>
                <p className="text-xs mt-1">Click an email from the list to view it</p>
              </div>
            </div>
          )}
        </div>

        {/* Right panel */}
        <div className="space-y-4 overflow-y-auto">
          {/* AI Summary */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
            <div className="px-4 pt-4 pb-2 border-b border-slate-100 flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-indigo-500" />
              <p className="text-sm font-semibold text-slate-900">AI Summary</p>
            </div>
            <div className="p-4 space-y-3">
              <div className="bg-indigo-50 rounded-lg p-3">
                <span className="text-xs font-bold text-indigo-700">Core Issue: </span>
                <span className="text-xs text-slate-600">Timeline friction for Q4 objectives.</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                Sarah is pressuring for a 3-week acceleration in Phase 2 deployment. High churn risk if Friday deadline for solutioning is missed. Nexus Corp is a top-tier account ($1.2M ARR).
              </p>
              {selectedEmail && (
                <div className="space-y-2 pt-2 border-t border-slate-100">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-500">Sentiment</span>
                    <span className={`text-xs font-semibold ${sentimentColor(selectedEmail.sentiment)}`}>
                      ● {selectedEmail.sentiment}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-500">AI Detection</span>
                    <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">High-Value Contract</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Smart Tags */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
            <div className="px-4 pt-4 pb-2 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Tag className="h-3.5 w-3.5 text-slate-400" />
                <p className="text-sm font-semibold text-slate-900">Smart Tags</p>
              </div>
              <button className="text-xs text-indigo-600 font-semibold hover:text-indigo-700">Edit</button>
            </div>
            <div className="p-4">
              <div className="flex flex-wrap gap-2">
                {FOCUS_EMAIL.tags.map((tag) => (
                  <span key={tag} className="flex items-center gap-1 px-2 py-1 bg-indigo-50 border border-indigo-100 text-indigo-700 rounded-full text-[10px] font-semibold">
                    {tag}
                    <button className="hover:text-indigo-900 ml-0.5">×</button>
                  </span>
                ))}
                <button className="px-2 py-1 border border-dashed border-slate-300 text-slate-400 rounded-full text-[10px] hover:border-indigo-300 hover:text-indigo-500 transition-colors">
                  + Add Tag
                </button>
              </div>
            </div>
          </div>

          {/* Thread Sentiment Trend */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
            <p className="text-sm font-semibold text-slate-900 mb-3">Thread Sentiment Trend</p>
            <div className="flex items-end gap-2 h-20">
              {SENTIMENT_TREND.map((point, i) => (
                <div key={point.day} className="flex-1 flex flex-col items-center gap-1">
                  <div
                    className={`w-full rounded-t transition-all ${i === SENTIMENT_TREND.length - 1 ? 'bg-indigo-600' : 'bg-indigo-200'}`}
                    style={{ height: `${point.val}%` }}
                  />
                  <span className="text-[9px] text-slate-400 font-medium">{point.day}</span>
                </div>
              ))}
            </div>
          </div>

          {/* AI Reasoning (collapsed) */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm">
            <button className="w-full px-4 py-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="h-5 w-5 rounded-full bg-indigo-100 flex items-center justify-center">
                  <span className="text-[10px] font-bold text-indigo-700">AI</span>
                </div>
                <p className="text-sm font-semibold text-slate-900">AI Reasoning</p>
              </div>
              <ChevronRight className="h-4 w-4 text-slate-400 rotate-90" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default InboxPage
