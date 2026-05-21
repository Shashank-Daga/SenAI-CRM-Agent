import React from 'react'
import PanelCard from './ui/PanelCard'

interface WebIntelligence {
  summary: string
  rating?: number
  review_count?: number
  themes?: string[]
  cached?: boolean
  source?: string
}

interface Props {
  data?: WebIntelligence
}

export const WebIntelligencePanel: React.FC<Props> = ({ data }) => {
  if (!data) {
    return (
      <PanelCard title="Web Intelligence">
        <p className="text-sm text-gray-500">No reputation data available</p>
      </PanelCard>
    )
  }

  return (
    <PanelCard title="Web Intelligence">
      <div className="space-y-3">
        <div>
          <p className="text-xs text-gray-500 mb-1">Summary</p>
          <p className="text-sm text-gray-900">{data.summary}</p>
        </div>

        {data.rating && (
          <div className="flex items-center justify-between pt-2 border-t border-gray-200">
            <div>
              <p className="text-xs text-gray-500">Rating</p>
              <p className="text-lg font-bold text-yellow-600">⭐ {data.rating.toFixed(1)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Reviews</p>
              <p className="text-sm font-medium text-gray-900">{data.review_count?.toLocaleString() || '—'}</p>
            </div>
          </div>
        )}

        {data.themes && data.themes.length > 0 && (
          <div>
            <p className="text-xs text-gray-500 mb-2">Common Themes</p>
            <div className="flex flex-wrap gap-1">
              {data.themes.map((t, i) => (
                <span key={i} className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">
                  {t}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="pt-2 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            {data.cached ? '💾 Cached' : '🔄 Fresh'} from {data.source || 'Trustpilot'}
          </p>
        </div>
      </div>
    </PanelCard>
  )
}

export default WebIntelligencePanel
