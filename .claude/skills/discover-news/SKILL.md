---
name: discover-news
description: >
  Search for news articles with language, source quality, and regional filtering.
  Use when researching current events, market news, policy changes, or any topic
  requiring recent journalism. Supports Chinese, Japanese, Korean, and English sources
  with tiered quality filtering. Returns URLs ready for Jina extraction.
---

# News Discovery

Find high-quality news articles with language and source filtering.

## Required Tool

**Use Jina Search** (`mcp__jina__search_web`) as primary, with Serper as fallback:

```
mcp__jina__search_web:
  query: "{topic} {filters}"
  num: 10
```

## Source Quality Tiers

### Tier 1: Premium Sources (Highest credibility)

| Region | Sources |
|--------|---------|
| **Global** | `reuters.com`, `bloomberg.com`, `ft.com`, `wsj.com`, `economist.com`, `nytimes.com` |
| **China** | `caixinglobal.com`, `scmp.com`, `yicaiglobal.com`, `chinadaily.com.cn` |
| **Japan** | `nikkei.com`, `japantimes.co.jp`, `nhk.or.jp` |
| **Korea** | `koreaherald.com`, `koreatimes.co.kr` |
| **Tech** | `techcrunch.com`, `theverge.com`, `arstechnica.com`, `wired.com` |

### Tier 2: Quality Sources (Good credibility)

| Region | Sources |
|--------|---------|
| **Global** | `theguardian.com`, `bbc.com`, `cnn.com`, `apnews.com` |
| **China** | `globaltimes.cn`, `sixthtone.com`, `radii.co` |
| **Finance** | `seekingalpha.com`, `marketwatch.com`, `cnbc.com` |

### Tier 3: General Web (Use with caution)
No site filter - broader search but requires more verification.

## Language Filters

### Chinese (Mandarin) Sources
```
# Chinese-language business/finance
site:caixin.com OR site:36kr.com OR site:sina.com.cn OR site:163.com

# Search query example
mcp__jina__search_web:
  query: "{topic} site:caixin.com OR site:36kr.com"
  hl: "zh-cn"
```

### Japanese Sources
```
site:nikkei.com OR site:nhk.or.jp OR site:asahi.com OR site:yomiuri.co.jp
```

### Korean Sources
```
site:chosun.com OR site:donga.com OR site:hani.co.kr
```

### English (Default)
No language filter needed.

## Search Templates

### By Topic Type

| Topic | Search Template |
|-------|-----------------|
| **Company News** | `"{company}" news {year}` |
| **Policy/Regulation** | `"{policy}" regulation announcement` |
| **Market Trends** | `"{industry}" market trend analysis {year}` |
| **Geopolitical** | `"{country}" "{topic}" policy` |
| **Executive/Personnel** | `"{company}" CEO executive appointment` |

### By Region Focus

| Region | Search Template |
|--------|-----------------|
| **China Business** | `"{topic}" site:caixinglobal.com OR site:scmp.com` |
| **China (Chinese)** | `"{topic}" site:caixin.com OR site:36kr.com` |
| **Japan** | `"{topic}" site:nikkei.com OR site:japantimes.co.jp` |
| **US** | `"{topic}" site:wsj.com OR site:bloomberg.com` |
| **Global** | `"{topic}" site:reuters.com OR site:ft.com` |

## Time Filters

Use Jina's `tbs` parameter or include date in query:

| Filter | Jina Parameter | Alternative |
|--------|----------------|-------------|
| Past 24 hours | `tbs: "qdr:d"` | `"{topic}" 2025` |
| Past week | `tbs: "qdr:w"` | Include recent date |
| Past month | `tbs: "qdr:m"` | `"{topic}" January 2025` |
| Past year | `tbs: "qdr:y"` | `"{topic}" 2025` |

## Example Searches

### Example 1: China EV Market (English, Tier 1)
```
mcp__jina__search_web:
  query: "China electric vehicle market 2025 site:caixinglobal.com OR site:scmp.com OR site:reuters.com"
  num: 10
```

### Example 2: China Tech (Chinese sources)
```
mcp__jina__search_web:
  query: "人工智能 监管 site:caixin.com OR site:36kr.com"
  num: 10
  hl: "zh-cn"
```

### Example 3: Japan Monetary Policy
```
mcp__jina__search_web:
  query: "Bank of Japan interest rate site:nikkei.com OR site:reuters.com"
  num: 10
  tbs: "qdr:w"
```

### Example 4: US-China Trade (Multiple perspectives)
```
# Run both searches for balanced view:

# Western perspective
mcp__jina__search_web:
  query: "US China tariffs 2025 site:ft.com OR site:bloomberg.com"

# Chinese perspective
mcp__jina__search_web:
  query: "US China tariffs 2025 site:scmp.com OR site:caixinglobal.com"
```

## Output Format

Return discovered articles for extraction:

```
Found 5 articles on "{topic}":

1. [Tier 1] Caixin Global - "Title of Article"
   URL: https://www.caixinglobal.com/...
   Date: 2025-01-10

2. [Tier 1] Reuters - "Title of Article"
   URL: https://www.reuters.com/...
   Date: 2025-01-09

3. [Tier 2] CNBC - "Title of Article"
   URL: https://www.cnbc.com/...
   Date: 2025-01-08
```

## Next Step

Pass URLs to **Jina MCP** for reading:

```
mcp__jina__read_url:
  url: "https://www.caixinglobal.com/..."
```

Or read multiple in parallel:
```
mcp__jina__parallel_read_url:
  urls:
    - url: "https://www.reuters.com/..."
    - url: "https://www.scmp.com/..."
```

## Fallback: Serper MCP

If Jina search is unavailable:

```
mcp__serper__google_search:
  q: "{topic} site:reuters.com OR site:bloomberg.com"
  num: "10"
  tbs: "qdr:w"
```

## Best Practices

1. **Start with Tier 1 sources** for credibility
2. **Use multiple perspectives** for controversial topics (Western + Chinese sources)
3. **Filter by time** for current events (past week/month)
4. **Specify language** when searching non-English sources
5. **Cross-reference** claims across multiple sources before analysis
