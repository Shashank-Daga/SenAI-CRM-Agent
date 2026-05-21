import React from 'react'

interface Tab {
  key: string
  label: string
}

interface Props {
  tabs: Tab[]
  active: string
  onChange: (key: string) => void
}

export const FilterTabs: React.FC<Props> = ({ tabs, active, onChange }) => {
  return (
    <div className="flex items-center gap-2">
      {tabs.map((t) => (
        <button
          key={t.key}
          onClick={() => onChange(t.key)}
          className={`px-3 py-1 rounded-md text-sm ${active === t.key ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'}`}>
          {t.label}
        </button>
      ))}
    </div>
  )
}

export default FilterTabs
