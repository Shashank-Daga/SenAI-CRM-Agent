import React from 'react'

type Urgency = 'Low' | 'Medium' | 'High' | 'Critical' | string
type Sentiment = 'Positive' | 'Neutral' | 'Negative' | string

interface Props {
  urgency?: Urgency
  sentiment?: Sentiment
  category?: string
  escalated?: boolean
  size?: 'sm' | 'md'
}

const urgencyColor = (u?: Urgency) => {
  switch (u) {
    case 'Critical':
      return 'bg-red-600 text-white'
    case 'High':
      return 'bg-orange-500 text-white'
    case 'Medium':
      return 'bg-yellow-400 text-black'
    case 'Low':
      return 'bg-green-500 text-white'
    default:
      return 'bg-gray-200 text-gray-800'
  }
}

const sentimentColor = (s?: Sentiment) => {
  switch (s) {
    case 'Positive':
      return 'bg-green-100 text-green-800'
    case 'Neutral':
      return 'bg-gray-100 text-gray-800'
    case 'Negative':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

export const StatusBadge: React.FC<Props> = ({ urgency, sentiment, category, escalated, size = 'md' }) => {
  const base = size === 'sm' ? 'px-2 py-0.5 text-xs rounded' : 'px-3 py-1 text-sm rounded-md'

  if (urgency) {
    return (
      <span className={`${base} ${urgencyColor(urgency)} font-semibold ${escalated ? 'ring-2 ring-red-300' : ''}`}>
        {urgency}
      </span>
    )
  }

  if (sentiment) {
    return <span className={`${base} ${sentimentColor(sentiment)}`}>{sentiment}</span>
  }

  if (category) {
    return <span className={`${base} bg-slate-100 text-slate-800`}>{category}</span>
  }

  return <span className={`${base} bg-gray-100 text-gray-800`}>—</span>
}

export default StatusBadge
