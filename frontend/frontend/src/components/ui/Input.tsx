import React from 'react'
import clsx from 'clsx'

interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
  icon?: React.ReactNode
}

export const Input: React.FC<Props> = ({ className, icon, ...props }) => {
  return (
    <div className={clsx('group relative w-full', className)}>
      {icon && <div className="pointer-events-none absolute inset-y-0 left-4 flex items-center text-slate-400">{icon}</div>}
      <input
        className={clsx(
          'w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 shadow-sm transition duration-200 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-100',
          icon ? 'pl-12' : 'pl-4',
        )}
        {...props}
      />
    </div>
  )
}

export default Input
