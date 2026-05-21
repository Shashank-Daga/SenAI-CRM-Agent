import React, { useState } from 'react'
import { AgentReasoningStep } from '../types'
import PanelCard from './ui/PanelCard'

interface Props {
  steps: AgentReasoningStep[]
}

export const AgentReasoningPanel: React.FC<Props> = ({ steps }) => {
  const [expanded, setExpanded] = useState<number | null>(null)

  if (!steps || steps.length === 0) {
    return (
      <PanelCard title="Agent Reasoning">
        <p className="text-sm text-gray-500">No reasoning trace available</p>
      </PanelCard>
    )
  }

  return (
    <PanelCard title="Agent Reasoning Trace">
      <div className="space-y-2">
        {steps.map((step, idx) => (
          <div 
            key={idx}
            className="border border-indigo-200 bg-indigo-50 rounded p-3 cursor-pointer hover:bg-indigo-100"
            onClick={() => setExpanded(expanded === idx ? null : idx)}
          >
            <div className="flex items-start justify-between mb-1">
              <p className="text-xs font-bold text-indigo-900">Step {step.step_number}</p>
              <p className="text-xs font-semibold text-indigo-700">
                {(step.confidence * 100).toFixed(0)}% confidence
              </p>
            </div>
            
            <p className="text-sm font-semibold text-gray-900 mb-1">Action: {step.action}</p>
            
            {expanded === idx && (
              <div className="mt-3 space-y-2 border-t border-indigo-200 pt-3">
                <div>
                  <p className="text-xs text-indigo-700 font-semibold">Thought</p>
                  <p className="text-xs text-gray-700 whitespace-pre-wrap">{step.thought}</p>
                </div>
                <div>
                  <p className="text-xs text-indigo-700 font-semibold">Observation</p>
                  <p className="text-xs text-gray-700 whitespace-pre-wrap">{step.observation || '—'}</p>
                </div>
                <div>
                  <p className="text-xs text-indigo-700 font-semibold">Next Decision</p>
                  <p className="text-xs text-gray-700">{step.next_decision}</p>
                </div>
              </div>
            )}
            
            {expanded !== idx && (
              <p className="text-xs text-gray-600 truncate">{step.thought}</p>
            )}
          </div>
        ))}
      </div>
    </PanelCard>
  )
}

export default AgentReasoningPanel
