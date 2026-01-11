---
name: ingest-content
description: Low-token document extraction skill. Downloads PDFs via curl and converts to clean Markdown using pypdf/pdfplumber. Use after discover-document returns a validated PDF URL.
---

# Content Extraction Skill

Extract PDF content to clean Markdown without browser overhead.

## Scripts

This skill includes two scripts in the `scripts/` directory:

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `download_pdf.sh` | Download PDFs with browser headers | When you have a URL to download |
| `extract_pdf.py` | Convert PDF to Markdown | After downloading a PDF |

## Quick Reference

### Download a PDF

```bash
.claude/skills/extraction/scripts/download_pdf.sh "https://example.com/doc.pdf" "output_name.pdf"
```

### Extract to Markdown

```bash
python .claude/skills/extraction/scripts/extract_pdf.py temp/document.pdf --output temp/document.md
```

### Full Pipeline

```bash
# 1. Download
.claude/skills/extraction/scripts/download_pdf.sh "https://sec.gov/filing.pdf" "AAPL_10K.pdf"

# 2. Extract
python .claude/skills/extraction/scripts/extract_pdf.py temp/AAPL_10K.pdf --output temp/AAPL_10K.md
```

## Download Script Details

**File:** `scripts/download_pdf.sh`

Downloads PDFs using curl with browser-like headers to avoid basic bot blocking.

```bash
# Usage
./scripts/download_pdf.sh <url> [output_filename]

# Examples
./scripts/download_pdf.sh "https://sec.gov/document.pdf"
./scripts/download_pdf.sh "https://sec.gov/document.pdf" "custom_name.pdf"
```

**Features:**
- Follows redirects (`-L`)
- Browser User-Agent header
- Google referrer header
- PDF validation after download
- Outputs to `temp/` directory by default

## Extraction Script Details

**File:** `scripts/extract_pdf.py`

Converts PDF files to clean Markdown with table extraction.

```bash
# Usage
python scripts/extract_pdf.py <input.pdf> [options]

# Options
--output, -o     Output file path (default: input.md)
--pages          Page range to extract (e.g., "1-10")
--tables-only    Extract only tables, skip body text
--json-tables    Also output tables as JSON
--source-url     Original URL for metadata
```

**Examples:**

```bash
# Basic extraction
python scripts/extract_pdf.py temp/filing.pdf

# Specific pages with JSON tables
python scripts/extract_pdf.py temp/filing.pdf --pages 1-20 --json-tables

# Custom output location
python scripts/extract_pdf.py temp/filing.pdf --output output/report.md
```

## Output Format

Extracted Markdown follows this structure:

```markdown
# Document: filename.pdf

## Metadata
- **Source URL**: https://...
- **Pages**: 45
- **Extracted**: 2024-01-15 10:30:00

---

## Content

[Extracted text with page markers]

--- Page 1 ---

[Page 1 content...]

--- Page 2 ---

[Page 2 content...]

---

## Tables

### Table 1 (Page 5)
| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| HTTP 403 | Bot blocking | Script includes fallback headers automatically |
| HTTP 404 | URL expired | Re-run discovery skill for fresh URL |
| Empty output | Scanned PDF | Inform user; OCR not currently supported |
| Encoding error | Non-UTF8 | Script handles with `errors='ignore'` |

## Dependencies

Requires Python packages (install via `pip install -r requirements.txt`):

- `pypdf` — Text extraction
- `pdfplumber` — Table extraction

## Integration

After extraction, the Markdown file is ready for the `generate-report` skill:

```
discover-document → [URL] → ingest-content → [temp/*.md] → generate-report
```
