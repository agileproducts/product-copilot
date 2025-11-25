# Technical Design Document: Bitcoin Sniper Alert Pilot

**Version:** 1.0  
**Date:** 25 November 2025  
**Product:** Bitcoin Sniper - Alert Pilot Phase  
**Author:** Technical Team

## 1. Overview

This document defines the technical architecture and implementation approach for the Bitcoin Sniper alert pilot system. The system will run as a serverless application on Google Cloud Platform, executing daily to detect Bitcoin price dips and deliver SMS/email alerts.

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────┐
│ Cloud Scheduler │ (Triggers daily at 08:30 London time)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cloud Function  │ (Python)
│  "dip-detector" │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌──────────────┐  ┌──────────────┐
│ Coinbase API │  │  Firestore   │
│ (Price Data) │  │ (Data Store) │
└──────────────┘  └──────────────┘
         │
         ▼
   ┌─────────────┐
   │ Dip         │
   │ Detected?   │
   └──────┬──────┘
          │
    ┌─────┴─────┐
    │ Yes       │ No
    ▼           ▼
┌─────────┐  [End]
│ Twilio  │
│ (SMS)   │
└────┬────┘
     │
     │ (Fallback)
     ▼
┌─────────┐
│SendGrid │
│ (Email) │
└─────────┘
```

### 2.2 Component Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| Scheduler | GCP Cloud Scheduler | Trigger daily execution |
| Compute | GCP Cloud Functions (Python 3.11+) | Dip detection logic |
| Data Store | GCP Firestore | Price history, dip logs, alert records |
| Price API | Coinbase API | Bitcoin price data |
| SMS | Twilio (via GCP Marketplace) | Primary alert delivery |
| Email | SendGrid | Fallback alert delivery |
| Monitoring | GCP Cloud Monitoring | Error alerts and logging |
| Secrets | Environment Variables | API keys and credentials |

## 3. Detailed Component Design

### 3.1 Cloud Function: `bitcoin-dip-detector`

**Runtime:** Python 3.11  
**Memory:** 256 MB  
**Timeout:** 60 seconds  
**Trigger:** HTTP (invoked by Cloud Scheduler)

**Environment Variables:**
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `SENDGRID_API_KEY`
- `SENDGRID_FROM_EMAIL`
- `USER_PHONE_NUMBER`
- `USER_EMAIL`
- `FIRESTORE_COLLECTION_PRICES` (default: "bitcoin_prices")
- `FIRESTORE_COLLECTION_ALERTS` (default: "alert_log")

**Execution Flow:**

```python
def main(request):
    # 1. Fetch current Bitcoin price from Coinbase API
    current_price = fetch_bitcoin_price()
    
    # 2. Store price in Firestore
    store_price(current_price)
    
    # 3. Retrieve last 14 days of prices from Firestore
    price_history = get_price_history(days=14)
    
    # 4. Calculate rolling statistics
    mean, std_dev = calculate_statistics(price_history)
    z_score = (current_price - mean) / std_dev
    
    # 5. Check if dip detected (z_score < -1.0)
    if z_score < -1.0:
        # 6a. Build alert message
        message = build_alert_message(current_price, mean, std_dev, z_score, price_history)
        
        # 6b. Send SMS via Twilio
        sms_success = send_sms(message)
        
        # 6c. Send email fallback if SMS fails
        if not sms_success:
            send_email(message)
        
        # 6d. Log alert
        log_alert(current_price, z_score, sms_success)
    
    # 7. Return success
    return {'status': 'success', 'dip_detected': z_score < -1.0}
```

**Hardcoded Configuration:**
```python
LOOKBACK_WINDOW = 14  # days
DIP_THRESHOLD = -1.0  # standard deviations
COINBASE_API_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
```

### 3.2 Data Storage: Firestore

**Collections:**

#### `bitcoin_prices`
```json
{
  "date": "2025-11-25",
  "timestamp": "2025-11-25T08:30:00Z",
  "price": 94250.50,
  "source": "coinbase"
}
```
**Indexes:** `date` (ascending), `timestamp` (descending)

#### `alert_log`
```json
{
  "timestamp": "2025-11-25T08:30:15Z",
  "date": "2025-11-25",
  "price": 89450.00,
  "mean": 94200.00,
  "std_dev": 3950.00,
  "z_score": -1.2,
  "sms_sent": true,
  "email_sent": false,
  "alert_message": "Bitcoin Sniper Alert!..."
}
```
**Indexes:** `date` (descending), `timestamp` (descending)

#### `dip_events`
```json
{
  "timestamp": "2025-11-25T08:30:15Z",
  "date": "2025-11-25",
  "price": 89450.00,
  "z_score": -1.2,
  "alerted": true
}
```
**Purpose:** Track all dips, even if alerts not sent (future iteration support)

**Spike/Fallback Plan:**
- **Week 1:** Implement Firestore solution
- **Week 1 Review:** If Firestore complexity/issues arise, fallback to CSV in Cloud Storage bucket
- **CSV Format (if used):** `prices.csv`, `alerts.csv`, `dips.csv` with same field structure

### 3.3 External APIs

#### Coinbase API
- **Endpoint:** `GET https://api.coinbase.com/v2/prices/BTC-USD/spot`
- **Authentication:** None required (public endpoint)
- **Rate Limit:** 10,000 requests/hour (far exceeds our 1/day need)
- **Response Format:**
```json
{
  "data": {
    "base": "BTC",
    "currency": "USD",
    "amount": "94250.50"
  }
}
```
- **Error Handling:** Retry up to 3 times with exponential backoff, alert on total failure

