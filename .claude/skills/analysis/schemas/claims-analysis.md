# Claims Analysis Schema

Fact-check and evaluate truth claims in content. Inspired by Fabric's `analyze_claims` pattern.

## When to Use

Use this schema for:
- Controversial news or opinion pieces
- Political statements or policy announcements
- Marketing claims or company statements
- Research findings that need verification

## Output Structure

```markdown
# Claims Analysis: {Title/Topic}

**Source:** {Article/Document title}
**Author/Speaker:** {Name}
**Date:** {Publication date}
**Analysis Date:** {today}

---

## ARGUMENT SUMMARY

{30-word summary of the main argument being made}

---

## CLAIMS ANALYSIS

### Claim 1: {Claim in 16 words or less}

**CLAIM SUPPORT EVIDENCE:**
- {Evidence point 1 with verifiable source}
- {Evidence point 2 with verifiable source}
- Source: {URL or citation}

**CLAIM REFUTATION EVIDENCE:**
- {Counter-evidence point 1 with verifiable source}
- {Counter-evidence point 2 with verifiable source}
- Source: {URL or citation}

**LOGICAL FALLACIES:**
- {Fallacy type}: "{quoted example from text}"

**CLAIM RATING:** {A/B/C/D/F}
- A = Definitely True (overwhelming evidence)
- B = Likely True (strong evidence, minor gaps)
- C = Mixed (evidence on both sides)
- D = Likely False (weak evidence, significant counter-evidence)
- F = Definitely False (contradicted by facts)

**LABELS:** {characterization tags}
Examples: specious, well-sourced, emotional, data-driven, misleading, balanced, partisan, evidence-based

---

### Claim 2: {Claim in 16 words or less}

{Repeat structure above}

---

## LOGICAL FALLACIES SUMMARY

| Fallacy | Example | Impact |
|---------|---------|--------|
| {Type} | "{Quote}" | {How it affects the argument} |

Common fallacies to check:
- Ad hominem (attacking the person, not the argument)
- Straw man (misrepresenting the opposing view)
- False dichotomy (presenting only two options)
- Appeal to authority (citing authority without evidence)
- Cherry picking (selective use of data)
- Post hoc (assuming causation from correlation)
- Slippery slope (assuming extreme consequences)

---

## OVERALL SCORE

| Metric | Score |
|--------|-------|
| Lowest Claim Score | {A-F} |
| Highest Claim Score | {A-F} |
| Average Claim Score | {A-F} |

---

## OVERALL ANALYSIS

{30-word assessment of argument quality, main weaknesses, strengths, and recommendation for how to update understanding based on this analysis}

---

## VERIFICATION SOURCES

{List all sources used to verify/refute claims}

- {Source 1}: {URL}
- {Source 2}: {URL}
```

## Extraction Guidelines

1. **Separate claims from arguments**: A claim is a factual assertion; an argument is reasoning
2. **Find verifiable evidence**: Only use sources that can be independently checked
3. **Be genuinely neutral**: Look equally hard for supporting AND refuting evidence
4. **Identify fallacies precisely**: Quote the specific text that contains the fallacy
5. **Rate conservatively**: When uncertain, rate toward the middle (C)

## Rating Criteria

| Grade | Criteria |
|-------|----------|
| **A** | Multiple independent sources confirm; no credible counter-evidence |
| **B** | Strong evidence from reliable sources; minor gaps or caveats |
| **C** | Evidence exists on both sides; reasonable people could disagree |
| **D** | Weak evidence; significant counter-evidence; logical problems |
| **F** | Directly contradicted by verifiable facts; fundamentally false |

## Quality Checklist

- [ ] Each claim is stated in 16 words or less
- [ ] All evidence includes verifiable sources (not made up)
- [ ] Both supporting AND refuting evidence sought
- [ ] Fallacies include exact quotes
- [ ] Ratings are justified by evidence presented
- [ ] Overall analysis is exactly 30 words
