# Lead Generation Agent - Prompting Guide

## How to Structure Your Lead Generation Prompt

### 1. Define Your Ideal Customer Profile (ICP)

```
Our Ideal Customer Profile:
- Industry: [Your target industries]
- Company Size: [Employee range]
- Revenue: [Annual revenue range]
- Location: [Geographic focus]
- Technology: [Tech stack they use]
- Decision Maker: [Job titles]
```

**Example:**
```
- Industry: E-commerce, Retail, Consumer Goods
- Company Size: 100-1000 employees
- Revenue: $10M-$100M annually
- Location: North America
- Technology: Shopify, WooCommerce, custom platforms
- Decision Maker: CMO, Director of Marketing, Head of E-commerce
```

---

### 2. Set Qualification Criteria

```
Score leads based on:
1. [Criterion 1] = [Points]
2. [Criterion 2] = [Points]
3. [Criterion 3] = [Points]

Total: Hot (70+), Warm (40-69), Cold (<40)
```

**Example:**
```
1. Annual revenue over $20M = 30 points
2. Used our competitor in last 12 months = 25 points
3. Attended our webinar/downloaded content = 20 points
4. Located in target city = 15 points
5. Decision maker identified = 10 points
```

---

### 3. Specify Data Sources

Tell Claude where to look:
```
Data Sources:
- Primary: leads_database.csv (10,000 records)
- Secondary: crm_exports/salesforce_data.json
- Enrichment: LinkedIn company data
- Behavioral: website_analytics.db
```

---

### 4. Define Output Requirements

```
I need:
1. Top [N] qualified leads
2. Format: [CSV/JSON/Excel]
3. Include fields: [list specific fields]
4. Sort by: [criteria]
5. Save to: [filename]
```

---

## Complete Prompt Templates

### Template 1: Basic Lead Discovery

```
Find qualified leads from leads_database.csv.

Ideal Customer:
- Industry: SaaS, Technology, Software Development
- Size: 50-500 employees
- Revenue: $5M+
- Location: USA (tech hubs preferred)

Qualification:
- Recent website visit (last 30 days) = High priority
- Downloaded whitepaper = Medium priority
- Email engagement (opens/clicks) = Bonus points

Tasks:
1. Load and analyze the database
2. Filter for ICP matches
3. Score each lead (0-100)
4. Return top 50 leads sorted by score
5. Export to 'hot_leads.csv'
```

---

### Template 2: Re-engagement Campaign

```
Find dormant leads to re-engage.

Criteria:
- Had interaction 6-12 months ago
- No activity in last 6 months
- Previously showed high interest (demo request, trial signup)
- Company still matches our ICP
- No closed-lost reason

Analysis needed:
1. Segment by original interest area
2. Identify trigger events (funding, new hire, expansion)
3. Create personalized re-engagement angle for each
4. Priority: Those with recent positive business news

Output: Top 30 re-engagement opportunities with messaging suggestions
```

---

### Template 3: Account-Based Marketing (ABM)

```
Build target account list for ABM campaign.

Target Accounts Profile:
- Enterprise companies (1000+ employees)
- Revenue: $100M+
- Industries: Finance, Healthcare, Manufacturing
- Must have: Multiple decision makers identified

For each account:
1. Map decision-making unit (DMU):
   - Economic buyer
   - Technical buyer
   - End users
   - Influencers
2. Identify account signals:
   - Technology changes
   - Leadership changes
   - Expansion/growth
   - Competitor usage
3. Score account fit (1-10)
4. Suggest multi-threaded approach

Deliver: Top 25 accounts with full DMU mapping and engagement strategy
```

---

### Template 4: Competitor Displacement

```
Find companies using competitor products who are good switch candidates.

Competitors to target:
- CompetitorA (look for dissatisfaction signals)
- CompetitorB (look for pricing complaints)
- CompetitorC (look for contract renewal dates)

Switching signals:
- Negative reviews/complaints
- Contract expires in next 6 months
- Recent leadership change
- Growth beyond competitor's capabilities
- Public statements about limitations

Analyze:
1. Current competitor satisfaction level
2. Switching cost/complexity
3. Our competitive advantage for them
4. Estimated win probability

Deliver: Top 20 switch candidates with displacement playbook
```

---

### Template 5: Expansion/Upsell

```
Find existing customers ready for expansion.

Current Customer Analysis:
- Using basic plan for 6+ months
- High product engagement (daily active users)
- Approaching plan limits (usage, seats, features)
- Strong health score (no support issues)
- Growing company (hiring, revenue up)

Upsell Triggers:
- 80%+ of plan limits used
- Requested features only in higher tiers
- Team size doubled
- New use cases emerging
- High NPS score (9-10)

For each candidate:
1. Calculate expansion revenue potential
2. Identify specific upgrade path
3. Suggest timing for outreach
4. Draft personalized expansion pitch

Output: Top 40 expansion opportunities sorted by revenue potential
```

---

### Template 6: Event-Based Lead Generation

