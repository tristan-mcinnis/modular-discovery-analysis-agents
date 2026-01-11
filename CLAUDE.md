# MDAA Project Instructions

## Overview

This project implements a three-skill loop for document research:

1. **discover-document** — Find PDFs via Serper MCP
2. **ingest-content** — Extract PDF content to Markdown
3. **generate-report** — Analyze using predefined schemas

## Skill Locations

```
.claude/skills/
├── discovery/SKILL.md
├── extraction/
│   ├── SKILL.md
│   └── scripts/
│       ├── download_pdf.sh
│       └── extract_pdf.py
├── analysis/SKILL.md
└── research-flow/SKILL.md
```

## Quick Commands

### Download a PDF

```bash
.claude/skills/extraction/scripts/download_pdf.sh "https://url.pdf" "filename.pdf"
```

### Extract to Markdown

```bash
python .claude/skills/extraction/scripts/extract_pdf.py temp/file.pdf --output temp/file.md
```

## Key Design Decisions

- Use curl for downloads (no browser automation)
- Search with `filetype:pdf` for direct links
- Prioritize sec.gov and .gov domains
- Schema-driven analysis for consistent output

## File Locations

- `temp/` — Downloaded PDFs and extracted Markdown
- `output/` — Generated reports (JSON and Markdown)