#### Twilio SMS (via GCP Marketplace)
- **Spike Approach:** Configure via GCP Marketplace, test integration
- **Fallback:** Direct Twilio API if marketplace integration proves problematic
- **Implementation:** Python `twilio` library
- **Message Length:** Target <160 characters to avoid multi-part SMS
- **Error Handling:** Log failure, trigger email fallback

#### SendGrid Email
- **Implementation:** Python `sendgrid` library
- **From Address:** Configured via environment variable
- **Subject:** "Bitcoin Sniper Alert - Dip Detected"
- **Format:** Plain text (same content as SMS for consistency)
- **Error Handling:** Log failure to Cloud Logging

### 3.4 Scheduling

**Cloud Scheduler Job:**
- **Name:** `bitcoin-dip-check-daily`
- **Frequency:** `30 8 * * 1-5` (08:30, Mon-Fri)
- **Timezone:** `Europe/London` (handles GMT/BST automatically)
- **Target:** HTTPS endpoint of Cloud Function
- **Retry Policy:** 
  - Max retry attempts: 3
  - Max retry duration: 30 minutes
  - Min/Max backoff: 5s / 1m

### 3.5 Monitoring and Alerting

**Cloud Monitoring Alerts:**

1. **Function Execution Failure**
   - Condition: Cloud Function returns error or times out
   - Notification: Email to user
   - Severity: Critical

2. **Function Not Executed**
   - Condition: No successful execution in 26 hours (allows for missed day detection)
   - Notification: Email to user
   - Severity: Warning

**Cloud Logging:**
- All executions logged with structured output
- Include: price fetched, calculation results, alert decisions, API call outcomes
- Retention: 30 days (default)

## 4. Alert Message Format

### SMS Format (Target: <160 chars)
```
Bitcoin Sniper Alert!
Current: $89,450 (-1.2σ)
14d mean: $94,200
14d low: $88,100
Last dip: 3d ago
Buy opportunity
```

### Email Format
```
Subject: Bitcoin Sniper Alert - Dip Detected

Bitcoin Sniper Alert!

Current Price: $89,450.00
14-day Mean: $94,200.00
Standard Deviations Below Mean: -1.2σ
14-day Low: $88,100.00
Last Similar Dip: 3 days ago

This appears to be a good buying opportunity.

---
Bitcoin Sniper Alert System
Alert Time: 2025-11-25 08:30:15 GMT
```

## 5. Algorithm Details

### Dip Detection Logic

```python
def detect_dip(price_history, current_price):
    """
    Detects if current price represents a dip.
    
    Args:
        price_history: List of dict with 'price' and 'date' keys (last 14 days)
        current_price: Float, current Bitcoin price
        
    Returns:
        tuple: (is_dip: bool, z_score: float, mean: float, std_dev: float)
    """
    prices = [p['price'] for p in price_history]
    
    # Calculate 14-day statistics
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    std_dev = variance ** 0.5
    
    # Calculate z-score
    z_score = (current_price - mean) / std_dev
    
    # Dip if more than 1 standard deviation below mean
    is_dip = z_score < -1.0
    
    return is_dip, z_score, mean, std_dev
```

### Historical Context

```python
def get_historical_context(price_history):
    """
    Extracts context for alert message.
    
    Returns:
        dict: {
            'lowest_price': float,
            'lowest_date': str,
            'days_since_last_dip': int or None
        }
    """
    prices = [(p['price'], p['date']) for p in price_history]
    lowest_price, lowest_date = min(prices, key=lambda x: x[0])
    
    # Find last dip (simplified - check for z_score < -1 in history)
    # Implementation details in code
    
    return {
        'lowest_price': lowest_price,
        'lowest_date': lowest_date,
        'days_since_last_dip': calculate_days_since_last_dip(price_history)
    }
```

## 6. Deployment

### 6.1 Infrastructure Setup

**Prerequisites:**
- GCP Project created
- Billing enabled
- Required APIs enabled:
  - Cloud Functions API
  - Cloud Scheduler API
  - Cloud Firestore API
  - Cloud Logging API
  - Cloud Monitoring API

**GCP Services Configuration:**

```bash
# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable firestore.googleapis.com

# Initialize Firestore (select region)
gcloud firestore databases create --region=europe-west2

# Deploy Cloud Function
gcloud functions deploy bitcoin-dip-detector \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --entry-point main \
  --memory 256MB \
  --timeout 60s \
  --set-env-vars TWILIO_ACCOUNT_SID=xxx,TWILIO_AUTH_TOKEN=xxx,...

# Create Cloud Scheduler job
gcloud scheduler jobs create http bitcoin-dip-check-daily \
  --schedule "30 8 * * 1-5" \
  --time-zone "Europe/London" \
  --uri "https://europe-west2-PROJECT_ID.cloudfunctions.net/bitcoin-dip-detector" \
  --http-method GET
```

