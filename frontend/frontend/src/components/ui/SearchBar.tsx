import React from 'react'

interface Props {
  value: string
  onChange: (v: string) => void
  placeholder?: string
}

export const SearchBar: React.FC<Props> = ({ value, onChange, placeholder = 'Search emails, subjects, senders...' }) => {
  return (
    <div className="relative w-full">
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full border border-gray-200 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
    </div>
  )
}

export default SearchBar
