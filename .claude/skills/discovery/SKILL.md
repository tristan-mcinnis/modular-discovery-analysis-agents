---
name: discover-document
description: Find official PDF documents using Serper MCP search. Prioritizes SEC.gov, government sites, and company IR domains. Use when you need to locate financial or legal documents.
---

# Document Discovery Skill

Find verified PDF links for financial and legal documents.

## Quick Reference

### Search Pattern

Always use `filetype:pdf` and target trusted domains:

```
"{company}" "{document type}" filetype:pdf site:sec.gov
```

### Trusted Domains (Priority Order)

1. `sec.gov` — SEC EDGAR filings
2. `*.gov` — Government sources
3. `investor.{company}.com` — Official IR sites
4. `{company}.com/investors` — Company investor pages

## Search Templates

| Document Type | Search Query |
|---------------|--------------|
| 10-K Annual Report | `"{company}" "10-K" filetype:pdf site:sec.gov` |
| 10-Q Quarterly | `"{company}" "10-Q" {quarter} {year} filetype:pdf site:sec.gov` |
| Merger Agreement | `"{acquirer}" "{target}" "merger agreement" filetype:pdf` |
| Proxy Statement | `"{company}" "DEF 14A" OR "proxy statement" filetype:pdf site:sec.gov` |
| S-1 IPO Filing | `"{company}" "S-1" filetype:pdf site:sec.gov` |

## Validation Checklist

Before returning a URL, verify:

- [ ] URL ends in `.pdf` (direct link, not landing page)
- [ ] Domain is trusted (see list above)
- [ ] Document title matches search intent
- [ ] Most recent version if multiple exist

## Output Format

Return results as:

```json
{
  "url": "https://sec.gov/Archives/.../document.pdf",
  "title": "Document Title",
  "domain": "sec.gov",
  "confidence": "high"
}
```

**Confidence levels:**
- `high` — Direct PDF from sec.gov or .gov
- `medium` — PDF from verified company IR domain
- `low` — Other source (ask user to confirm)

## Error Recovery

| Issue | Action |
|-------|--------|
| No PDF results | Remove `filetype:pdf`, note browser may be needed |
| Wrong document | Add year or specific filing type to query |
| Multiple versions | Return most recent, note alternatives |

## Integration

Pass validated URLs to `ingest-content` skill for extraction:

```
discover-document → [URL] → ingest-content → [Markdown] → generate-report
```
