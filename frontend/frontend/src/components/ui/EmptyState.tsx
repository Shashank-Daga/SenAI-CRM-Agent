import React from 'react'

interface Props {
  title?: string
  description?: string
}

export const EmptyState: React.FC<Props> = ({ title = 'No items', description = 'Nothing to show here.' }) => {
  return (
    <div className="p-8 text-center text-gray-500">
      <div className="mx-auto mb-4 w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center">
        <svg className="w-8 h-8 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" d="M9 12h6" />
        </svg>
      </div>
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      <p className="mt-2 text-sm">{description}</p>
    </div>
  )
}

export default EmptyState
