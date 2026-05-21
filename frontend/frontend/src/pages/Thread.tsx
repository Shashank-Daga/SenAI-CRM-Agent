import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { ChevronLeft } from 'lucide-react'
import { useThread } from '../hooks/useThread'
import { useDryRunAgent, useExecuteAgent, useClassifyEmail } from '../hooks/useAgentActions'
import { Skeleton } from '../components/ui/Skeleton'
import EmailContent from '../components/EmailContent'
import ThreadTimeline from '../components/ThreadTimeline'
import ContactProfileCard from '../components/ContactProfileCard'
import AgentReasoningPanel from '../components/AgentReasoningPanel'
import RagContextPanel from '../components/RagContextPanel'
import WebIntelligencePanel from '../components/WebIntelligencePanel'

export const ThreadPage: React.FC = () => {
  const { email } = useParams<{ email: string }>()
  const { data: thread, isLoading, isError } = useThread(email || '')
  const dryRunMutation = useDryRunAgent(email || '')
  const executeMutation = useExecuteAgent(email || '')
  const classifyMutation = useClassifyEmail(email || '')

  if (!email) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <p>No thread selected.</p>
      </div>
    )
  }

  if (isLoading) return <div className="p-6"><Skeleton rows={8} /></div>

  if (isError || !thread) {
    return (
      <div className="p-6 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-sm">
        Unable to load thread details. Please try again.
      </div>
    )
  }

  return (
    <div className="space-y-5">
      {/* Back nav */}
      <Link to="/inbox" className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 transition-colors">
        <ChevronLeft className="h-4 w-4" />
        Back to Inbox
      </Link>

      <div className="grid xl:grid-cols-[1fr_300px] gap-5">
        {/* Main thread */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-100">
              <h2 className="text-base font-semibold text-slate-900">Thread workspace</h2>
              <p className="text-xs text-slate-500 mt-0.5">Conversation with {thread.contact.email}</p>
            </div>
            <div className="p-5 space-y-5">
              <EmailContent email={{
                id: thread.messages[0]?.id || '',
                sender: thread.contact.email,
                subject: thread.messages[0]?.body?.slice(0, 80) || 'Conversation',
                category: 'Support',
                urgency: 'High',
                sentiment: thread.messages[0]?.sentiment || 'Neutral',
                timestamp: thread.messages[0]?.timestamp || new Date().toISOString(),
                escalation: false,
                needs_human: false,
                auto_replied: false,
                spam: false,
                thread_id: thread.contact.email,
              }} />
              <ThreadTimeline messages={thread.messages} />

              {/* Action buttons */}
              <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
                <button
                  onClick={() => dryRunMutation.mutate()}
                  disabled={dryRunMutation.isPending}
                  className="px-3 py-2 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 disabled:opacity-50 transition-colors"
                >
                  🔍 Dry-run agent
                </button>
                <button
                  onClick={() => executeMutation.mutate()}
                  disabled={executeMutation.isPending}
                  className="px-3 py-2 text-xs font-semibold rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50 transition-colors"
                >
                  ▶ Execute agent
                </button>
                <button
                  onClick={() => classifyMutation.mutate()}
                  disabled={classifyMutation.isPending}
                  className="px-3 py-2 text-xs font-semibold rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-50 transition-colors"
                >
                  ↻ Reclassify
                </button>
              </div>
            </div>
          </div>

          {/* Summary stats */}
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: 'Open escalations', value: thread.messages.filter((m) => m.escalation_marker).length },
              { label: 'Current sentiment', value: thread.messages[0]?.sentiment || 'Neutral' },
              { label: 'Messages', value: thread.messages.length },
            ].map((stat) => (
              <div key={stat.label} className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
                <p className="text-xs text-slate-500 mb-1">{stat.label}</p>
                <p className="text-xl font-bold text-slate-900">{stat.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right panel */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <ContactProfileCard contact={thread.contact} />
          </div>
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <AgentReasoningPanel steps={thread.agent_reasoning} />
          </div>
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <RagContextPanel contexts={thread.rag_context} />
          </div>
          {thread.contact.web_intelligence && (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <WebIntelligencePanel data={thread.contact.web_intelligence} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ThreadPage
