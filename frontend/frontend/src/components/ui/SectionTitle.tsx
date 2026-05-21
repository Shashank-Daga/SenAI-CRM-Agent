import React from 'react'

interface Props {
  title: string
  caption?: string
}

export const SectionTitle: React.FC<Props> = ({ title, caption }) => (
  <div className="mb-3">
    <h2 className="text-sm font-semibold text-gray-900">{title}</h2>
    {caption && <p className="text-xs text-gray-500 mt-1">{caption}</p>}
  </div>
)

export default SectionTitle