```
Find leads experiencing trigger events.

Monitor for:
- Company Triggers:
  - Recent funding round (Series A-C)
  - New executive hire (C-level, VP)
  - Office expansion/new location
  - Product launch
  - Acquisition or merger

- Market Triggers:
  - Industry regulation changes
  - Technology shifts
  - Seasonal peaks

- Personal Triggers:
  - Decision maker job change (new role = new priorities)
  - Conference/event attendance
  - Content engagement spike

For each trigger event:
1. Verify event date and details
2. Assess relevance to our solution (1-10)
3. Identify timing window (strike while hot)
4. Create event-specific messaging
5. Assign priority level

Deliver: Real-time trigger feed with top 15 immediate opportunities
```

---

### Template 7: Industry Vertical Deep Dive

```
Analyze the Healthcare vertical for expansion.

Objectives:
- Map the entire addressable market in Healthcare
- Identify sub-segments (Hospitals, Clinics, Pharma, Insurance)
- Find underserved niches

For each company:
- Size and revenue
- Current technology stack
- Compliance requirements (HIPAA, etc.)
- Pain points specific to their sub-segment
- Existing relationships with healthcare vendors

Analysis:
1. Total Addressable Market (TAM) size
2. Most accessible sub-segment
3. Key differentiators needed
4. Common objections/concerns
5. Reference customers we can leverage

Deliver: Healthcare vertical strategy with prioritized account list (100 companies)
```

---

### Template 8: Lead Scoring Model Creation

```
Build an intelligent lead scoring model.

Historical Data:
- Analyze last 500 closed-won deals
- Analyze last 500 closed-lost opportunities
- Identify patterns and common attributes

Create model to predict:
- Likelihood to buy (0-100%)
- Expected deal size ($)
- Expected sales cycle length (days)
- Churn risk (low/medium/high)

Factors to consider:
- Firmographic data (size, industry, revenue)
- Behavioral data (engagement, content downloads)
- Technographic data (current tools, tech stack)
- Temporal data (time of year, business cycles)
- Competitive data (who they currently use)

Output:
1. Lead scoring formula with weights
2. Score all current leads in database
3. Identify top 10% of leads (should correlate with 80% of revenue)
4. Recommend score thresholds for SDR handoff
```

---

## Pro Tips for Effective Prompts

### 1. Be Specific About Numbers
❌ "Find some good leads"
✅ "Find the top 25 qualified leads scoring 70+ points"

### 2. Define "Qualified"
❌ "Find qualified leads"
✅ "Qualified = $10M+ revenue, 100-500 employees, tech industry, decision maker identified"

### 3. Specify Output Format
❌ "Give me the results"
✅ "Export to CSV with columns: Company, Contact, Score, Reason, Next Action"

### 4. Include Context
❌ "Find leads"
✅ "Find leads for our new AI product targeting data teams who currently use manual processes"

### 5. Set Priorities
❌ "Look at everything"
✅ "Prioritize 1) Recent engagement, 2) Company size, 3) Geography"

### 6. Request Actionability
❌ "Show me leads"
✅ "For each lead provide: Score, qualification reason, recommended first touchpoint, personalized message angle"

---

## Sample Complete Prompt (Copy & Customize)

```
LEAD GENERATION TASK

Product: [Your product/service]
Goal: Find 50 qualified leads for Q4 outbound campaign

IDEAL CUSTOMER PROFILE:
- Industry: [Industries]
- Company Size: [Size range]
- Revenue: [Revenue range]
- Location: [Geographic focus]
- Technology: [Tech they use]
- Decision Maker: [Job titles]

LEAD SOURCES:
- File: leads_master_2024.csv
- Contains: [describe columns/fields]
- Size: [number of records]

QUALIFICATION CRITERIA (Score 0-100):
1. [Criterion] = [points] points
2. [Criterion] = [points] points
3. [Criterion] = [points] points
4. [Criterion] = [points] points
5. [Criterion] = [points] points

PRIORITY RANKING:
- Hot: 70+ points (immediate outreach)
- Warm: 40-69 points (nurture sequence)
- Cold: <40 points (long-term nurture)

TASKS:
1. Load and analyze [data source]
2. Apply ICP filters
3. Score each lead using criteria above
4. Segment into Hot/Warm/Cold
5. For Hot leads, provide:
   - Company overview
   - Key decision maker contact
   - Qualification score breakdown
   - Recommended messaging angle
   - Best time to reach out
6. Export results to 'q4_outbound_leads.csv'

SPECIAL CONSIDERATIONS:
- [Any exclusions, e.g., "Exclude current customers"]
- [Any preferences, e.g., "Prefer companies with recent funding"]
- [Any must-haves, e.g., "Must have email address"]

Please analyze the database and deliver actionable lead list with recommendations.
```

---

## Questions to Ask Yourself Before Prompting

1. **What is my goal?**
   - Number of leads needed?
   - Campaign purpose? (outbound, event, content)

2. **What data do I have?**
   - File format and location?
   - Data quality/completeness?
   - Field names and types?

3. **What makes a "good" lead for me?**
   - Firmographic criteria?
   - Behavioral signals?
   - Timing factors?

4. **What do I need to do with the results?**
   - Import to CRM?
   - Send to sales team?
   - Use for ads targeting?

5. **What resources/context should Claude use?**
   - Historical win/loss data?
   - Competitor information?
   - Market research?

Answer these, then build your prompt!
