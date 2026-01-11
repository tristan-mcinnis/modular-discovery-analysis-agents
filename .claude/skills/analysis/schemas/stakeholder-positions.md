# Stakeholder Positions Schema

Analyze multiple perspectives on a topic. Inspired by Fabric's `analyze_debate` pattern.

## When to Use

Use this schema for:
- Multi-source news analysis on controversial topics
- Policy debates with multiple stakeholders
- Business conflicts (labor disputes, regulatory battles)
- Geopolitical tensions with multiple parties

## Output Structure

```markdown
# Stakeholder Analysis: {Topic}

**Sources Analyzed:** {count} articles/documents
**Date Range:** {earliest} to {latest}
**Analysis Date:** {today}

---

## ISSUE SUMMARY

{30-word neutral summary of the issue/debate}

---

## STAKEHOLDERS

| Stakeholder | Type | Position (10 words) |
|-------------|------|---------------------|
| {Name/Group} | {Government/Industry/Civil Society/Expert} | {Brief position} |

---

## DETAILED POSITIONS

### {Stakeholder 1 Name}

**Role:** {Government official / CEO / Analyst / etc.}
**Organization:** {Company / Agency / Institution}
**Stated Position:** {16-word summary of their position}

**Key Arguments:**
- {Argument 1 - 16 words exactly}
- {Argument 2 - 16 words exactly}

**Supporting Quotes:**
> "{Exact quote}" — {Context/Date}

**Evidence Cited:**
- {Data or sources they reference}

**Potential Motivations:**
- {Why they might hold this position}

---

### {Stakeholder 2 Name}

{Repeat structure above}

---

## AREAS OF AGREEMENT

{Points where stakeholders align, even if they disagree overall}

| Agreement Point (16 words) | Stakeholders |
|---------------------------|--------------|
| {Point of agreement} | {Who agrees} |

---

## AREAS OF DISAGREEMENT

{Core points of contention that remain unresolved}

| Disagreement (16 words) | Side A | Side B |
|------------------------|--------|--------|
| {Point of disagreement} | {Position A} | {Position B} |

---

## POSSIBLE MISUNDERSTANDINGS

{Places where stakeholders may be talking past each other}

| Misunderstanding (16 words) | Stakeholders | Why It Occurred |
|----------------------------|--------------|-----------------|
| {Misunderstanding} | {Who} | {Reason} |

---

## POWER DYNAMICS

{Who has leverage, who is vulnerable}

| Stakeholder | Leverage | Vulnerabilities |
|-------------|----------|-----------------|
| {Name} | {What power they have} | {What they risk} |

---

## LIKELY OUTCOMES

{Based on positions and power dynamics}

| Scenario | Likelihood | Winners | Losers |
|----------|------------|---------|--------|
| {Outcome 1} | High/Medium/Low | {Who benefits} | {Who loses} |

---

## KEY LEARNINGS

{5-7 insights from analyzing these positions}

- {Learning 1 - exactly 16 words}
- {Learning 2 - exactly 16 words}

---

## TAKEAWAYS

{Actionable insights for someone following this issue}

- {Takeaway 1 - exactly 16 words}
- {Takeaway 2 - exactly 16 words}

---

## SOURCES

| Stakeholder | Source | Date |
|-------------|--------|------|
| {Name} | [{Article}]({URL}) | {Date} |
```

## Extraction Guidelines

1. **Be genuinely neutral**: Present each side's strongest arguments
2. **Use their words**: Include direct quotes to represent positions accurately
3. **Identify motivations**: Why might each party hold their position?
4. **Find common ground**: Even bitter opponents often agree on something
5. **Spot misunderstandings**: Often debates persist due to different definitions or frames

## Stakeholder Types

| Type | Examples |
|------|----------|
| **Government** | Regulators, elected officials, agencies |
| **Industry** | Companies, trade associations, executives |
| **Civil Society** | NGOs, advocacy groups, unions |
| **Experts** | Academics, analysts, researchers |
| **Media** | Journalists, commentators |
| **Public** | Consumer groups, affected communities |

## Quality Checklist

- [ ] All stakeholders represented fairly
- [ ] Direct quotes used (not paraphrased)
- [ ] Both agreements AND disagreements identified
- [ ] Potential motivations explored
- [ ] Power dynamics analyzed
- [ ] All positions exactly 16 words
- [ ] Sources cited for each stakeholder
