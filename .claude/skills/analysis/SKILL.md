---
name: generate-report
description: Analyze extracted documents using predefined schemas for M&A deals, SEC filings, and legal agreements. Use after ingest-content has extracted text to temp/ directory.
---

# Report Generation Skill

Generate structured analysis from extracted document content.

## Quick Reference

### Input

Read extracted Markdown from `temp/` directory:

```
temp/{document_name}.md
```

### Output

Save reports to `output/` directory:

```
output/{document_name}_report.json
output/{document_name}_report.md
```

## Available Schemas

### 1. M&A Deal Analysis

For merger agreements and acquisition documents.

```json
{
  "deal_summary": {
    "acquirer": "Company Name",
    "target": "Company Name",
    "deal_type": "merger|acquisition|asset_purchase",
    "announcement_date": "YYYY-MM-DD"
  },
  "financial_terms": {
    "deal_value": 0,
    "price_per_share": 0,
    "premium_percentage": 0,
    "cash_component": 0,
    "stock_component": 0
  },
  "key_provisions": {
    "termination_fee_target": 0,
    "termination_fee_acquirer": 0,
    "go_shop_period_days": null,
    "material_adverse_change": true
  },
  "governing_law": "State"
}
```

### 2. 10-K Annual Report

For SEC 10-K filings.

```json
{
  "company": {
    "name": "Company Name",
    "ticker": "TICK",
    "fiscal_year_end": "YYYY-MM-DD"
  },
  "financials": {
    "revenue": 0,
    "revenue_yoy_change": 0,
    "net_income": 0,
    "total_assets": 0,
    "total_debt": 0,
    "cash": 0
  },
  "risk_factors": ["risk 1", "risk 2"],
  "business_segments": [
    {"name": "Segment", "revenue": 0, "percentage": 0}
  ]
}
```

### 3. Proxy Statement (DEF 14A)

For proxy statements.

```json
{
  "meeting": {
    "date": "YYYY-MM-DD",
    "type": "annual|special"
  },
  "executive_compensation": {
    "ceo_name": "Name",
    "ceo_total": 0,
    "executives": [
      {"name": "Name", "title": "Title", "total": 0}
    ]
  },
  "board": {
    "total_directors": 0,
    "independent": 0,
    "new_nominees": ["Name"]
  },
  "proposals": [
    {"number": 1, "title": "Title", "recommendation": "FOR|AGAINST"}
  ]
}
```

## Analysis Steps

1. **Identify document type** from filename or content
2. **Select appropriate schema** from above
3. **Extract each field** with page reference
4. **Flag missing data** rather than guessing
5. **Output both JSON and Markdown**

## Output Templates

### JSON Output

```json
{
  "metadata": {
    "document": "filename.pdf",
    "type": "merger_agreement",
    "analyzed": "YYYY-MM-DD",
    "confidence": "high"
  },
  "data": {
    // Schema fields here
  },
  "page_references": {
    "deal_value": 3,
    "termination_fee": 67
  },
  "notes": ["Any caveats or missing data"]
}
```

### Markdown Output

```markdown
# Analysis: [Document Name]

## Summary
[2-3 sentence overview]

## Key Metrics
| Metric | Value | Page |
|--------|-------|------|
| Deal Value | $X.XB | 3 |

## Details
[Detailed findings by section]

## Notes
- [Any missing or uncertain data]
```

## Quality Checklist

- [ ] All schema fields have values or explicit "not found"
- [ ] Numbers include units (USD, %, etc.)
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Page references for key data points
- [ ] Confidence reflects completeness

## Integration

This is the final step in the pipeline:

```
discover-document → ingest-content → generate-report → [output/*.json, output/*.md]
```
