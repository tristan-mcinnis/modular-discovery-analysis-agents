---
name: ingest-content
description: >
  Extract content from PDFs and web pages. PRIMARY METHOD: Use Jina MCP read_url
  which handles PDFs, HTML, and bypasses most blocking. FALLBACK: Local scripts
  for offline use. Use as Step 2 of research-flow after discovering a document URL.
---

# Content Extraction

Extract text from PDFs and web pages for analysis.

## Primary Method: Jina MCP

**Use Jina for all document reading** — it handles PDFs, HTML, and bypasses blocking.

```
mcp__jina__read_url:
  url: "https://www.sec.gov/Archives/edgar/data/.../document.pdf"
```

### Jina Capabilities

| Content Type | Support |
|--------------|---------|
| PDF files | ✅ Extracts text directly |
| HTML pages | ✅ Converts to clean Markdown |
| SEC EDGAR filings | ✅ Works with .htm and .pdf |
| Blocked by 403 | ✅ Usually bypasses |

### Examples

**Read a PDF:**
```
mcp__jina__read_url:
  url: "https://www.sec.gov/.../nke-20250531.pdf"
```

**Read an HTML filing:**
```
mcp__jina__read_url:
  url: "https://www.sec.gov/.../nke-20250531.htm"
```

**Read investor relations page:**
```
mcp__jina__read_url:
  url: "https://investors.nike.com/.../fiscal-2025-results"
```

## Fallback: Local Scripts

If Jina MCP is unavailable, use the local extraction scripts.

### Download Script

```bash
.claude/skills/extraction/scripts/download_pdf.sh "{url}" "{filename}.pdf"
```

- Downloads to `temp/` directory
- Includes browser-like headers
- Validates PDF format (rejects HTML error pages)

### Extraction Script

```bash
python .claude/skills/extraction/scripts/extract_pdf.py temp/{filename}.pdf --output temp/{filename}.md
```

**Options:**
- `--output, -o`: Output file path
- `--pages`: Page range (e.g., `1-50`)
- `--source-url`: Original URL for metadata

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

# 3. Read the result
# Content is now in temp/company_10k.md
```

## When to Use Each Method

| Situation | Method |
|-----------|--------|
| Normal operation | Jina MCP (primary) |
| Jina MCP unavailable | Local scripts (fallback) |
| Need to save PDF locally | Local scripts |
| Offline/air-gapped | Local scripts |

## Error Handling

| Error | Solution |
|-------|----------|
| Jina returns truncated content | Large doc; read specific sections |
| 403 from SEC with curl | Use Jina instead (usually works) |
| Invalid PDF header | URL returned HTML; try different URL or use Jina on HTML version |
| Empty content | Scanned PDF; OCR not supported |

## Dependencies

**For local scripts only:**
```bash
pip install pypdf pdfplumber  # pdfplumber optional for tables
```
