---
name: research-flow
description: >
  USE THIS SKILL when the user asks to find, analyze, or summarize financial documents
  like SEC filings (10-K, 10-Q, 8-K, DEF 14A), merger agreements, or annual reports.
  This skill downloads the actual PDF and extracts its content rather than relying on
  news summaries. Triggers: "find [company] 10-K", "analyze [company] annual report",
  "summarize [company] financials", "get the merger agreement for", "what does [company]'s
  SEC filing say about". ALWAYS prefer this over web search for official financial documents.
---

# Financial Document Research Pipeline

## When to Use This Skill

**ALWAYS use this skill when the user asks about:**
- SEC filings (10-K, 10-Q, 8-K, DEF 14A, S-1)
- Annual reports or quarterly reports
- Merger agreements or acquisition documents
- Proxy statements
- Any official financial or legal document

**DO NOT just search the web and summarize news articles.** Get the actual source document.

## Pipeline Overview

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Step 1: DISCOVER   │────▶│  Step 2: READ       │────▶│  Step 3: ANALYZE    │
│                     │     │                     │     │                     │
│  Serper MCP search  │     │  Jina MCP read_url  │     │  Apply schema and   │
│  filetype:pdf       │     │  (reads PDFs too)   │     │  generate report    │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Choosing the Right Source

**Match the source to the question:**

| Question Type | Best Source | Why |
|---------------|-------------|-----|
| Specific metrics (revenue, margins) | Earnings press release | Concise, key numbers |
| Segment breakdown (China, Europe) | Earnings call transcript | Management commentary |
| Risk factors, legal | 10-K filing | Full disclosure |
| Executive compensation | Proxy statement (DEF 14A) | Detailed comp tables |
| Deal terms | Merger agreement | Actual contract |

**For "challenges in China"** → Use earnings press release + call transcript (not full 10-K)

## Step 1: Discover the Document

Use **Serper MCP** to search:

```
mcp__serper__google_search:
  q: "{company}" "{document type}" site:sec.gov OR site:investors.{company}.com
  num: "5"
```

**Search Templates:**

| Document | Search Query |
|----------|--------------|
| Earnings release | `"{company}" "fiscal 2025" "fourth quarter results" site:investors.{company}.com` |
| 10-K Annual Report | `"{company}" "10-K" 2024 filetype:pdf site:sec.gov` |
| 10-Q Quarterly | `"{company}" "10-Q" Q3 2024 filetype:pdf site:sec.gov` |
| Merger Agreement | `"{acquirer}" "{target}" "merger agreement" filetype:pdf` |
| Proxy Statement | `"{company}" "DEF 14A" filetype:pdf site:sec.gov` |

**Validate the URL:**
- Prefer `sec.gov` or `.gov` domains
- If PDF URL, use Jina to read it directly
- If HTML filing page, Jina can read that too

## Step 2: Read with Jina

Use **Jina MCP** to read the document content:

```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/.../document.pdf"
```

**Jina can read:**
- PDF files directly (extracts text)
- HTML SEC filings
- Any web page

**If the filing is HTML (like most SEC EDGAR filings):**
```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/.../nke-20250531.htm"
```

## Step 3: Analyze with Schema

Once you have the content, apply the appropriate schema:

**For 10-K filings, extract:**
- Company name, ticker, fiscal year
- Revenue, net income, total assets (with YoY changes)
- Geographic segment breakdown
- Key risk factors

**For Merger Agreements, extract:**
- Acquirer and target names
- Deal value and price per share
- Termination fees
- Key conditions and provisions

**Format the output as a structured report with:**
- Data table with key metrics
- Bullet points for qualitative findings
- Source citation with filing date

## Example: Complete Flow

**User:** "Find Nike's latest financial statement and summarize their China business challenges"

**Think first:** For "challenges in China", the earnings press release + call transcript is better than a 150-page 10-K.

**Step 1 - Search for earnings release:**
```
mcp__serper__google_search:
  q: "Nike" "fiscal 2025" "fourth quarter results" site:investors.nike.com
  num: "5"
```
→ Found investor relations earnings page

**Step 2 - Read the earnings release:**
```
mcp__jina__read_url:
  url: "https://investors.nike.com/.../NIKE-Inc-Reports-Fiscal-2025-Fourth-Quarter-Results"
```
→ Got concise earnings data with Greater China breakdown

**Step 3 - Analyze:**
Extract from the press release:
- Greater China revenue: $6.59B (-13% YoY)
- Greater China EBIT: $1.60B (-31% YoY)
- Management commentary on challenges

**Output:**
```
Nike Greater China - Key Metrics (FY2025)
| Metric   | Value   | Change |
|----------|---------|--------|
| Revenue  | $6.59B  | -13%   |
| EBIT     | $1.60B  | -31%   |

Key Challenges:
1. Traffic declines across digital (-34%) and retail
2. Elevated inventory requiring promotional activity
3. Consumer spending weakness in discretionary categories
4. Competition from local brands (Anta, Li Ning)
5. Strategic franchise reset creating near-term headwinds

Source: Nike FY2025 Earnings Release, July 17, 2025
```

**Note:** If the user specifically asks for the 10-K (not just "financial statement"), then get the 10-K. But for most questions about business performance, the earnings release is more useful.

## Handling Large Documents

SEC 10-K filings can be 100+ pages. When Jina returns a large response:

**Option 1: Use the saved file**
When Jina says "Output has been saved to [path]", read that file with offset/limit:
```
Read:
  file_path: "/path/to/saved/file.txt"
  offset: 1
  limit: 500
```

**Option 2: Search within the investor relations page**
Instead of the full 10-K, read the earnings press release which has key metrics:
```
mcp__jina__read_url:
  url: "https://investors.nike.com/.../fiscal-2025-results"
```

**Option 3: Ask for specific section**
If the user wants "China business", search for the geographic segment section:
- Look for "Greater China" or "Geographic Operating Segments"
- 10-Ks have a standard structure with these sections

**DO NOT** loop through bash grep commands trying to parse large files. Either:
1. Read specific portions of the saved file
2. Use a shorter source (press release, investor page)
3. Tell the user the document is large and ask what section they want

## Error Handling

| Issue | Solution |
|-------|----------|
| No PDF in search results | Search for EDGAR filing page, use Jina on HTML version |
| 403/blocked | Jina typically bypasses these; if blocked, try investor relations URL |
| "exceeds maximum allowed tokens" | Use saved file with offset/limit OR read press release instead |
| Scanned PDF | Inform user OCR not supported in Jina text extraction |

## Fallback: Local Scripts

If Jina is unavailable, use the local extraction scripts:

```bash
# Download
.claude/skills/extraction/scripts/download_pdf.sh "{url}" "{filename}.pdf"

# Extract
python .claude/skills/extraction/scripts/extract_pdf.py temp/{filename}.pdf
```

These scripts are in `.claude/skills/extraction/scripts/`.
