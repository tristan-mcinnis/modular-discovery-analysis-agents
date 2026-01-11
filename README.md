# Modular Discovery & Analysis Agent (MDAA)

A Claude Code skills-based deep research system. MDAA finds documents and news, extracts content, and generates structured analysis reports using Fabric-inspired schemas.

## What Does This Do?

MDAA automates deep research across two domains:

### Financial Documents
- SEC filings (10-K, 10-Q, 8-K, DEF 14A, S-1)
- Merger agreements, proxy statements
- Earnings releases, investor presentations

### News & Current Events
- Multi-language sources (English, Chinese, Japanese, Korean)
- Source quality filtering (Tier 1/2/3)
- Multiple perspectives on controversial topics

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        RESEARCH FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  DISCOVER    │───▶│   EXTRACT    │───▶│   ANALYZE    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│    ┌────┴────┐              │            ┌──────┴──────┐         │
│    │         │              │            │             │         │
│ Financial  News         Jina MCP     Financial    News          │
│  (SEC)   (Multi-lang)    read_url    Schemas    Schemas         │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Claude Code** installed and configured
- **Jina MCP** server connected (primary extraction)
- **Serper MCP** server connected (financial document search)
- **Python 3.8+** (for fallback scripts only)

## Installation

### 1. Install Python Dependencies (Optional)

Only needed for fallback local extraction:

```bash
pip install -r requirements.txt
```

### 2. Verify MCP Servers

Check your Claude Code MCP configuration for:
- `jina` — Primary search and extraction
- `serper` — Financial document search

### 3. Ready to Use

The skills are automatically available. Just ask Claude to research something.

## Usage Examples

### Financial Research

```
Find Apple's latest 10-K and summarize their services segment
```

```
Get the Microsoft-Activision merger agreement and extract deal terms
```

```
What does Nike's proxy statement say about CEO compensation?
```

### News Research

```
What are Chinese and Western media saying about the new EV tariffs?
```

```
Find coverage of the Fed rate decision from Reuters and Bloomberg
```

```
Search Japanese sources for news about Toyota's EV strategy
```

### Analysis Types

```
Is it true that Apple is moving production out of China? Fact-check this.
```

```
How did the FTX collapse unfold? Give me a timeline.
```

```
What are analysts predicting for AI chip demand in 2025?
```

## Output Options

MDAA supports flexible output:

| Request | Behavior |
|---------|----------|
| *(default)* | Output directly to chat |
| "Save the report" | Writes to `output/{topic}_report.md` |
| "Save as JSON" | Writes to `output/{topic}_report.json` |
| "Save to output/" | Writes to `output/` directory |

### Examples

```
Find Nike's 10-K and save the report to output/
```

```
Analyze the Tesla news and save as JSON
```

## Project Structure

```
modular-discovery-analysis-agents/
├── .claude/skills/
│   ├── research-flow/SKILL.md        # Pipeline orchestrator
│   ├── discover-financial/SKILL.md   # SEC filings, financial docs
│   ├── discover-news/SKILL.md        # News with source/language filters
│   ├── extraction/SKILL.md           # Jina-first content extraction
│   └── analysis/
│       ├── SKILL.md                  # Schema selector
│       └── schemas/
│           ├── news-summary.md       # Article wisdom extraction
│           ├── claims-analysis.md    # Fact-checking (A-F ratings)
│           ├── stakeholder-positions.md  # Multi-perspective analysis
│           ├── timeline-narrative.md # Chronological + causal
│           └── predictions.md        # Future outlook extraction
├── temp/                             # Intermediate files
├── output/                           # Generated reports
├── CLAUDE.md                         # Agent instructions
└── README.md
```

## Skills Reference

### discover-financial

Finds official financial documents via Serper MCP.

- Prioritizes `sec.gov` and official IR sites
- Supports 10-K, 10-Q, 8-K, DEF 14A, S-1, 20-F
- Returns verified URLs for extraction

### discover-news

Finds news articles with language and source filtering.

**Source Tiers:**
| Tier | Sources |
|------|---------|
| Tier 1 | reuters.com, bloomberg.com, ft.com, caixinglobal.com, scmp.com, nikkei.com |
| Tier 2 | theguardian.com, bbc.com, cnbc.com, globaltimes.cn |
| Tier 3 | General web (use with caution) |

**Language Support:**
| Language | Example Sources |
|----------|-----------------|
| Chinese | caixin.com, 36kr.com, sina.com.cn |
| Japanese | nikkei.com, nhk.or.jp, asahi.com |
| Korean | chosun.com, koreaherald.com |

### extraction

Extracts content using Jina MCP (primary) or local scripts (fallback).

- Handles PDFs, HTML, and most paywalls
- Supports parallel extraction for multiple sources
- Falls back to local pypdf for offline use

### analysis

Applies structured schemas to extracted content.

**Financial Schemas:**
- 10-K — Revenue, segments, risks, key metrics
- M&A — Deal value, terms, conditions
- Proxy — Executive comp, board, proposals

**News/Research Schemas:**
- News Summary — Key developments, quotes, facts
- Claims Analysis — Evidence for/against, A-F rating
- Stakeholder Positions — Multi-perspective with agreements/disagreements
- Timeline Narrative — Chronological events with causal analysis
- Predictions — Forecasts with confidence levels

## Analysis Schema Selection

| Question Type | Schema |
|---------------|--------|
| "Summarize the financials" | 10-K |
| "What are the deal terms?" | M&A |
| "Summarize this article" | News Summary |
| "Is this claim true?" | Claims Analysis |
| "What are the perspectives?" | Stakeholder Positions |
| "How did this unfold?" | Timeline Narrative |
| "What's the outlook?" | Predictions |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No search results | Broaden query, try different terms |
| 403 when reading | Jina usually bypasses; try HTML instead of PDF |
| Content too long | Ask for specific section or use shorter source |
| Empty extraction | May be scanned PDF; OCR not supported |
| Conflicting info | Use Stakeholder Positions schema |

## Extending MDAA

### Add a New Analysis Schema

1. Create `.claude/skills/analysis/schemas/your-schema.md`
2. Add entry to `.claude/skills/analysis/SKILL.md` schema table
3. Add trigger phrases to `CLAUDE.md`

### Add Trusted News Sources

Edit `.claude/skills/discover-news/SKILL.md` and update the source tiers.

### Add Financial Document Types

Edit `.claude/skills/discover-financial/SKILL.md` and add search templates.

## Design Principles

- **Jina-first extraction** — Handles PDFs, HTML, and bypasses blocking
- **Source quality tiers** — Prioritize credible sources
- **Multi-perspective** — Get both sides of controversial topics
- **Structured output** — Fabric-inspired analysis schemas
- **Flexible output** — Chat, Markdown files, or JSON

## Credits

Analysis schemas inspired by [Fabric](https://github.com/danielmiessler/Fabric) patterns:
- `extract_article_wisdom`
- `analyze_claims`
- `analyze_debate`
- `extract_predictions`

## Resources

- [Claude Code Skills](https://docs.anthropic.com/claude-code)
- [Jina AI](https://jina.ai)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Fabric Patterns](https://github.com/danielmiessler/Fabric)
