import React from 'react'
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react'

interface Props {
  value: string
  trend: 'positive' | 'neutral' | 'negative'
  label?: string
}

const iconMap = {
  positive: ArrowUpRight,
  neutral: Minus,
  negative: ArrowDownRight,
}

const colorMap = {
  positive: 'bg-emerald-100 text-emerald-700',
  neutral: 'bg-slate-100 text-slate-700',
  negative: 'bg-rose-100 text-rose-700',
}

export const TrendBadge: React.FC<Props> = ({ value, trend, label }) => {
  const Icon = iconMap[trend]

  return (
    <div className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${colorMap[trend]}`}>
      <Icon className="h-3.5 w-3.5" />
      <span>{label ?? value}</span>
    </div>
  )
}

export default TrendBadge
