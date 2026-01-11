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

# Research Pipeline

Orchestrate discovery, extraction, and analysis using cost-effective sub-agents.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     RESEARCH FLOW (Opus)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ROUTE          2. DELEGATE           3. ANALYZE              │
│  ┌──────────┐      ┌──────────┐         ┌──────────┐            │
│  │ Classify │─────▶│ Spawn    │────────▶│ Apply    │            │
│  │ request  │      │ agents   │         │ schema   │            │
│  └──────────┘      └──────────┘         └──────────┘            │
│       │                 │                    │                   │
│       │           ┌─────┴─────┐              │                   │
│       │           ▼           ▼              │                   │
│       │     ┌─────────┐ ┌─────────┐          │                   │
│       │     │discover │ │extract  │          │                   │
│       │     │(Haiku)  │ │(Haiku)  │          │                   │
│       │     └─────────┘ └─────────┘          │                   │
│       │           │           │              │                   │
│       └───────────┴───────────┴──────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Step 1: Route the Request

Classify what the user wants:

| Intent | Discovery Type | Signals |
|--------|----------------|---------|
| Financial docs | `financial` | "10-K", "filing", "SEC", "annual report", "merger" |
| News/current | `news` | "news", "media", "latest", "coverage", "saying about" |

## Step 2: Spawn Discovery Agent (Haiku)

**Use the Task tool** to spawn the discover agent:

```
Task:
  subagent_type: general-purpose
  model: haiku
  prompt: |
    Search for {financial|news} documents.

    Query: {user's topic}
    Type: {financial|news}

    For financial: Use Serper, search site:sec.gov, return max 3 URLs
    For news: Use Jina search, filter by source tier, return max 5 URLs

    Return URLs only in this format:
    DISCOVERY COMPLETE
    URLs:
    1. {url} | {source} | {title}
    ...
```

**Limits:** 5 URLs for news, 3 URLs for financial (quality over quantity)

## Step 3: Spawn Extraction Agent (Haiku)

**Use the Task tool** to spawn the extract agent:

```
Task:
  subagent_type: general-purpose
  model: haiku
  prompt: |
    Read these URLs and extract content:

    URLs:
    - {url1}
    - {url2}

    ALWAYS use mcp__jina__parallel_read_url (faster, handles failures).
    Truncate each source to 3000 words max.

    Return raw content in this format:
    EXTRACTION COMPLETE
    Source: {url}
    ---CONTENT START---
    {content}
    ---CONTENT END---
```

**Performance:** Always use parallel_read_url, even for 2 URLs. Only use single read_url for exactly 1 URL.

## Step 4: Analyze (Opus)

With content returned from agents, apply the appropriate schema:

| Content Type | Schema |
|--------------|--------|
| SEC Filing | 10-K, M&A, or Proxy schema |
| News | News Summary, Claims Analysis, Stakeholder Positions, Timeline, or Predictions |

See `.claude/skills/analysis/SKILL.md` for schema details.

---

## Complete Example

**User:** "What are Chinese media saying about Tesla? Save to output/"

### Step 1: Route
- Contains "media saying" → **news**
- Chinese sources requested

### Step 2: Spawn Discovery Agent

```
Task:
  subagent_type: general-purpose
  model: haiku
  description: "Search Chinese media for Tesla"
  prompt: |
    Search for news about Tesla from Chinese media sources.

    Use mcp__jina__search_web with:
    - English Chinese sources: site:scmp.com OR site:caixinglobal.com OR site:globaltimes.cn
    - Chinese language: site:caixin.com OR site:36kr.com (with hl: "zh-cn")

    Return top 5 URLs (max) in format:
    DISCOVERY COMPLETE
    URLs:
    1. {url} | {source} | {title}
```

### Step 3: Spawn Extraction Agent

```
Task:
  subagent_type: general-purpose
  model: haiku
  description: "Extract Tesla articles"
  prompt: |
    Read these URLs using mcp__jina__parallel_read_url:
    - https://scmp.com/...
    - https://globaltimes.cn/...
    - https://caixin.com/...

    Truncate to 3000 words per source.
    Return raw content for each source.
```

### Step 4: Analyze (Opus does this)
- Apply News Summary or Stakeholder Positions schema
- Synthesize across sources
- Write report to `output/tesla_chinese_media_analysis.md`

---

## Agent Reference

| Agent | Model | Purpose | Tools |
|-------|-------|---------|-------|
| `discover` | Haiku | Find URLs | Jina search, Serper |
| `extract` | Haiku | Read content | Jina read_url |
| Main flow | Opus | Route, analyze, write | All |

Agent definitions: `.claude/agents/`

---

## When to Use Agents vs Direct

| Scenario | Approach |
|----------|----------|
| Multi-source research | Spawn agents (cost-effective) |
| Single quick lookup | Direct call (faster) |
| Complex analysis | Opus direct |
| Bulk URL reading | Extract agent |

---

## Output Options

| User Request | Action |
|--------------|--------|
| *(default)* | Output to chat |
| "Save the report" | Write to `output/{topic}_report.md` |
| "Save as JSON" | Write to `output/{topic}_report.json` |

---

## Error Handling

| Issue | Solution |
|-------|----------|
| Agent timeout | Retry with fewer URLs |
| No results | Broaden search terms |
| Content too long | Agent truncates, Opus summarizes |
| Parallel read fails | Fall back to sequential |

---

## Best Practices

1. **Delegate search/read to Haiku** — saves tokens
2. **Keep Opus for reasoning** — analysis, synthesis, writing
3. **Limit URLs** — 5 for news, 3 for financial (quality > quantity)
4. **Always parallel read** — faster, handles failures gracefully
5. **Truncate early** — 3000 words per source is plenty for analysis
6. **Be specific in prompts** — agents work better with clear instructions
