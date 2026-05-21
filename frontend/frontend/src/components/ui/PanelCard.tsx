import React from 'react'

interface Props {
  title?: string
  children?: React.ReactNode
}

export const PanelCard: React.FC<Props> = ({ title, children }) => {
  return (
    <div className="bg-white/5 border border-gray-100/10 rounded-lg p-4 shadow-sm">
      {title && <div className="mb-3"><h3 className="text-sm font-medium text-gray-900">{title}</h3></div>}
      <div>{children}</div>
    </div>
  )
}

export default PanelCard
