# Research Findings: Problem Validation

**Analysis Date:** 19 November 2025  
**Data Source:** Daily Bitcoin prices, 1 January 2025 - 19 November 2025 (311 days)  
**Price Range:** $75,004.68 - $124,310.60  
**Overall Market Performance:** -4.18% (first to last day)

## Question 1: Is there actually a periodic pattern in Bitcoin prices?

**Finding: Limited evidence of clear periodic patterns**

Our analysis tested for periodicity using multiple approaches:

- **Autocorrelation Analysis:** The strongest autocorrelation (0.981) occurs at a 1-day lag, which simply indicates that today's price strongly predicts tomorrow's price (momentum/trending behaviour). This is not evidence of a meaningful cycle.

- **Fourier Analysis:** Identified a dominant period of approximately 27.7 days. However, this should be interpreted cautiously - it may represent noise rather than a reliable cycle, especially given the limited data sample (only ~11 complete cycles in our dataset).

- **Visual Pattern Recognition:** The data shows typical cryptocurrency volatility with irregular ups and downs rather than consistent periodic oscillations.

**Conclusion:** No strong evidence of reliable periodic patterns that could be exploited for timing purchases. Bitcoin appears to follow a random walk with momentum rather than cyclical behaviour.

## Question 2: What constitutes a "dip" or "minima"?

**Finding: Multiple definitions yield different opportunities**

We tested three methods for identifying dips:

1. **Percentage Drop (>2% decline from previous day)**
   - Frequency: ~4.2 occurrences per month
   - Simple to identify in real-time
   - Captures sharp downward movements

2. **Statistical Deviation (>1 standard deviation below 14-day rolling mean)**
   - Frequency: ~7.2 occurrences per month
   - More nuanced, accounts for recent price context
   - Requires historical window (lags by 14 days)

3. **Local Minima (5-day spacing, >$1,000 prominence)**
   - Frequency: ~3.0 occurrences per month
   - Identifies true turning points
   - Can only be confirmed retrospectively (not actionable in real-time)

**Recommendation:** Method 2 (statistical deviation) appears most promising as it balances frequency with contextual awareness, though it requires 14 days of data before making recommendations.

## Question 3: How frequently do these buying opportunities occur?

**Finding: 3-7 opportunities per month depending on definition**

- Local minima (most selective): ~3 per month
- Percentage drops (moderate): ~4.2 per month  
- Statistical deviations (most frequent): ~7.2 per month

This translates to roughly 1-2 opportunities per week, which is:
- Frequent enough to be actionable
- Not so frequent as to overwhelm with constant alerts
- Varies significantly with market conditions (volatility clustering)

## Question 4: Historical success rate versus alternatives?

**Finding: MIXED RESULTS - Dip buying shows marginal improvement for short holds only**

### Buying at Dips (>1 std dev below mean):
- **7-day hold:** Mean +0.72%, Median +0.97%, 59% profitable
- **14-day hold:** Mean +1.01%, Median +1.28%, 59% profitable
- **30-day hold:** Mean -0.20%, Median -1.04%, 41% profitable ⚠️

### Buying on Random Days (baseline):
- **7-day hold:** Mean +0.40%, Median +0.38%, 55% profitable
- **14-day hold:** Mean +0.23%, Median -0.23%, 49% profitable
- **30-day hold:** Mean +2.46%, Median +1.73%, 58% profitable

### Key Insights:

1. **Short-term advantage exists:** Buying dips shows modestly better results for 7-14 day holds (+0.32-0.78% improvement over random)

2. **Long-term disadvantage:** The 30-day results are concerning - dip buying actually underperforms random buying significantly (-2.66% difference). This suggests "catching falling knives" risk.

3. **Low absolute returns:** Even the best strategy yields only ~1% over 14 days, which may not cover transaction fees on many exchanges

4. **High variability:** Daily volatility of 2.26% means these small edges are easily overwhelmed by market noise

## Additional Considerations

### Market Context (2025 Data)
- Overall declining market (-4.18%) may bias results
- Average daily volatility: 2.26%
- Extreme events: -10.04% (largest drop), +8.90% (largest gain)

### Transaction Costs
At typical exchange fees (0.1-0.5%), the ~1% edge on dip buying is significantly eroded, potentially making the strategy unprofitable after costs.

### Statistical Confidence
With only 311 days of data and 75 "dip" events, sample size is moderate. Results should be validated against longer historical periods and different market conditions (bull vs. bear markets).

## Verdict

**The hypothesis is PARTIALLY SUPPORTED but with significant caveats:**

✅ Dips can be systematically identified  
✅ Short-term (7-14 day) dip buying shows slight edge over random buying  
✅ Opportunities occur frequently enough to be actionable  

⚠️ No clear periodic pattern exists to predict when dips will occur  
⚠️ Long-term (30-day) performance is worse than random  
⚠️ Absolute returns are small and may not survive transaction costs  
⚠️ Results based on limited sample in declining market  

**Recommendation:** Proceed with caution. Consider:
- Testing against multi-year historical data
- Comparing against simple DCA (dollar-cost averaging) more rigorously
- Building in transaction cost modelling
- Testing in different market regimes (bull/bear/sideways)
- Potentially combining with other indicators rather than relying solely on dip detection
