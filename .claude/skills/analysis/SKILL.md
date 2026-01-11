---
name: generate-report
description: >
  Analyze extracted documents using predefined schemas for M&A deals, SEC filings,
  and legal agreements. Use after ingest-content has extracted text to temp/ directory.
  Outputs structured JSON and human-readable Markdown reports to output/ directory.
---

# Document Analysis

Generate structured analysis from extracted document content.

## Input/Output

**Input:** Read extracted Markdown from `temp/{document}.md`
**Output:** Save reports to `output/{document}_report.md` and optionally `output/{document}_report.json`

## Document Type Detection

Identify the document type from filename or content:

| Pattern in Filename/Content | Document Type | Schema to Use |
|-----------------------------|---------------|---------------|
| `10-K`, `annual report` | 10-K Annual Report | 10-K Schema |
| `10-Q`, `quarterly` | 10-Q Quarterly Report | 10-Q Schema |
| `merger agreement`, `acquisition` | M&A Deal | M&A Schema |
| `DEF 14A`, `proxy statement` | Proxy Statement | Proxy Schema |
| `8-K`, `current report` | 8-K Current Report | 8-K Schema |

## Analysis Schemas

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

## Output Format

### Markdown Report Template

```markdown
# Analysis: {Document Name}

**Document Type:** {10-K / Merger Agreement / Proxy Statement}
**Company:** {Company Name}
**Period:** {Fiscal Year / Transaction Date}
**Analyzed:** {Current Date}

---

## Executive Summary

{2-3 sentence overview of key findings}

## Key Metrics

| Metric | Value | Page Reference |
|--------|-------|----------------|
| Revenue | $51.4B | 45 |
| Net Income | $5.7B | 47 |
| YoY Change | -2.3% | 45 |

## Detailed Findings

### {Section 1: e.g., Financial Performance}

{Key observations with specific numbers and page references}

### {Section 2: e.g., Geographic Segments}

{Breakdown by region with trends}

### {Section 3: e.g., Risk Factors}

{Top risks identified in the filing}

---

## Notes

- {Any caveats or missing data}
- {Assumptions made during analysis}

## Source

- **Document:** {filename.pdf}
- **Pages Analyzed:** {1-150}
- **Extraction Date:** {Date}
```

## Analysis Process

1. **Read the extracted Markdown** from `temp/{document}.md`
2. **Identify document type** from filename or content
3. **Select appropriate schema** from above
4. **Extract each field** with page references where possible
5. **Flag missing data** explicitly rather than guessing
6. **Generate both formats:**
   - `output/{document}_report.md` — Human-readable
   - `output/{document}_report.json` — Structured data (optional)

## Quality Checklist

Before delivering the report:

- [ ] All schema fields have values or explicit "not found"
- [ ] Numbers include units (USD, %, etc.)
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Page references for key data points
- [ ] Executive summary captures main insights
- [ ] Caveats noted for uncertain or missing data
