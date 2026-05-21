import React from 'react'

interface Props {
  title: string
  subtitle?: string
  children: React.ReactNode
}

export const ChartCard: React.FC<Props> = ({ title, subtitle, children }) => {
  return (
    <div className="rounded-3xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-4">
        <div>
          <h3 className="text-base font-semibold text-slate-900">{title}</h3>
          {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
        </div>
      </div>
      <div className="min-h-[260px]">{children}</div>
    </div>
  )
}

export default ChartCard
