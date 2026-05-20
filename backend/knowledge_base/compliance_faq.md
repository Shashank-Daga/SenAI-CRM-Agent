# Compliance FAQ

## HIPAA Compliance

### Is the platform HIPAA-compliant?
Yes, our Enterprise plan is HIPAA-compliant. We maintain active BAA (Business Associate Agreements) with covered entities and business associates.

### What controls do you have?
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.2+)
- Access controls with role-based permissions
- Audit logging of all data access
- Secure data deletion procedures
- Annual risk assessments

### How do I enable HIPAA mode?
1. Execute Business Associate Agreement (BAA)
2. Enable HIPAA compliance in account settings
3. All customer data stored in HIPAA-designated data centers
4. Compliance verified via annual SOC2 audit

### Data Residency
- HIPAA data stored in US data centers only
- No data transfer to non-HIPAA jurisdictions
- Customer can request specific region (US-EAST-1 or US-WEST-2)

## GDPR Compliance

### Data Rights Under GDPR
- Right to access: Export full data at any time
- Right to rectification: Update personal data
- Right to erasure: Hard delete data within 30 days
- Right to data portability: Download data in standard format
- Right to restrict processing: Disable AI classification

### Data Processing Agreement (DPA)
All customers outside US/Canada receive standard DPA at account setup. Enterprise customers can request custom DPA.

### Data Retention
- Deleted emails purged within 30 days
- Backups retained for 90 days then destroyed
- Legal holds can extend retention

### Sub-processors
Current approved sub-processors:
- AWS (data storage)
- SendGrid (email delivery)
- OpenAI (LLM classification, can be disabled)

Notification given 30 days before adding new processors.

## SOC2 Type II

### Certification Status
- Current: SOC2 Type II (Trust Service Criteria: CC, CI, A)
- Certification Period: 2025-2026
- Auditor: Big 4 audit firm
- Scope: Cloud infrastructure, data security, availability

### Access Controls
- Multi-factor authentication required
- Least privilege access
- Segregation of duties
- Quarterly access reviews

### Monitoring & Logging
- Real-time intrusion detection
- 12-month audit log retention
- Automated alert on suspicious activity
- Change management procedures

## Data Residency Options

### Default
- US-EAST-1 (Virginia, AWS)
- Redundancy: Multi-AZ

### Available Options
- **US-WEST-2**: $200/month additional (West Coast)
- **EU-WEST-1**: $400/month additional (Ireland, GDPR-friendly)
- **AP-SOUTHEAST-1**: $400/month additional (Singapore)

### Cross-Region Replication
- Available for Enterprise only
- Real-time replication with <100ms latency
- Asynchronous replication to secondary region
- Failover automated on primary region outage

## Data Breach Notification

### Notification Timeline
- Customer notified within 24 hours of discovery
- Regulatory authorities notified per jurisdiction requirements
- Public disclosure only if >1,000 individuals affected

### What We Provide
- Detailed breach report
- List of affected records/individuals
- Technical details of breach vector
- Corrective actions implemented

## DPA Negotiation

### Standard Processor Terms
- Included for all customers
- 30-day notice before material changes
- Covers US, EU, UK data processing

### Custom DPA
- Available for Enterprise customers
- Legal review: 2-3 weeks
- Additional cost: Tiered by complexity
- Minimum commitment: Annual contract

## Compliance Contacts

- **Privacy Officer**: privacy@company.com
- **Security Officer**: security@company.com
- **Compliance Requests**: compliance@company.com
- **DPA Negotiations**: contracts@company.com

## Audit Trail

All classification, escalation, and manual actions logged with:
- Timestamp
- User ID
- Action type
- Data accessed
- IP address
- User agent

Retention: 12 months (7 years for Enterprise)

## Incident Response SLA

| Severity | Response Time | Resolution Target |
|----------|---|---|
| Data breach | 4 hours | 24 hours |
| Unauthorized access | 2 hours | 8 hours |
| Security vulnerability | 1 hour | 24 hours |

## Third-Party Penetration Testing

- Annual pen testing by independent firm
- Results available to Enterprise customers under NDA
- Previous reports available for SAQ-D compliance
