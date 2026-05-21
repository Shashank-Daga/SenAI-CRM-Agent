import React from 'react'
import Sidebar from './Sidebar'
import TopNavbar from './TopNavbar'
import { useLocation } from 'react-router-dom'

interface Props {
  children?: React.ReactNode
}

const pageTitles: Record<string, { title: string; subtitle: string }> = {
  '/': { title: 'Intelligence Dashboard', subtitle: 'insights, threads, or customers' },
  '/dashboard': { title: 'Intelligence Dashboard', subtitle: 'insights, threads, or customers' },
  '/inbox': { title: 'Inbox', subtitle: 'enterprise intelligence' },
  '/analytics': { title: 'Analytics', subtitle: 'analytics' },
  '/settings': { title: 'Settings', subtitle: 'settings' },
}

export const DashboardLayout: React.FC<Props> = ({ children }) => {
  const location = useLocation()
  const pageInfo = pageTitles[location.pathname] || pageTitles['/dashboard']

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex">
      <Sidebar />
      <div className="flex-1 ml-[220px] min-h-screen flex flex-col">
        {/* Sticky top nav */}
        <div className="sticky top-0 z-20 bg-white border-b border-slate-200">
          <TopNavbar title={pageInfo.title} subtitle={pageInfo.subtitle} />
        </div>
        {/* Page content */}
        <main className="flex-1 px-6 py-6">
          <div className="mx-auto max-w-[1280px]">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default DashboardLayout
