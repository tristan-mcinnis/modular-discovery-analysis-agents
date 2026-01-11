# News Summary Schema

Extract key insights from news articles. Inspired by Fabric's `extract_article_wisdom` pattern.

## When to Use

Use this schema for:
- Single news articles or multiple articles on a topic
- Press releases and announcements
- Opinion pieces and analysis
- Market commentary

## Output Structure

```markdown
# News Analysis: {Topic}

**Sources Analyzed:** {count} articles
**Date Range:** {earliest} to {latest}
**Analysis Date:** {today}

---

## SUMMARY

{25-word summary of the core story, including who/what/when/where}

---

## KEY DEVELOPMENTS

{5-10 bullet points, each exactly 16 words, capturing the most important facts}

- {Development 1 - exactly 16 words}
- {Development 2 - exactly 16 words}
- ...

---

## NOTABLE QUOTES

{3-5 direct quotes from key figures, with attribution}

> "{Exact quote}" — {Name}, {Title/Role}

---

## FACTS & FIGURES

{Key statistics, numbers, and verifiable facts mentioned}

| Metric | Value | Source |
|--------|-------|--------|
| {metric} | {value} | {source article} |

---

## STAKEHOLDER REACTIONS

{Who said what - organized by stakeholder type}

### Government/Regulators
- {Name}: {Position summary}

### Companies/Industry
- {Name}: {Position summary}

### Analysts/Experts
- {Name}: {Position summary}

---

## TIMELINE

{Chronological sequence of events if applicable}

| Date | Event |
|------|-------|
| {date} | {event} |

---

## IMPLICATIONS

{3-5 bullet points on what this means going forward}

- {Implication 1}
- {Implication 2}

---

## REFERENCES

{All sources, people, companies, reports mentioned}

### Articles Analyzed
- [{Title}]({URL}) - {Publication}, {Date}

### People Mentioned
- {Name}, {Title} at {Organization}

### Reports/Documents Referenced
- {Document name}

---

## ONE-SENTENCE TAKEAWAY

{15-word sentence capturing the most important essence of the story}
```

## Extraction Guidelines

1. **SUMMARY**: Focus on the "so what" - why does this matter?
2. **KEY DEVELOPMENTS**: Each bullet must be exactly 16 words - forces precision
3. **QUOTES**: Use exact quotes only, never paraphrase
4. **FACTS**: Include units and context for all numbers
5. **STAKEHOLDER REACTIONS**: Group by type (government, industry, experts, public)
6. **TIMELINE**: Only include if there's a clear sequence of events
7. **IMPLICATIONS**: Focus on future impact, not past events

## Quality Checklist

- [ ] Summary is exactly 25 words
- [ ] Each KEY DEVELOPMENT is exactly 16 words
- [ ] All quotes are verbatim with attribution
- [ ] All numbers include units and context
- [ ] ONE-SENTENCE TAKEAWAY is exactly 15 words
- [ ] All sources are cited
