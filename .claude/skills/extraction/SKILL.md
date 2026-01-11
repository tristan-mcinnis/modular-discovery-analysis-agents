---
name: extraction
description: >
  Extract content from PDFs and web pages. PRIMARY METHOD: Use Jina MCP read_url
  which handles PDFs, HTML, and bypasses most blocking. FALLBACK: Local scripts
  for offline use. Use as Step 2 of research-flow after discovering a document URL.
---

# Content Extraction

Extract text from PDFs, web pages, and documents for analysis.

## Primary Method: Jina MCP

**Always use Jina first** — it handles PDFs, HTML, bypasses blocking, and works with most sources.

### Single URL
```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/.../document.pdf"
```

### Multiple URLs (Parallel)
```
mcp__jina__parallel_read_url:
  urls:
    - url: "https://reuters.com/..."
    - url: "https://scmp.com/..."
    - url: "https://ft.com/..."
```

## Jina Capabilities

| Content Type | Support | Notes |
|--------------|---------|-------|
| PDF files | ✅ | Extracts text directly |
| HTML pages | ✅ | Converts to clean Markdown |
| SEC EDGAR (.htm) | ✅ | Works with filing pages |
| News articles | ✅ | Bypasses most paywalls |
| Blocked by 403 | ✅ | Usually bypasses |
| Scanned PDFs | ❌ | No OCR support |

## Examples

### Read SEC Filing (HTML)
```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/320187/000032018725000047/nke-20250531.htm"
```

### Read SEC Filing (PDF)
```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/320187/000032018725000047/nke-20250531.pdf"
```

### Read News Article
```
mcp__jina__read_url:
  url: "https://www.reuters.com/business/..."
```

### Read Investor Relations Page
```
mcp__jina__read_url:
  url: "https://investors.nike.com/investors/news-events-and-reports/"
```

### Read Multiple Sources (News Research)
```
mcp__jina__parallel_read_url:
  urls:
    - url: "https://www.reuters.com/..."
    - url: "https://www.ft.com/..."
    - url: "https://www.scmp.com/..."
  timeout: 30000
```

## Advanced Options

### Extract All Links
```
mcp__jina__read_url:
  url: "https://example.com"
  withAllLinks: true
```

### Extract All Images
```
mcp__jina__read_url:
  url: "https://example.com"
  withAllImages: true
```

## Handling Large Documents

When Jina returns truncated or very large content:

### Option 1: Focus on Specific Sections
For 10-K filings, search within the returned content for specific sections:
- "Greater China" or "Geographic Operating Segments"
- "Risk Factors"
- "Management's Discussion and Analysis"

### Option 2: Use Shorter Source
Instead of full 10-K (150+ pages), use:
- Earnings press release (2-5 pages)
- Investor presentation (key slides)
- 8-K filing (specific event)

### Option 3: Ask User
"The document is very large. Which section should I focus on?"

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "exceeds maximum tokens" | Doc too large | Focus on specific section or use shorter source |
| 403 Forbidden | Blocked | Jina usually bypasses; try HTML instead of PDF |
| Empty content | Scanned PDF | Inform user OCR not supported |
| Timeout | Slow server | Increase timeout or try alternative URL |
| Redirect | URL changed | Follow the redirect URL provided |

## Fallback: Local Scripts

If Jina MCP is unavailable, use local extraction:

### Download PDF
```bash
.claude/skills/extraction/scripts/download_pdf.sh "{url}" "{filename}.pdf"
```

### Extract Text
```bash
python .claude/skills/extraction/scripts/extract_pdf.py temp/{filename}.pdf --output temp/{filename}.md
```

### Full Local Pipeline
```bash
# 1. Download
.claude/skills/extraction/scripts/download_pdf.sh \
  "https://www.sec.gov/.../document.pdf" \
  "company_10k.pdf"

# 2. Extract
python .claude/skills/extraction/scripts/extract_pdf.py \
  temp/company_10k.pdf \
  --output temp/company_10k.md

# 3. Read result
# Content is now in temp/company_10k.md
```

## When to Use Each Method

| Situation | Method |
|-----------|--------|
| Normal operation | Jina MCP |
| Multiple sources | `parallel_read_url` |
| Jina unavailable | Local scripts |
| Need PDF saved locally | Local scripts |
| Offline/air-gapped | Local scripts |

## Dependencies (Local Scripts Only)

```bash
pip install pypdf pdfplumber  # pdfplumber optional for tables
```

## Next Step

After extraction, pass content to the **Analysis** skill:
- Select appropriate schema (10-K, M&A, News Summary, etc.)
- Extract structured data
- Generate report
