import React from 'react'
import { RagContext } from '../types'
import PanelCard from './ui/PanelCard'

interface Props {
  contexts: RagContext[]
}

export const RagContextPanel: React.FC<Props> = ({ contexts }) => {
  if (!contexts || contexts.length === 0) {
    return (
      <PanelCard title="RAG Context">
        <p className="text-sm text-gray-500">No retrieved context</p>
      </PanelCard>
    )
  }

  return (
    <PanelCard title="RAG Context">
      <div className="space-y-3">
        {contexts.map((ctx, idx) => (
          <div key={ctx.id || idx} className="border border-gray-200 rounded p-2 bg-gray-50">
            <div className="flex items-center justify-between mb-2">
              <p className="text-xs font-medium text-gray-900">Match {idx + 1}</p>
              <p className="text-xs font-semibold text-green-700">
                {(ctx.similarity * 100).toFixed(0)}% match
              </p>
            </div>
            <p className="text-xs text-gray-700 mb-2 line-clamp-3">{ctx.chunk}</p>
            <p className="text-xs text-gray-500">📄 {ctx.source}</p>
          </div>
        ))}
      </div>
    </PanelCard>
  )
}

export default RagContextPanel
