# Escalation Matrix

## Escalation Triggers and Routing

### Legal Escalation

#### Triggers
- Keywords: "lawsuit", "legal action", "cease and desist", "attorney", "litigation", "court"
- Email from @*.law firm domains
- Tone analysis: Threatening or formal legal language
- Any mention of compliance violations

#### Routing
- **To**: Legal team (legal@company.com)
- **CC**: Account manager, VP of Operations
- **Priority**: Critical (P0)
- **Response SLA**: 2 hours (Enterprise), 4 hours (Professional)
- **Auto-Reply**: Disabled (manual review only)

#### Handling
1. Legal team reviews within 2 hours
2. If lawsuit threatened: VP escalation
3. Preserve all evidence (email thread, attachments)
4. No admissions of fault in any communication
5. All responses must be reviewed by general counsel

### Ransomware/Security Escalation

#### Triggers
- Keywords: "ransomware", "encrypted files", "decrypt", "bitcoin", "ransom demand"
- Mention of data exfiltration
- Claim of data theft or exposure
- Demand for payment for data recovery

#### Routing
- **To**: Security team (security@company.com)
- **CC**: CISO, VP of Operations, Legal
- **Priority**: Critical (P0)
- **Response SLA**: 30 minutes (any plan)
- **Auto-Reply**: Disabled

#### Handling
1. Immediate incident response activation
2. Forensic investigation initiated
3. Law enforcement notification if required
4. Customer communication coordinated with legal
5. Press/PR coordination if >1,000 users affected

### PR/Brand Escalation

#### Triggers
- Public social media mentions of outages
- Press inquiry subjects
- Mention of media coverage ("posted on Twitter", "Reddit", "news outlet")
- Request for public comment
- VIP customer complaint likely to become public

#### Routing
- **To**: Communications team (comms@company.com)
- **CC**: CEO, VP of Marketing, Legal
- **Priority**: High (P1)
- **Response SLA**: 1 hour
- **Auto-Reply**: Disabled

#### Handling
1. Approved response templates only
2. Legal review of any public statement
3. Coordinate with company social accounts
4. Monitor for secondary coverage
5. Document for crisis communication training

### VIP Churn Escalation

#### VIP Criteria
- Annual contract value >$100,000
- Account age >2 years
- Usage >80% of allocated quota
- Net revenue retention >100%
- Strategic partnership classification

#### Triggers
- Explicit churn request ("cancel", "downgrade", "leave")
- Extended inactivity (>30 days, no activity)
- Spike in support tickets (>5 in 7 days)
- Negative NPS survey (<6/10)
- Mention of competitor evaluation

#### Routing
- **To**: Account manager + VP of Customer Success
- **CC**: CEO, VP of Product
- **Priority**: High (P1)
- **Response SLA**: 4 hours
- **Auto-Reply**: Disabled (account manager calls directly)

#### Handling
1. Account manager reaches out within 4 hours (call not email)
2. Executive check-in call within 24 hours if needed
3. Custom retention offer (20-40% discount, custom terms)
4. Product roadmap presentation if feature-related
5. Escalation decision by end of business day

### Compliance Violation Escalation

#### Triggers
- HIPAA: PHI exposure, unauthorized access, breach
- GDPR: DSAR (Data Subject Access Request), deletion request
- SOC2: Audit failure, control gap
- Industry-specific: FINRA violation, CJIS breach
- Regulatory: Government inquiry, subpoena

#### Routing
- **To**: Compliance officer, Legal, Security
- **CC**: CFO, CEO
- **Priority**: Critical (P0)
- **Response SLA**: 1 hour (any plan)
- **Auto-Reply**: Disabled

#### Handling
1. Immediate legal review
2. Incident response activation
3. Regulatory notification timeline established
4. Internal team coordination mandatory
5. External counsel consultation if needed
6. Documentation for audit trail

## Escalation Decision Tree

```
Email received
    ↓
Is it ransomware/security threat?
    YES → Security Escalation (P0, 30 min)
    NO ↓
Is it legal/lawsuit/threat?
    YES → Legal Escalation (P0, 2-4 hours)
    NO ↓
Is sender a VIP customer requesting churn?
    YES → VIP Churn Escalation (P1, 4 hours)
    NO ↓
Is it a compliance request (GDPR, HIPAA, etc)?
    YES → Compliance Escalation (P0, 1 hour)
    NO ↓
Will this likely go public/media coverage?
    YES → PR Escalation (P1, 1 hour)
    NO ↓
Route to standard support queue (Normal priority)
```

## Escalation Communication

### Notification Template

```
Escalation Alert
├─ Email ID: [UUID]
├─ Thread ID: [UUID]
├─ Escalation Type: [Legal|Ransomware|PR|VIP|Compliance]
├─ Priority: [P0|P1]
├─ SLA: [timeframe]
├─ From: [sender email]
├─ Subject: [subject]
├─ Detected Urgency Tags: [keywords/phrases that triggered escalation]
├─ Confidence Score: [0.00-1.00]
└─ Classification Details:
    ├─ Category: [Complaint|Compliance|Legal|etc]
    ├─ Sentiment: [Positive|Neutral|Negative|Mixed]
    └─ Key Entities: [order IDs, deadlines, monetary amounts]
```

## No-Auto-Reply Rules

Escalated emails NEVER receive auto-reply, even if sender has auto-reply enabled:
- Manual review required before any communication
- Holds email in escalation queue until human review
- Prevents legal admissions or PR missteps

## Escalation Resolution

- Resolved by: Escalation team lead + account manager
- Resolution documented in escalation record
- Customer notified of resolution within SLA
- Post-mortems for P0 incidents within 48 hours
