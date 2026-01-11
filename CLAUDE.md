# MDAA - Modular Discovery & Analysis Agent

## IMPORTANT: When to Use This Pipeline

**USE THE RESEARCH-FLOW SKILL** when the user asks about:
- SEC filings (10-K, 10-Q, 8-K, DEF 14A, S-1)
- Annual reports, quarterly reports, or financial statements
- Merger agreements or acquisition documents
- Proxy statements or executive compensation
- Any official financial or legal document

**DO NOT** just search the web and summarize news articles. Get the **actual source document**.

### Trigger Phrases

When you see these patterns, use the research-flow skill:
- "Find [company] 10-K..."
- "Analyze [company] annual report..."
- "Summarize [company] financials..."
- "Get the merger agreement for..."
- "What does [company]'s SEC filing say about..."
- "Find [company]'s latest financial statement..."

## Pipeline Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. DISCOVER     │────▶│ 2. READ         │────▶│ 3. ANALYZE      │
│                 │     │                 │     │                 │
│ Serper MCP      │     │ Jina MCP        │     │ Apply schema    │
│ filetype:pdf    │     │ read_url        │     │ Generate report │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Quick Reference

### Step 1: Search for the Document
```
mcp__serper__google_search:
  q: "{company}" "{doc type}" filetype:pdf site:sec.gov
```

### Step 2: Read with Jina
```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/.../filing.htm"
```

### Step 3: Analyze
Apply the appropriate schema from `.claude/skills/analysis/SKILL.md`

## Skill Locations

```
.claude/skills/
├── research-flow/SKILL.md   # Main orchestrator - START HERE
├── discovery/SKILL.md       # Step 1: Find document URLs
├── extraction/SKILL.md      # Step 2: Read content (Jina primary)
└── analysis/SKILL.md        # Step 3: Schema-based analysis
```

## Example

**User:** "Find Nike's latest 10-K and summarize their China business"

**Correct approach:**
1. Search: `"Nike" "10-K" 2025 filetype:pdf site:sec.gov`
2. Read: `mcp__jina__read_url` on the SEC filing URL
3. Analyze: Find Greater China section, extract metrics
4. Report: Table with revenue/EBIT, bullet points for challenges, source citation

**Wrong approach:**
- Just searching "Nike China challenges" and summarizing news articles
