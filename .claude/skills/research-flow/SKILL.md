---
name: research-flow
description: Orchestrate the complete document research pipeline. Coordinates discover-document, ingest-content, and generate-report skills for end-to-end research tasks.
---

# Research Flow Skill

Run the complete discover → extract → analyze pipeline.

## When to Use

Use this skill for end-to-end research requests like:

- "Find and analyze the Apple 10-K"
- "Get the Microsoft-Activision merger agreement and extract the key terms"
- "Research Tesla's latest proxy statement"

## Pipeline Overview

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ discover-document│────▶│  ingest-content  │────▶│  generate-report │
│                  │     │                  │     │                  │
│ Serper search    │     │ curl + pypdf     │     │ Schema analysis  │
│ → Verified URL   │     │ → temp/*.md      │     │ → output/*.json  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

## Execution Steps

### Step 1: Discovery

Use `discover-document` skill:

```
Search: "{company}" "{document type}" filetype:pdf site:sec.gov
Output: Verified PDF URL
```

### Step 2: Extraction

Use `ingest-content` skill:

```bash
# Download
.claude/skills/extraction/scripts/download_pdf.sh "{url}" "{filename}.pdf"

# Extract
python .claude/skills/extraction/scripts/extract_pdf.py temp/{filename}.pdf --output temp/{filename}.md
```

### Step 3: Analysis

Use `generate-report` skill:

```
Input: temp/{filename}.md
Schema: [auto-detect or specify]
Output: output/{filename}_report.json, output/{filename}_report.md
```

## Example Flow

**User:** "Find and analyze the Adobe-Figma merger agreement"

**Step 1 - Discovery:**
```
Query: "Adobe" "Figma" "merger agreement" filetype:pdf site:sec.gov
Result: https://sec.gov/Archives/.../ex21.pdf (confidence: high)
```

**Step 2 - Extraction:**
```bash
.claude/skills/extraction/scripts/download_pdf.sh "https://sec.gov/..." "ADBE_FIGM_merger.pdf"
python .claude/skills/extraction/scripts/extract_pdf.py temp/ADBE_FIGM_merger.pdf --output temp/ADBE_FIGM_merger.md
```

**Step 3 - Analysis:**
```
Schema: M&A Deal Analysis
Output: output/ADBE_FIGM_merger_report.json
```

**Return to user:** Summary + link to full report

## User Checkpoints

Pause and ask the user when:

| Situation | Question |
|-----------|----------|
| Multiple search results | "Found 3 documents. Which should I analyze?" |
| Low confidence URL | "This isn't from a trusted domain. Proceed?" |
| Unknown document type | "Is this a 10-K, merger agreement, or other?" |

## Error Recovery

| Phase | Error | Recovery |
|-------|-------|----------|
| Discovery | No results | Broaden search, remove filters |
| Extraction | 403 Forbidden | Fallback headers already applied |
| Extraction | Empty content | Report to user (may be scanned) |
| Analysis | Schema mismatch | Ask user to specify document type |

## File Locations

After a research flow completes:

```
temp/
├── {name}.pdf           # Original document
├── {name}.md            # Extracted text
└── {name}_tables.json   # Tables (if any)

output/
├── {name}_report.json   # Structured data
└── {name}_report.md     # Human-readable report
```
