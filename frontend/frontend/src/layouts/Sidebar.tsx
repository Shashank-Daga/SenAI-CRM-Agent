import React from 'react'
import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Inbox, BarChart3, Settings, LifeBuoy, HelpCircle, Zap, Plus } from 'lucide-react'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/inbox', label: 'Inbox', icon: Inbox },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export const Sidebar: React.FC = () => {
  return (
    <aside className="fixed left-0 top-0 z-30 h-full w-[220px] border-r border-slate-200 bg-white flex flex-col">
      {/* Logo */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center gap-2.5 mb-1">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-sm">
            <Zap className="h-4 w-4" />
          </div>
          <div>
            <p className="text-sm font-bold text-slate-900 leading-tight">Sen AI</p>
            <p className="text-[10px] text-slate-500 leading-tight">Enterprise Intelligence</p>
          </div>
        </div>
      </div>

      {/* New Message Button */}
      <div className="px-4 mb-5">
        <button className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg py-2.5 transition-colors">
          <Plus className="h-4 w-4" />
          New Message
        </button>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 space-y-0.5">
        {navItems.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-50 text-indigo-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={`h-4 w-4 ${isActive ? 'text-indigo-600' : 'text-slate-400'}`} />
                  {item.label}
                </>
              )}
            </NavLink>
          )
        })}
      </nav>

      {/* Bottom */}
      <div className="px-3 pb-6 space-y-0.5">
        <div className="border-t border-slate-100 pt-3 space-y-0.5">
          <button className="w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors">
            <LifeBuoy className="h-4 w-4 text-slate-400" />
            Support
          </button>
          <button className="w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors">
            <HelpCircle className="h-4 w-4 text-slate-400" />
            Help
          </button>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
