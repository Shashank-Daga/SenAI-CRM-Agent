import React from 'react'

interface Props {
  title: string
  subtitle?: string
  children?: React.ReactNode
}

export const PageHeader: React.FC<Props> = ({ title, subtitle, children }) => {
  return (
    <div className="flex items-start justify-between gap-4 mb-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
        {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-2">{children}</div>
    </div>
  )
}

export default PageHeader
