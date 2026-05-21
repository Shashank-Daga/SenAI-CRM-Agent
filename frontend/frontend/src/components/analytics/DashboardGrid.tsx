import React from 'react'

interface Props {
  children?: React.ReactNode
}

export const DashboardGrid: React.FC<Props> = ({ children }) => {
  return <div className="grid gap-6 xl:grid-cols-12">{children}</div>
}

export default DashboardGrid
