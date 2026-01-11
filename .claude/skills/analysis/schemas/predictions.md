# Predictions Schema

Extract and evaluate predictions and future outlook. Inspired by Fabric's `extract_predictions` pattern.

## When to Use

Use this schema for:
- Analyst forecasts and market predictions
- Company guidance and outlook statements
- Expert commentary on future trends
- Policy impact projections

## Output Structure

```markdown
# Predictions Analysis: {Topic}

**Sources Analyzed:** {count} articles/documents
**Prediction Horizon:** {Short-term / Medium-term / Long-term}
**Analysis Date:** {today}

---

## SUMMARY OF OUTLOOK

{25-word summary of the overall consensus or key predictions}

---

## PREDICTIONS TABLE

| Prediction (16 words max) | Source | Date By | Confidence | How to Verify |
|--------------------------|--------|---------|------------|---------------|
| {Specific prediction} | {Who said it} | {Target date} | High/Medium/Low | {What would prove it true/false} |

---

## DETAILED PREDICTIONS

### Prediction 1: {Title}

**Statement:** {Exact prediction in 16 words or less}
**Source:** {Who made the prediction}
**Context:** {Where/when it was stated}
**Target Date:** {When it should occur by}
**Confidence Level:** {High/Medium/Low/Not stated}

**Verification Criteria:**
- {What would prove this true}
- {What would prove this false}

**Supporting Reasoning:**
- {Why the source believes this}

**Counter-Arguments:**
- {Why this might not happen}

---

### Prediction 2: {Title}

{Repeat structure}

---

## PREDICTIONS BY TIMEFRAME

### Near-term (0-6 months)
- {Prediction 1}
- {Prediction 2}

### Medium-term (6-18 months)
- {Prediction 1}
- {Prediction 2}

### Long-term (18+ months)
- {Prediction 1}
- {Prediction 2}

---

## PREDICTIONS BY CATEGORY

### Market/Financial
| Prediction | Source | Confidence |
|------------|--------|------------|
| {Prediction} | {Source} | {Level} |

### Technology/Product
| Prediction | Source | Confidence |
|------------|--------|------------|
| {Prediction} | {Source} | {Level} |

### Regulatory/Policy
| Prediction | Source | Confidence |
|------------|--------|------------|
| {Prediction} | {Source} | {Level} |

### Competitive/Industry
| Prediction | Source | Confidence |
|------------|--------|------------|
| {Prediction} | {Source} | {Level} |

---

## CONSENSUS VS. CONTRARIAN VIEWS

### Consensus Predictions
{What most sources agree will happen}

- {Consensus view 1}
- {Consensus view 2}

### Contrarian Predictions
{Minority views that differ from consensus}

| Contrarian View | Source | Why Different |
|-----------------|--------|---------------|
| {View} | {Who} | {Their reasoning} |

---

## TRACK RECORD

{If available: How accurate have these sources been before?}

| Source | Past Prediction | Outcome | Accuracy |
|--------|-----------------|---------|----------|
| {Name} | {What they predicted} | {What happened} | Correct/Partial/Wrong |

---

## DEPENDENCIES & ASSUMPTIONS

{What conditions must hold for predictions to come true}

| Prediction | Key Assumption | Risk if Wrong |
|------------|----------------|---------------|
| {Prediction} | {What it assumes} | {What happens if assumption fails} |

---

## SCENARIOS

### Bull Case
{If things go better than expected}
- {Trigger}
- {Outcome}

### Base Case
{Most likely scenario}
- {Assumptions}
- {Outcome}

### Bear Case
{If things go worse than expected}
- {Trigger}
- {Outcome}

---

## MONITORING CHECKLIST

{How to track whether predictions are coming true}

- [ ] {Metric/Event 1 to watch} — Target: {value/date}
- [ ] {Metric/Event 2 to watch} — Target: {value/date}

---

## SOURCES

| Source | Type | Date | URL |
|--------|------|------|-----|
| {Name} | Analyst/Executive/Expert | {Date} | {URL} |
```

## Extraction Guidelines

1. **Be specific**: "Revenue will grow" is not a prediction; "Revenue will grow 15% in Q3" is
2. **Capture confidence**: Note how certain the source sounds
3. **Define verification**: How would we know if this came true?
4. **Note timeframes**: When is this supposed to happen?
5. **Identify assumptions**: What must be true for the prediction to hold?

## Confidence Level Criteria

| Level | Indicators |
|-------|------------|
| **High** | Strong language ("will", "certain"), specific numbers, clear reasoning |
| **Medium** | Hedged language ("likely", "expect"), ranges given, some uncertainty noted |
| **Low** | Speculative language ("could", "might"), wide ranges, many caveats |
| **Not stated** | No confidence indicated by source |

## Quality Checklist

- [ ] Each prediction is specific and falsifiable
- [ ] Target dates captured where stated
- [ ] Confidence levels noted
- [ ] Verification criteria defined
- [ ] Key assumptions identified
- [ ] Contrarian views included
- [ ] All sources cited with dates
