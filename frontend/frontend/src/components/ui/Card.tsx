import React from 'react'
import { motion } from 'framer-motion'

interface Props {
  title?: string
  subtitle?: string
  className?: string
  children?: React.ReactNode
}

export const Card: React.FC<Props> = ({ title, subtitle, className = '', children }) => {
  return (
    <motion.section
      layout
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      className={`rounded-2xl border border-slate-200/80 bg-white p-6 shadow-sm ${className}`}
    >
      {(title || subtitle) && (
        <div className="mb-5 flex items-start justify-between gap-4">
          <div>
            {title && <h2 className="text-lg font-semibold text-slate-900">{title}</h2>}
            {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
          </div>
        </div>
      )}
      {children}
    </motion.section>
  )
}

export default Card
