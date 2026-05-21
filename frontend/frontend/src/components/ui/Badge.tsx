import React from 'react'
import clsx from 'clsx'

interface Props {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'accent'
  children: React.ReactNode
}

const styles: Record<NonNullable<Props['variant']>, string> = {
  default: 'bg-slate-100 text-slate-700',
  success: 'bg-emerald-100 text-emerald-700',
  warning: 'bg-amber-100 text-amber-700',
  danger: 'bg-rose-100 text-rose-700',
  accent: 'bg-indigo-100 text-indigo-700',
}

export const Badge: React.FC<Props> = ({ variant = 'default', children }) => {
  return <span className={clsx('inline-flex rounded-full px-3 py-1 text-xs font-semibold', styles[variant])}>{children}</span>
}

export default Badge
