---
name: discover-document
description: >
  Find direct PDF URLs for SEC filings and financial documents using Serper MCP search.
  Use this skill as Step 1 of the research-flow pipeline. Always search with filetype:pdf
  and prioritize sec.gov domains. Returns validated PDF URLs ready for the extraction skill.
---

# Document Discovery

Find document URLs for financial and legal documents.

## Required Tool

**Use Serper MCP** (`mcp__serper__google_search`):

```
mcp__serper__google_search:
  q: "{company}" "{document type}" filetype:pdf site:sec.gov
  num: "5"
```

## Search Templates

| Document Type | Search Query |
|---------------|--------------|
| **10-K** (Annual) | `"{company}" "10-K" {year} filetype:pdf site:sec.gov` |
| **10-Q** (Quarterly) | `"{company}" "10-Q" Q{1-4} {year} filetype:pdf site:sec.gov` |
| **8-K** (Current Report) | `"{company}" "8-K" filetype:pdf site:sec.gov` |
| **DEF 14A** (Proxy) | `"{company}" "DEF 14A" filetype:pdf site:sec.gov` |
| **S-1** (IPO) | `"{company}" "S-1" filetype:pdf site:sec.gov` |
| **Merger Agreement** | `"{acquirer}" "{target}" "merger agreement" filetype:pdf` |

## Domain Priority

1. `sec.gov` — Official SEC EDGAR (highest confidence)
2. `*.gov` — Other government sources
3. `investor.{company}.com` — Official investor relations
4. `{company}.com/investors` — Company IR pages

## URL Types

SEC EDGAR returns two formats — **both work with Jina**:

| Format | Example | Notes |
|--------|---------|-------|
| HTML filing | `nke-20250531.htm` | Most common, Jina reads directly |
| PDF filing | `nke-20250531.pdf` | Less common, Jina reads directly |

## Output

Return the URL for the next step:

```
Found: Nike FY2025 10-K
URL: https://www.sec.gov/Archives/edgar/data/320187/000032018725000047/nke-20250531.htm
Source: sec.gov
```

## Next Step

Pass the URL to **Jina MCP** for reading:

```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/.../filing.htm"
```

## Fallback Strategy

If no direct results:

1. Search without `filetype:pdf` for EDGAR landing page
2. Navigate to the filing index
3. Find the main document (usually largest .htm file)
4. Use Jina to read it
