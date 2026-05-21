import React from 'react'
import { EmailItem } from '../types'
import StatusBadge from './ui/StatusBadge'

interface Props {
  email: EmailItem
}

export const EmailContent: React.FC<Props> = ({ email }) => {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-900">{email.subject}</h2>
      </div>
      
      <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
        <div>
          <p className="text-gray-500">From</p>
          <p className="text-gray-900 font-medium">{email.sender}</p>
        </div>
        <div>
          <p className="text-gray-500">Timestamp</p>
          <p className="text-gray-900">{new Date(email.timestamp).toLocaleString()}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-4">
        <div>
          <p className="text-xs text-gray-500 mb-1">Category</p>
          <StatusBadge category={email.category} size="sm" />
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Urgency</p>
          <StatusBadge urgency={email.urgency} escalated={email.escalation} size="sm" />
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Sentiment</p>
          <StatusBadge sentiment={email.sentiment} size="sm" />
        </div>
      </div>

      <div className="border-t border-gray-200 pt-4 mt-4">
        <p className="text-xs text-gray-500 mb-2">Status</p>
        <div className="flex gap-2">
          {email.escalation && <span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">Escalated</span>}
          {email.needs_human && <span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded">Needs Human</span>}
          {email.auto_replied && <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Auto-Replied</span>}
          {email.spam && <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">Spam</span>}
        </div>
      </div>
    </div>
  )
}

export default EmailContent
