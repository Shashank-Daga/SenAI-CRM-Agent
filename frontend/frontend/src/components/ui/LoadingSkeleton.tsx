import React from 'react'

interface Props {
  rows?: number
}

export const LoadingSkeleton: React.FC<Props> = ({ rows = 6 }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="animate-pulse flex items-center gap-4 p-3 bg-white/5 rounded">
          <div className="h-8 w-8 bg-gray-200 rounded" />
          <div className="flex-1 space-y-2">
            <div className="h-3 bg-gray-200 rounded w-3/4" />
            <div className="h-2 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      ))}
    </div>
  )
}

export default LoadingSkeleton
