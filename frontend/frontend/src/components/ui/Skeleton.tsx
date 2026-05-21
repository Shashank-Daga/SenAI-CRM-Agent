import React from 'react'
import clsx from 'clsx'

interface Props {
  className?: string
  rows?: number
}

export const Skeleton: React.FC<Props> = ({ className, rows = 4 }) => {
  return (
    <div className={clsx('space-y-3 animate-pulse', className)}>
      {Array.from({ length: rows }).map((_, index) => (
        <div key={index} className="h-4 rounded-2xl bg-slate-200/80" />
      ))}
    </div>
  )
}

export default Skeleton
