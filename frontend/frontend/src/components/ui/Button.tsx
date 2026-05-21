import React from 'react'
import clsx from 'clsx'

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
}

const variantClasses: Record<NonNullable<Props['variant']>, string> = {
  primary: 'bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:ring-indigo-500',
  secondary: 'bg-slate-100 text-slate-900 hover:bg-slate-200 focus-visible:ring-slate-400',
  ghost: 'bg-transparent text-slate-700 hover:bg-slate-100 focus-visible:ring-slate-400',
  danger: 'bg-rose-600 text-white hover:bg-rose-700 focus-visible:ring-rose-500',
}

export const Button: React.FC<Props> = ({ className, variant = 'primary', children, ...props }) => {
  return (
    <button
      className={clsx(
        'inline-flex items-center justify-center rounded-2xl px-4 py-2 text-sm font-semibold transition-colors duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60',
        variantClasses[variant],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}

export default Button
