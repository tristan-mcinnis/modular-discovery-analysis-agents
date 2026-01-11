---
name: discover-financial
description: >
  Find direct PDF URLs for SEC filings and financial documents using Serper MCP search.
  Use this skill as Step 1 of the research-flow pipeline. Always search with filetype:pdf
  and prioritize sec.gov domains. Returns validated PDF URLs ready for the extraction skill.
---

# Financial Document Discovery

Find official SEC filings, annual reports, and financial documents.

## When to Use

Use this skill for:
- SEC filings (10-K, 10-Q, 8-K, DEF 14A, S-1)
- Annual reports and quarterly reports
- Merger agreements and acquisition documents
- Proxy statements
- Earnings releases and investor presentations

**DO NOT use for general news** — use `discover-news` instead.

## Required Tool

**Use Serper MCP** (`mcp__serper__google_search`):

```
mcp__serper__google_search:
  q: "{company}" "{document type}" filetype:pdf site:sec.gov
  num: "5"
```

## Search Templates

### SEC Filings

| Document Type | Search Query |
|---------------|--------------|
| **10-K** (Annual) | `"{company}" "10-K" {year} filetype:pdf site:sec.gov` |
| **10-Q** (Quarterly) | `"{company}" "10-Q" Q{1-4} {year} filetype:pdf site:sec.gov` |
| **8-K** (Current Report) | `"{company}" "8-K" filetype:pdf site:sec.gov` |
| **DEF 14A** (Proxy) | `"{company}" "DEF 14A" filetype:pdf site:sec.gov` |
| **S-1** (IPO) | `"{company}" "S-1" filetype:pdf site:sec.gov` |
| **20-F** (Foreign Annual) | `"{company}" "20-F" {year} filetype:pdf site:sec.gov` |

### M&A Documents

| Document Type | Search Query |
|---------------|--------------|
| **Merger Agreement** | `"{acquirer}" "{target}" "merger agreement" filetype:pdf` |
| **Tender Offer** | `"{company}" "tender offer" "SC TO" filetype:pdf site:sec.gov` |
| **Proxy (M&A)** | `"{company}" "DEFM14A" filetype:pdf site:sec.gov` |

### Investor Relations

| Document Type | Search Query |
|---------------|--------------|
| **Earnings Release** | `"{company}" "fiscal {year}" "quarterly results" site:investors.{company}.com` |
| **Investor Presentation** | `"{company}" "investor presentation" {year} filetype:pdf` |
| **Annual Report** | `"{company}" "annual report" {year} filetype:pdf` |

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

## Example Searches

### Example 1: Nike 10-K
```
mcp__serper__google_search:
  q: "Nike" "10-K" 2025 filetype:pdf site:sec.gov
  num: "5"
```

### Example 2: Apple Proxy Statement
```
mcp__serper__google_search:
  q: "Apple" "DEF 14A" 2025 filetype:pdf site:sec.gov
  num: "5"
```

### Example 3: Merger Agreement
```
mcp__serper__google_search:
  q: "Microsoft" "Activision" "merger agreement" filetype:pdf
  num: "5"
```

### Example 4: Earnings Release
```
mcp__serper__google_search:
  q: "Tesla" "Q4 2024" "earnings" site:ir.tesla.com
  num: "5"
```

## Output Format

Return the URL for the next step:

```
Found: Nike FY2025 10-K
URL: https://www.sec.gov/Archives/edgar/data/320187/000032018725000047/nke-20250531.htm
Source: sec.gov
Document Type: 10-K Annual Report
Filing Date: 2025-07-25
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

## Choosing the Right Document

Match the source to the question:

| Question Type | Best Source | Why |
|---------------|-------------|-----|
| Specific metrics (revenue, margins) | Earnings press release | Concise, key numbers |
| Segment breakdown (China, Europe) | 10-K or earnings call | Detailed breakdowns |
| Risk factors, legal issues | 10-K filing | Full disclosure required |
| Executive compensation | Proxy statement (DEF 14A) | Detailed comp tables |
| Deal terms | Merger agreement | Actual contract |
| Future guidance | Earnings call transcript | Management commentary |
