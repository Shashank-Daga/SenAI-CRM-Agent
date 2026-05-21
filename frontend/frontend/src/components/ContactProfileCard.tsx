import React from 'react'
import { ContactProfile } from '../types'
import PanelCard from './ui/PanelCard'

interface Props {
  contact: ContactProfile
}

export const ContactProfileCard: React.FC<Props> = ({ contact }) => {
  return (
    <PanelCard title="Contact Profile">
      <div className="space-y-3">
        <div>
          <p className="text-xs text-gray-500">Email</p>
          <p className="text-sm font-medium text-gray-900">{contact.email}</p>
        </div>
        
        <div>
          <p className="text-xs text-gray-500">Name</p>
          <p className="text-sm text-gray-900">{contact.name || '—'}</p>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-gray-200">
          <div>
            <p className="text-xs text-gray-500">VIP Status</p>
            <p className="text-sm font-medium">{contact.vip_status ? '⭐ VIP' : 'Standard'}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Account Value</p>
            <p className="text-sm font-medium text-green-700">{contact.account_value}</p>
          </div>
        </div>

        <div>
          <p className="text-xs text-gray-500 mb-1">Churn Risk</p>
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            contact.churn_risk === 'High' ? 'bg-red-100 text-red-700' :
            contact.churn_risk === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
            'bg-green-100 text-green-700'
          }`}>
            {contact.churn_risk}
          </span>
        </div>

        <div>
          <p className="text-xs text-gray-500 mb-1">Open Tickets</p>
          <p className="text-sm font-semibold text-gray-900">{contact.open_tickets}</p>
        </div>
      </div>
    </PanelCard>
  )
}

export default ContactProfileCard
