import React from 'react'
import { Bell, History, Search } from 'lucide-react'

interface Props {
  title?: string
  subtitle?: string
}

export const TopNavbar: React.FC<Props> = ({ title, subtitle }) => {
  return (
    <div className="flex items-center justify-between gap-4 px-6 py-3 h-14">
      {/* Search */}
      <div className="relative flex-1 max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400 pointer-events-none" />
        <input
          placeholder={`Search ${title?.toLowerCase() || 'insights'}, threads, or customers…`}
          className="w-full pl-9 pr-4 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-indigo-400 transition"
        />
      </div>

      {/* Right controls */}
      <div className="flex items-center gap-2">
        <button className="h-9 w-9 flex items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700 transition-colors">
          <Bell className="h-4.5 w-4.5" />
        </button>
        <button className="h-9 w-9 flex items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700 transition-colors">
          <History className="h-4.5 w-4.5" />
        </button>
        <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
          <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center overflow-hidden">
            <span className="text-xs font-semibold text-indigo-700">AR</span>
          </div>
          <span className="text-sm font-medium text-slate-700">Alex Rivera</span>
        </div>
      </div>
    </div>
  )
}

export default TopNavbar
