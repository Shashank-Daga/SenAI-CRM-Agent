import React from 'react'

interface Props {
  onApproveSend?: () => void
  onEditDraft?: () => void
  onEscalate?: () => void
  onDryAgent?: () => void
  onExecuteAgent?: () => void
  onMarkSpam?: () => void
  isLoading?: boolean
}

export const ActionToolbar: React.FC<Props> = ({
  onApproveSend,
  onEditDraft,
  onEscalate,
  onDryAgent,
  onExecuteAgent,
  onMarkSpam,
  isLoading = false,
}) => {
  return (
    <div className="bg-white border-t border-gray-200 p-4 flex flex-wrap gap-2">
      <button
        onClick={onApproveSend}
        disabled={isLoading}
        className="px-3 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 disabled:opacity-50"
      >
        ✓ Approve & Send
      </button>
      
      <button
        onClick={onEditDraft}
        disabled={isLoading}
        className="px-3 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        ✏️ Edit Draft
      </button>
      
      <button
        onClick={onEscalate}
        disabled={isLoading}
        className="px-3 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700 disabled:opacity-50"
      >
        ⚠️ Escalate
      </button>
      
      <button
        onClick={onDryAgent}
        disabled={isLoading}
        className="px-3 py-2 bg-gray-600 text-white text-sm rounded-md hover:bg-gray-700 disabled:opacity-50"
      >
        🔍 Dry Agent
      </button>
      
      <button
        onClick={onExecuteAgent}
        disabled={isLoading}
        className="px-3 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        ▶️ Execute Agent
      </button>
      
      <button
        onClick={onMarkSpam}
        disabled={isLoading}
        className="px-3 py-2 bg-gray-400 text-white text-sm rounded-md hover:bg-gray-500 disabled:opacity-50"
      >
        🚫 Mark Spam
      </button>
    </div>
  )
}

export default ActionToolbar
