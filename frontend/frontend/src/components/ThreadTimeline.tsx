import React from 'react'
import { ThreadMessage } from '../types'
import StatusBadge from './ui/StatusBadge'

interface Props {
  messages: ThreadMessage[]
}

export const ThreadTimeline: React.FC<Props> = ({ messages }) => {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <h3 className="text-lg font-semibold mb-4 text-gray-900">Conversation Timeline</h3>
      
      <div className="space-y-4">
        {messages.map((msg, idx) => (
          <div key={msg.id || idx} className="border-l-2 border-gray-200 pl-4 pb-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="text-sm font-medium text-gray-900">{msg.sender}</p>
                <p className="text-xs text-gray-500">{new Date(msg.timestamp).toLocaleString()}</p>
              </div>
              <div className="flex gap-2">
                {msg.sentiment && <StatusBadge sentiment={msg.sentiment} size="sm" />}
                {msg.type === 'outgoing' && <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded">Sent</span>}
              </div>
            </div>
            <p className="text-sm text-gray-700 whitespace-pre-wrap">{msg.body}</p>
            {msg.escalation_marker && (
              <div className="mt-2 px-2 py-1 bg-red-100 border border-red-200 rounded text-xs text-red-700">
                ⚠️ {msg.escalation_marker}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ThreadTimeline