### 6.2 Dependencies

**Python Requirements (`requirements.txt`):**
```
google-cloud-firestore==2.14.0
requests==2.31.0
twilio==8.11.0
sendgrid==6.11.0
```

### 6.3 Testing Strategy

**Pre-deployment:**
1. Unit tests for dip detection logic
2. Mock API responses for testing
3. Local execution with test data

**Post-deployment:**
1. Manual trigger via Cloud Console (test with current price)
2. Verify Firestore writes
3. Test SMS delivery (force a dip condition)
4. Test email fallback (disable Twilio temporarily)
5. Verify Cloud Logging output
6. Confirm Cloud Scheduler execution

## 7. Security Considerations

- Cloud Function authenticated via Cloud Scheduler service account
- Environment variables for secrets (acceptable for pilot; migrate to Secret Manager for production)
- Firestore security rules: deny all external access (function uses service account)
- No public endpoints except the Cloud Function (which performs no sensitive operations)
- API keys rotated if compromised

## 8. Cost Estimate

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| Cloud Functions | 30 invocations × 256MB × 5s | Free tier |
| Cloud Scheduler | 1 job | Free (up to 3 jobs) |
| Firestore | ~100 writes, ~450 reads, <1MB | Free tier |
| Twilio SMS | ~30 messages | ~£1.50 |
| SendGrid | <10 emails (fallback only) | Free tier |
| Cloud Logging | Standard logs, 30-day retention | Free tier |
| Cloud Monitoring | 2 alert policies | Free tier |
| **Total** | | **~£1.50/month** |

*Note: First year may be entirely free under GCP free tier. Costs may increase slightly after free tier expiration.*

## 9. Future Enhancements (Out of Scope for Pilot)

**Iteration 2+ Considerations:**
- Alert frequency management (cooldown periods)
- Configurable parameters via Cloud Storage config file
- Migration to Secret Manager for credentials
- CSV fallback implementation if Firestore spike unsuccessful
- Direct Twilio integration if GCP Marketplace spike unsuccessful
- Dashboard for viewing price history and alerts
- Backtesting interface
- Multiple detection algorithms

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Coinbase API downtime | Missed dip detection | Retry logic, monitoring alert |
| Twilio SMS delivery failure | No alert received | Email fallback, delivery logging |
| Cloud Function cold start delay | Late alert delivery | Acceptable for 30-min SLA |
| Firestore complexity | Development delay | Spike early, CSV fallback ready |
| Incorrect timezone handling | Wrong alert time | Test DST transitions |
| Insufficient free tier | Unexpected costs | Set billing alerts at £5 threshold |

## 11. Success Criteria (Technical)

- [ ] Function executes successfully every weekday at 08:30 ± 15 minutes
- [ ] Zero missed executions over pilot period
- [ ] >99% SMS delivery success rate
- [ ] <30 seconds average execution time
- [ ] All dip events and alerts logged to Firestore
- [ ] Zero unauthorized access to data or credentials

## 12. Approval and Sign-off

**Technical Architect:** ___________________ Date: ___________

**Product Owner:** ___________________ Date: ___________

---

## Appendix A: Spike Plan

### Firestore Spike (Week 1)
**Goals:**
- Successfully write/read price data
- Query last 14 days efficiently
- Evaluate complexity vs. CSV approach

**Success Criteria:**
- <2 hours to implement basic CRUD operations
- Query performance adequate (<1 second)
- Clear documentation available

**Fallback Trigger:**
- Implementation takes >4 hours
- Unexpected costs or quota issues
- Complexity seems unnecessary for data volume

### Twilio GCP Marketplace Spike (Week 1)
**Goals:**
- Configure Twilio via GCP Marketplace
- Send test SMS successfully
- Verify billing integration

**Success Criteria:**
- SMS delivered successfully
- Straightforward configuration
- Unified billing working

**Fallback Trigger:**
- Marketplace integration incomplete/buggy
- Unclear pricing
- Takes >2 hours to configure vs. <30 mins for direct Twilio

## Appendix B: Development Phases

**Phase 1: Core Function (Week 1-2)**
- Implement price fetching from Coinbase
- Implement dip detection algorithm
- Firestore/CSV spike and implementation
- Unit tests

**Phase 2: Alerting (Week 2)**
- Twilio spike and SMS implementation
- SendGrid email fallback
- Alert message formatting

**Phase 3: Deployment (Week 3)**
- GCP infrastructure setup
- Cloud Function deployment
- Cloud Scheduler configuration
- End-to-end testing

**Phase 4: Monitoring (Week 3)**
- Cloud Monitoring alerts
- Log analysis
- Documentation finalization

**Phase 5: Pilot Launch (Week 4)**
- Final testing
- Production deployment
- Pilot begins
