import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { EmailItem } from '../types'
import StatusBadge from './ui/StatusBadge'

interface Props {
  emails: EmailItem[]
}

type SortKey = 'timestamp' | 'sender' | 'subject' | 'urgency'

export const InboxTable: React.FC<Props> = ({ emails }) => {
  const [sortBy, setSortBy] = useState<SortKey>('timestamp')
  const [dir, setDir] = useState<'asc' | 'desc'>('desc')

  const sorted = useMemo(() => {
    const copy = [...emails]
    copy.sort((a, b) => {
      let av: any = a[sortBy]
      let bv: any = b[sortBy]
      if (sortBy === 'timestamp') {
        av = new Date(a.timestamp).getTime()
        bv = new Date(b.timestamp).getTime()
      }
      if (av < bv) return dir === 'asc' ? -1 : 1
      if (av > bv) return dir === 'asc' ? 1 : -1
      return 0
    })
    return copy
  }, [emails, sortBy, dir])

  const toggleSort = (k: SortKey) => {
    if (k === sortBy) setDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    else {
      setSortBy(k)
      setDir('asc')
    }
  }

  return (
    <div className="rounded-md border bg-white/5">
      <table className="min-w-full divide-y">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-3 py-2 text-left text-sm font-medium">Sender</th>
            <th className="px-3 py-2 text-left text-sm font-medium">Subject</th>
            <th className="px-3 py-2 text-left text-sm font-medium">Category</th>
            <th className="px-3 py-2 text-left text-sm font-medium">Urgency</th>
            <th className="px-3 py-2 text-left text-sm font-medium">Sentiment</th>
            <th className="px-3 py-2 text-left text-sm font-medium">Time</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {sorted.map((e) => (
            <Link key={e.id} to={`/thread/${encodeURIComponent(e.sender)}`} className="no-underline">
              <tr className={`cursor-pointer hover:bg-gray-100 ${e.urgency === 'Critical' ? 'bg-red-50 hover:bg-red-100' : ''}`}>
                <td className="px-3 py-3 text-sm">{e.sender}</td>
                <td className="px-3 py-3 text-sm text-gray-700">{e.subject}</td>
                <td className="px-3 py-3 text-sm"><StatusBadge category={e.category} size="sm" /></td>
                <td className="px-3 py-3 text-sm"><StatusBadge urgency={e.urgency} size="sm" escalated={e.escalation} /></td>
                <td className="px-3 py-3 text-sm"><StatusBadge sentiment={e.sentiment} size="sm" /></td>
                <td className="px-3 py-3 text-sm text-gray-500">{new Date(e.timestamp).toLocaleString()}</td>
              </tr>
            </Link>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default InboxTable
