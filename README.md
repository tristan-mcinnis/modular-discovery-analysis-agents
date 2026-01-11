# Modular Discovery & Analysis Agent (MDAA)

A Claude Code skills-based system for autonomous financial and legal document research. MDAA finds documents, extracts their content, and generates structured analysis reports — all without heavy browser automation.

## What Does This Do?

MDAA automates the tedious process of:

1. **Finding** official documents (SEC filings, merger agreements, annual reports)
2. **Downloading** and extracting text from PDFs
3. **Analyzing** the content and producing structured reports

Instead of manually searching SEC.gov, downloading PDFs, and reading through hundreds of pages, you simply ask Claude:

> "Find and analyze the Microsoft 10-K filing for 2024"

And MDAA handles the rest.

## How It Works

MDAA uses a **three-skill loop**:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Discovery     │────▶│   Extraction    │────▶│    Analysis     │
│                 │     │                 │     │                 │
│ Serper search   │     │ curl + pypdf    │     │ Schema-based    │
│ → Verified URL  │     │ → Markdown      │     │ → JSON report   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Prerequisites

- **Claude Code** installed and configured
- **Serper MCP** server connected (for web search)
- **Python 3.8+** installed

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Serper MCP

The discovery skill requires Serper MCP for web search. Check your Claude Code MCP configuration.

### 3. Ready to Use

The skills are automatically available. Just ask Claude to research a document.

## Usage Examples

### Find and Analyze a 10-K

```
Find and analyze the Apple 10-K for 2024
```

### Research a Merger Agreement

```
Find the Microsoft-Activision merger agreement and extract the key terms
```

### Get a Proxy Statement

```
Get Amazon's 2024 proxy statement and summarize executive compensation
```

## Project Structure

```
modular-discovery-analysis-agents/
├── .claude/skills/
│   ├── discovery/
│   │   └── SKILL.md              # Document search via Serper
│   ├── extraction/
│   │   ├── SKILL.md              # PDF download and extraction
│   │   └── scripts/
│   │       ├── download_pdf.sh   # curl wrapper with headers
│   │       └── extract_pdf.py    # PDF to Markdown converter
│   ├── analysis/
│   │   └── SKILL.md              # Schema-based report generation
│   └── research-flow/
│       └── SKILL.md              # Pipeline orchestration
├── temp/                         # Downloaded PDFs and extracted text
├── output/                       # Generated reports
├── requirements.txt
└── README.md
```

## The Four Skills

### discover-document

Finds official PDFs using Serper MCP search.

- Prioritizes trusted domains (sec.gov, .gov, IR sites)
- Uses `filetype:pdf` for direct links
- Returns confidence-scored URLs

### ingest-content

Downloads and extracts PDF content.

**Scripts included:**
- `scripts/download_pdf.sh` — Downloads with browser headers
- `scripts/extract_pdf.py` — Converts PDF to Markdown

### generate-report

Analyzes content using predefined schemas:

- **M&A Deal** — Deal value, termination fees, provisions
- **10-K** — Revenue, risks, segments
- **Proxy Statement** — Compensation, board, proposals

### research-flow

Orchestrates all three skills for end-to-end research.

## Output Examples

### JSON Report

```json
{
  "metadata": {
    "document": "MSFT_ATVI_merger.pdf",
    "type": "merger_agreement",
    "confidence": "high"
  },
  "data": {
    "deal_summary": {
      "acquirer": "Microsoft Corporation",
      "target": "Activision Blizzard, Inc.",
      "deal_value": 68700000000
    },
    "key_provisions": {
      "termination_fee_target": 2270000000,
      "governing_law": "Delaware"
    }
  }
}
```

### Markdown Report

```markdown
# Analysis: Microsoft-Activision Merger

## Summary
Microsoft to acquire Activision Blizzard for $68.7B in all-cash deal.

## Key Metrics
| Metric | Value | Page |
|--------|-------|------|
| Deal Value | $68.7B | 3 |
| Termination Fee | $2.27B | 67 |
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No search results | Broaden query, remove year |
| 403 when downloading | Fallback headers auto-applied |
| Empty PDF extraction | May be scanned; OCR not supported |
| Wrong schema applied | Specify document type in request |

## Extending MDAA

### Add a New Schema

Edit `.claude/skills/analysis/SKILL.md` and add your schema under "Available Schemas".

### Add Trusted Domains

Edit `.claude/skills/discovery/SKILL.md` and update the domain list.

## Design Principles

- **No browser automation** — Direct downloads via curl
- **Trusted sources** — Prioritize official domains
- **Structured output** — Schema-driven analysis
- **Modular skills** — Each skill does one thing well

## Resources

- [Anthropic Agent Skills](https://github.com/anthropics/skills)
- [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch)
- [Serper API](https://serper.dev)
