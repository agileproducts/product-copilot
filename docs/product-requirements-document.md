# Product Requirements Document: Bitcoin Sniper Alert Pilot

**Version:** 1.0  
**Date:** 25 November 2025  
**Product:** Bitcoin Sniper - Alert Pilot Phase  
**Author:** Product Team

## 1. Overview

Bitcoin Sniper will detect favourable buying opportunities in the Bitcoin market by identifying price dips and alerting the user via SMS. This document defines requirements for a 3-month pilot phase focused on alert delivery and validation of the dip-detection hypothesis.

## 2. Goals

- Validate the hypothesis that buying at detected dips outperforms regular dollar-cost averaging
- Provide timely, actionable alerts when Bitcoin price dips occur
- Collect data to inform future automated trading features

## 3. Success Criteria

After the 3-month pilot:
- System successfully delivers alerts for all detected dip events
- Notional profit from fixed-sum purchases at alerted dips exceeds fortnightly DCA by a meaningful percentage
- In declining markets: losses from dip-buying strategy are smaller than DCA losses

## 4. User

**Primary User:** Product owner (single user)  
**User Context:** Busy professional, needs clear actionable alerts, limited time to monitor markets manually

## 5. Core Requirements

### 5.1 Dip Detection
**REQ-01:** System shall fetch daily Bitcoin price data from Coinbase API once per day  
**REQ-02:** System shall calculate 14-day rolling mean and standard deviation of Bitcoin price  
**REQ-03:** System shall identify a "dip" when current price falls >1 standard deviation below the 14-day rolling mean  
**REQ-04:** System shall maintain at least 14 days of historical price data to enable detection algorithm

### 5.2 Alert Delivery
**REQ-05:** System shall send SMS alerts to the user when a dip is detected  
**REQ-06:** Alerts shall be sent at approximately 08:30 London time on weekdays only (Monday-Friday)  
**REQ-07:** System shall send email as a fallback if SMS delivery fails  

### 5.3 Alert Content
**REQ-08:** Alert shall include:
- Current Bitcoin price
- 14-day rolling mean price
- Number of standard deviations below mean
- Lowest price in past 14 days (for context)
- Last time a similar dip occurred

**Example format:**  
```
Bitcoin Sniper Alert!
Current: $89,450 (-1.2σ below mean)
14-day mean: $94,200
14-day low: $88,100
Last similar dip: 3 days ago
Consider buying opportunity.
```

### 5.4 Alert Frequency (Iterative Approach)

**Iteration 1 (Launch):**  
**REQ-09:** System shall send an alert for every qualifying dip event (no cooldown period)

**Future Iterations (to be evaluated after pilot data):**
- Option A: Maximum one alert per week
- Option B: Cooldown period of N days after each alert
- Option C: Alert only if dip is "significantly better" than recent alerts
- Decision to be made based on pilot phase observation of alert frequency and user feedback

### 5.5 Data Tracking
**REQ-10:** System shall log all detected dip events (whether alerted or not)  
**REQ-11:** System shall record all alert delivery attempts and outcomes  
**REQ-12:** System shall maintain price history for comparison with DCA baseline at pilot end

## 6. Non-Functional Requirements

**REQ-13:** System shall operate autonomously without manual intervention  
**REQ-14:** System shall be reliable enough to not miss dip detection on any trading day  
**REQ-15:** Alerts shall be delivered within 30 minutes of the scheduled time (08:30 London)

## 7. Out of Scope

The following are explicitly **not included** in this pilot phase:

- Automated trade execution
- Integration with cryptocurrency exchanges for actual purchases
- Portfolio tracking or profit/loss calculation
- Multi-currency support (Bitcoin only)
- Mobile application or web dashboard
- User account management or authentication
- Real-time price monitoring (only daily checks)
- Price prediction or machine learning models
- Alert customisation or user preferences
- Multiple user support
- Historical backtesting interface
- Risk management or position sizing recommendations

## 8. Assumptions

- Coinbase API will remain available and free for daily price data access
- User has consistent SMS reception at alert time
- User will manually track purchases made in response to alerts (for success measurement)
- 3-month pilot period is sufficient to collect meaningful comparison data
- Market will provide sufficient dip events during pilot period (based on historical ~7 per month)

## 9. Dependencies

- Access to Coinbase API (or approved alternative)
- SMS delivery service (provider TBD in technical design)
- Email delivery service for fallback
- Hosting environment capable of scheduled daily execution

## 10. Timeline

**Pilot Duration:** 3 months from launch  
**Launch Date:** When development complete and ready (exact date flexible)  
**Review Date:** End of month 3 - evaluate results and decide next phase

## 11. Success Metrics

- **Primary:** Notional profit comparison vs. DCA baseline
- **Secondary:** 
  - Alert delivery success rate (target: >99%)
  - Average time-to-delivery from scheduled time (target: <15 minutes)
  - Number of dip events detected during pilot
  - User satisfaction with alert timing and content

## 12. Future Phases (Post-Pilot)

Subject to pilot success:
- Phase 2: Automated trade execution
- Phase 3: Risk management and position sizing
- Phase 4: Advanced detection algorithms

---

## Approval

_To be signed off by product owner before development begins_
