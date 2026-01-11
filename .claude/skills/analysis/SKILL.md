---
name: analysis
description: >
  Analyze extracted documents using predefined schemas for M&A deals, SEC filings,
  and legal agreements. Use after ingest-content has extracted text to temp/ directory.
  Outputs structured JSON and human-readable Markdown reports to output/ directory.
---

# Document Analysis

Generate structured analysis from extracted document content.

## Available Schemas

### Financial Document Schemas

| Schema | Use Case | Location |
|--------|----------|----------|
| **10-K** | Annual reports, financial performance | Built-in (below) |
| **M&A** | Merger agreements, deal terms | Built-in (below) |
| **Proxy (DEF 14A)** | Executive comp, board info | Built-in (below) |

### News & Research Schemas

| Schema | Use Case | Location |
|--------|----------|----------|
| **News Summary** | Article wisdom extraction | `schemas/news-summary.md` |
| **Claims Analysis** | Fact-checking, evidence evaluation | `schemas/claims-analysis.md` |
| **Stakeholder Positions** | Multi-perspective debate analysis | `schemas/stakeholder-positions.md` |
| **Timeline Narrative** | Chronological event analysis | `schemas/timeline-narrative.md` |
| **Predictions** | Future outlook, forecasts | `schemas/predictions.md` |

## Schema Selection Guide

| User Question | Recommended Schema |
|---------------|-------------------|
| "Summarize this article" | News Summary |
| "Is this claim true?" | Claims Analysis |
| "What are the different perspectives?" | Stakeholder Positions |
| "How did this happen?" | Timeline Narrative |
| "What's the outlook?" | Predictions |
| "What are the financials?" | 10-K Schema |
| "What are the deal terms?" | M&A Schema |
| "What's the CEO paid?" | Proxy Schema |

## Input/Output

**Input:** Read extracted content from Jina or from `temp/{document}.md`
**Output:** Structured report to chat or file

## Output Options

| User Request | Action |
|--------------|--------|
| *(default)* | Output directly to chat |
| "Save the report" | Write to `output/{topic}_report.md` |
| "Save as JSON" | Write to `output/{topic}_report.json` |
| "Save to output/" | Write to `output/` directory |

### File Output Examples

**Markdown report:**
```
Write:
  file_path: "output/nike_10k_analysis.md"
  content: "{report content}"
```

**JSON report:**
```
Write:
  file_path: "output/nike_10k_analysis.json"
  content: "{structured JSON}"
```

### Naming Convention

Use descriptive filenames:
- `{company}_{doc_type}_report.md` — e.g., `apple_10k_report.md`
- `{topic}_{schema}_analysis.md` — e.g., `ev_tariffs_stakeholder_analysis.md`
- `{event}_timeline.md` — e.g., `ftx_collapse_timeline.md`

---

## Financial Schemas (Built-in)

### 10-K Annual Report Schema

Extract these fields with page references:

```json
{
  "company": {
    "name": "Company Name",
    "ticker": "TICK",
    "fiscal_year_end": "2024-05-31"
  },
  "financials": {
    "revenue": 51362000000,
    "revenue_yoy_change_pct": -2.3,
    "net_income": 5700000000,
    "total_assets": 38000000000,
    "total_debt": 9500000000,
    "cash_and_equivalents": 7900000000
  },
  "segments": [
    {"name": "North America", "revenue": 21500000000, "pct_of_total": 42},
    {"name": "Greater China", "revenue": 7500000000, "pct_of_total": 15}
  ],
  "risk_factors": [
    "Competition from domestic brands in China",
    "Foreign currency fluctuations",
    "Supply chain disruptions"
  ],
  "key_metrics": {
    "gross_margin_pct": 44.6,
    "operating_margin_pct": 12.1,
    "employees": 83700
  }
}
```

### M&A Deal Schema

```json
{
  "deal_summary": {
    "acquirer": "Company A",
    "target": "Company B",
    "deal_type": "merger",
    "announcement_date": "2024-01-15"
  },
  "financial_terms": {
    "deal_value": 20000000000,
    "price_per_share": 85.50,
    "premium_pct": 35,
    "cash_component": 10000000000,
    "stock_component": 10000000000
  },
  "key_provisions": {
    "termination_fee_target": 750000000,
    "termination_fee_acquirer": 1500000000,
    "go_shop_period_days": 45,
    "outside_date": "2025-06-30"
  },
  "conditions": [
    "Shareholder approval",
    "Regulatory approval",
    "No material adverse change"
  ],
  "governing_law": "Delaware"
}
```

### Proxy Statement (DEF 14A) Schema

```json
{
  "meeting": {
    "date": "2024-09-15",
    "type": "annual"
  },
  "executive_compensation": {
    "ceo_name": "John Smith",
    "ceo_total_compensation": 25000000,
    "named_executives": [
      {"name": "Jane Doe", "title": "CFO", "total": 12000000},
      {"name": "Bob Wilson", "title": "COO", "total": 11000000}
    ]
  },
  "board": {
    "total_directors": 12,
    "independent_directors": 10,
    "new_nominees": ["Alice Johnson"]
  },
  "proposals": [
    {"number": 1, "title": "Election of Directors", "recommendation": "FOR"},
    {"number": 2, "title": "Advisory Vote on Executive Compensation", "recommendation": "FOR"},
    {"number": 3, "title": "Ratification of Auditors", "recommendation": "FOR"}
  ]
}
```

---

## Output Format Template

### Markdown Report Template

```markdown
# Analysis: {Document Name}

**Document Type:** {Type}
**Source:** {Company/Publication}
**Period/Date:** {Date}
**Schema Used:** {Schema name}
**Analyzed:** {Current Date}

---

## Executive Summary

{2-3 sentence overview of key findings}

## Key Metrics

| Metric | Value | Context |
|--------|-------|---------|
| {metric} | {value} | {comparison/change} |

## Detailed Findings

### {Section 1}

{Key observations with specific numbers and references}

### {Section 2}

{Additional findings}

---

## Notes

- {Any caveats or missing data}
- {Assumptions made during analysis}

## Source

- **Document:** {filename or URL}
- **Extraction Date:** {Date}
```

---

## Analysis Process

1. **Identify content type**: News article? SEC filing? Multiple sources?
2. **Select appropriate schema**: Match question to schema (see guide above)
3. **Read the schema file**: For news schemas, read from `schemas/` directory
4. **Extract each field**: Follow the schema structure precisely
5. **Flag missing data**: Explicitly note "not found" rather than guessing
6. **Generate report**: Use markdown template above

## Quality Checklist

Before delivering the report:

- [ ] Correct schema selected for content type
- [ ] All schema fields have values or explicit "not found"
- [ ] Numbers include units (USD, %, etc.)
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Sources cited for all facts
- [ ] Executive summary captures main insights
- [ ] Caveats noted for uncertain or missing data

## Combining Schemas

For complex research, you may need multiple schemas:

**Example: Company crisis analysis**
1. **Timeline Narrative**: What happened and when
2. **Stakeholder Positions**: How different parties reacted
3. **Predictions**: What analysts say will happen next

**Example: Policy change impact**
1. **News Summary**: What the policy is
2. **Claims Analysis**: Are the stated benefits real?
3. **Stakeholder Positions**: Who supports/opposes
