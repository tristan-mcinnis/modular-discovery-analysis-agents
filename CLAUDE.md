# MDAA - Modular Discovery & Analysis Agent

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MAIN AGENT (Opus)                            │
│                   Route → Delegate → Analyze                     │
├─────────────────────────────────────────────────────────────────┤
│                            │                                     │
│                    ┌───────┴───────┐                             │
│                    ▼               ▼                             │
│              ┌──────────┐   ┌──────────┐                         │
│              │ discover │   │ extract  │                         │
│              │ (Haiku)  │   │ (Haiku)  │                         │
│              └──────────┘   └──────────┘                         │
│                    │               │                             │
│                    └───────┬───────┘                             │
│                            ▼                                     │
│                    ┌──────────────┐                              │
│                    │   ANALYZE    │  ← Opus applies schemas      │
│                    └──────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

## Cost-Effective Agent Strategy

| Task | Agent | Model | Why |
|------|-------|-------|-----|
| Search/Discovery | `discover` | Haiku | Simple queries, no reasoning needed |
| URL Reading | `extract` | Haiku | Just extraction, no analysis |
| Analysis/Writing | Main | Opus | Complex reasoning, synthesis |

---

## When to Spawn Agents

**Spawn Haiku agents for:**
- Multi-source news research
- Bulk URL reading
- Any search task

**Keep in Opus for:**
- Single quick lookup (faster than spawning)
- Analysis and synthesis
- Report writing

---

## Agent Usage

### Spawn Discovery Agent

```
Task:
  subagent_type: general-purpose
  model: haiku
  description: "Search for {topic}"
  prompt: |
    Search for {financial|news} about {topic}.

    Financial: Use mcp__serper__google_search, site:sec.gov
    News: Use mcp__jina__search_web, filter by tier

    Return URLs only:
    1. {url} | {source} | {title}
```

### Spawn Extraction Agent

```
Task:
  subagent_type: general-purpose
  model: haiku
  description: "Read {count} URLs"
  prompt: |
    Read these URLs using mcp__jina__read_url:
    - {url1}
    - {url2}

    Return raw content for each.
```

---

## Request Routing

| User Says | Route To | Agent |
|-----------|----------|-------|
| "10-K", "SEC", "filing" | Financial discovery | Haiku |
| "news", "media", "latest" | News discovery | Haiku |
| "Chinese sources", "Japanese" | News + language filter | Haiku |
| "analyze", "summarize" | Schema application | Opus |

---

## Skills Reference

```
.claude/
├── agents/
│   ├── discover.md      # Haiku - search tasks
│   └── extract.md       # Haiku - read URLs
└── skills/
    ├── research-flow/   # Main orchestrator
    ├── discover-financial/
    ├── discover-news/
    ├── extraction/
    └── analysis/
        └── schemas/     # News Summary, Claims, Timeline, etc.
```

---

## Analysis Schemas

| Question | Schema |
|----------|--------|
| "Summarize" | News Summary |
| "Is this true?" | Claims Analysis |
| "Perspectives?" | Stakeholder Positions |
| "How did it unfold?" | Timeline Narrative |
| "Outlook?" | Predictions |
| "Financials?" | 10-K / M&A / Proxy |

---

## Output Options

| Request | Action |
|---------|--------|
| *(default)* | Chat output |
| "Save the report" | `output/{topic}_report.md` |
| "Save as JSON" | `output/{topic}_report.json` |

---

## Example Flow

**User:** "What are Chinese media saying about Tesla? Save to output/"

1. **Route:** "media saying" → news discovery
2. **Spawn discover agent (Haiku):**
   - Search SCMP, Caixin, Global Times
   - Return 5-8 URLs
3. **Spawn extract agent (Haiku):**
   - Read each URL
   - Return raw content
4. **Analyze (Opus):**
   - Apply Stakeholder Positions schema
   - Synthesize themes across sources
5. **Write:** `output/tesla_chinese_media_analysis.md`

---

## DO NOT

- Use Opus for simple searches (waste of tokens)
- Skip schema application (always structure output)
- Use single source for controversial topics
- Guess at data (cite or say "not found")
