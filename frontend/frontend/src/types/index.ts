export interface EmailItem {
  id: string
  sender: string
  subject: string
  category: string
  urgency: 'Low' | 'Medium' | 'High' | 'Critical' | string
  sentiment: 'Positive' | 'Neutral' | 'Negative' | string
  timestamp: string
  escalation: boolean
  needs_human: boolean
  auto_replied: boolean
  spam: boolean
  thread_id: string
}

export interface ThreadMessage {
  id: string
  sender: string
  body: string
  timestamp: string
  sentiment: string
  escalation_marker?: string
  type?: 'incoming' | 'outgoing'
}

export interface ContactProfile {
  email: string
  name: string
  account_value: string
  churn_risk: 'Low' | 'Medium' | 'High'
  vip_status: boolean
  open_tickets: number
  web_intelligence?: {
    summary: string
    rating?: number
    review_count?: number
    themes?: string[]
  }
}

export interface ThreadDetails {
  contact: ContactProfile
  messages: ThreadMessage[]
  agent_reasoning: AgentReasoningStep[]
  rag_context: RagContext[]
  actions: {
    draft: string
    status: string
  }
}

export interface AgentReasoningStep {
  step_number: number
  thought: string
  action: string
  observation: string
  next_decision: string
  confidence: number
}

export interface RagContext {
  id: string
  chunk: string
  source: string
  similarity: number
}

export interface AnalyticsPoint {
  timestamp: string
  value: number
}

export interface SentimentTrendPoint {
  timestamp: string
  positive: number
  neutral: number
  negative: number
}

export interface CategorySegment {
  category: string
  count: number
}

export interface EscalationMetrics {
  escalated: number
  resolved: number
  humanReviewPct: number
}

export interface AutomationMetrics {
  autoReplyRate: number
  dryRunCount: number
  executionCount: number
}

export interface AtRiskAccount {
  company: string
  churnRisk: 'Low' | 'Medium' | 'High'
  unresolvedEscalations: number
  negativeSentimentTrend: number
}

export interface TeamPerformanceItem {
  team: string
  responseRate: number
  resolutionRate: number
  backlog: number
}

export interface DashboardOverview {
  sentimentTrend: SentimentTrendPoint[]
  categoryBreakdown: CategorySegment[]
  escalationMetrics: EscalationMetrics
  automationMetrics: AutomationMetrics
  atRiskAccounts: AtRiskAccount[]
  inboxVolume: {
    total: number
    escalated: number
    needsHuman: number
    autoReplied: number
  }
  teamPerformance: TeamPerformanceItem[]
}

export interface SagencyAnalytics {
  sentimentTrend: SentimentTrendPoint[]
  categoryBreakdown: CategorySegment[]
  escalationMetrics?: EscalationMetrics
  automationMetrics?: AutomationMetrics
  atRiskAccounts?: AtRiskAccount[]
}
