import React from 'react'

interface Props {
  title: string
  value: string | number
  description?: string
  smallText?: string
  highlight?: boolean
}

export const MetricCard: React.FC<Props> = ({ title, value, description, smallText, highlight }) => {
  return (
    <div className={`rounded-3xl border p-4 shadow-sm ${highlight ? 'border-indigo-200/80 bg-indigo-50/70' : 'border-gray-200 bg-white'}`}>
      <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">{title}</p>
      <div className="mt-3 flex items-end gap-3">
        <p className="text-3xl font-semibold text-slate-900">{value}</p>
        {smallText && <span className="text-sm text-slate-500">{smallText}</span>}
      </div>
      {description && <p className="mt-3 text-sm text-slate-500">{description}</p>}
    </div>
  )
}

export default MetricCard
