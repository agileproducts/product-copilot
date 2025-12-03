# Using Github Copilot for product management and business analysis

---

![Copilot splash screen](copilot-splash.png)

--

<div class="myprompt">
&gt; npm install -g @github/copilot
</div>

<div class="myprompt">
&gt; copilot
</div>

---

<div class="myprompt">
&gt; read instructions.md and tell me what you think
we are going to do
</div>


<div class="copilot-response">
We're going to demonstrate using GitHub Copilot for product management and business analysis work, developing a hypothetical product from vision through user stories without actual implementation.
</div>

---

<div class="myprompt">
&gt; read the product vision I have supplied
</div>

<div class="copilot-response">
Got it! You're building "Bitcoin Sniper" - a tool to detect periodic dips in Bitcoin prices and alert you (or eventually auto-buy) when there's a favourable buying opportunity. It's a personal project for one user (you) based on the hypothesis that Bitcoin price patterns are somewhat periodic. Starting with alerts before moving to automated trading
</div>

---

<div class="myprompt">
&gt; what research questions would you have at this time? Write them to a document
</div>

---

<div class="myprompt">
&gt; I've added a csv file of daily bitcoin prices to the data folder. See if you can have a go at answering the first few research questions you listed under 'problem validation'. Write your findings to a file
</div>

---

<div class="myprompt">
&gt; I note that your research isn't convinced about the financial viability of this. But as the project is for demonstration purposes we'll assume I want to proceed anyway. I've answered some of your other questions in separate research findings documents. What's your understanding now?
</div>

--

<div class="copilot-response">
Perfect! Here's my understanding:

   Technical: Coinbase APIs available for daily Bitcoin data, which meets your needs.

   User Needs: Daily alert (weekdays only) at 8:30 AM London time via SMS (preferred) or email, showing current price and context for why it's a buying opportunity.

   Scope: Starting with an alert-only pilot for one quarter, deferring actual trading implementation and associated financial/regulatory concerns until later.

   Success Criteria: Compare notional profits from your alert-triggered buys (fixed sum per alert) against fortnightly DCA over the quarter. Success = beating DCA by a
   meaningful percentage (or losing less in a down market).

   So we're building an observation/alert system first, which is sensible—validate the hypothesis with real-time alerts before automating trades. Ready to move forward with
   defining requirements and user stories for this pilot phase?
</div>  

---

<div class="myprompt">
&gt; Let's start by drafting a short, focused product requirements document. Ask me any questions you have.
</div>

--

<div class="copilot-response">
 I'll draft a PRD for the Bitcoin Sniper alert pilot. A few questions first:

Alert frequency: If multiple days in a week trigger the dip criteria, should you receive an alert each time, or is there a cooldown period (e.g. only one alert per week)?

Dip detection method: Based on my analysis, the statistical deviation method (>1 std dev below 14-day mean) seemed most promising. Should we use that, or would you prefer the simpler >2% daily drop method?

Alert content specifics: Beyond current price and context, do you want historical comparison (e.g., "lowest in past 14 days") or forward-looking info (e.g., "similar dips recovered by X% within 7 days")?

SMS provider preference: Do you have a preference (Twilio, AWS SNS, etc.) or should I just note "SMS service TBD"?

Pilot start date: When do you plan to begin the 3-month pilot?

Out of scope clarifications: Should I explicitly list things like "no automated trading", "no portfolio tracking", "no multi-currency support" to keep scope tight?
</div>

--

<div class="myprompt">
&gt; Let's use your suggestions for dip detection. I think we'll try historical context for alerts. Let's leave the choice of SMS provider for our technical design document. Start date is - whenever we are shipped and ready, the exact day is not important. Those are the easy ones. On alert frequency - I suggest we think in terms of iteration here? State your out of scopes for now.
</div>

--

<div class="copilot-response">
Done! I've created a focused PRD covering the alert pilot phase. Key points:

Alert frequency: Iteration 1 starts with no cooldown (alert every dip), with options for future iterations based on pilot learnings.

Out of scope: All trading automation, portfolio tracking, multi-user, dashboards, predictions, and customisation features—keeping this strictly about alert delivery and hypothesis validation.

Does this capture what you need, or would you like me to adjust anything?
</div>

---

<div class="myprompt">
&gt; Now let's think about a technical design document. Again, ask me any questions you have. One at a time might be easier.
</div>

--

<div class="copilot-response">
Let me start with the foundational question. Hosting/deployment environment: What's your preference for where this will run? Options could include:

  - Cloud provider (AWS, Azure, GCP) with serverless functions (Lambda, Cloud Functions, etc.)
  - Cloud provider with a small always-on server/container
  - Self-hosted on your own hardware/VPS
  - Something else?

This will inform the rest of the technical architecture decisions.
</div>

--

<div class="myprompt">
&gt; well, I don't want to spend a lot of money on this. What's your assessment of the first two cloud options versus running it myself on something like a raspberry pi? 
</div>

--

<div class="copilot-response">
Serverless (AWS Lambda/CloudWatch):

     - ~$0.20/month (1 execution/day, minimal compute)
     - Free tier covers this easily for first year
     - SMS via AWS SNS: ~$0.05 per message (£1.50/month for 30 alerts)
     - Total: ~£2/month after free tier expires

   Small cloud server (t2.micro/equivalent):

     - ~$5-10/month for basic instance
     - SMS costs same as above
     - Total: ~£8-12/month

   Raspberry Pi (self-hosted):

     - One-time: £35-50 for Pi, £10-15 for power supply/SD card
     - Running costs: ~£2/month electricity
     - SMS via Twilio/similar: same ~£1.50/month
     - Total: £50 upfront, then £3.50/month
     - BUT: Your internet/power reliability becomes critical, you handle all maintenance

   My recommendation: Serverless for a 3-month pilot. Minimal cost (possibly free), zero maintenance, highly reliable, and you're not locked in. If this becomes long-term, the
   Pi makes financial sense after ~18 months.

   What's your preference given the cost/effort trade-offs?
</div>

--

<div class="copilot-response">
Data storage: For storing the price history, detected dips, and alert logs (REQ-10, REQ-11, REQ-12), what would you prefer?

Options:

  - Cloud Storage bucket with CSV/JSON files (simplest, cheapest, ~pennies/month)
  - Cloud Firestore (NoSQL, easy queries, free tier generous)
  - Cloud SQL (PostgreSQL/MySQL, more overhead but familiar if you prefer SQL)
  - BigQuery (overkill for this, but good if you want to do analysis later)

Given the small data volumes (daily entries, ~90 records over pilot), even the "expensive" options are negligible cost-wise.
</div>

-- 

<div class="myprompt">
&gt; I've done projects myself just with a csv in a bucket and agree the SQL options are overkill at this stage. But I'm unfamiliar with firestore
</div>

--

<div class="copilot-response">
  Firestore quick comparison:

   CSV in Cloud Storage (your experience):

     - Read entire file, append new row, write back
     - Manual parsing/formatting
     - Risk of corruption if writes fail mid-process
     - Need to handle locking if multiple processes
     - Simple, predictable

   Firestore (NoSQL document DB):

     - Add records with single API call: db.collection('prices').add({date: ..., price: ...})
     - Query easily: "get all dips in last 30 days"
     - Atomic writes (no corruption risk)
     - Free tier: 50K reads, 20K writes, 1GB storage per day (way more than needed)
     - Cost after free tier: effectively £0 for this use case
     - Slightly more setup than CSV initially

   My take for this project: CSV is fine and you know it works. Firestore is marginally "better" but adds a learning curve you don't need for a 3-month pilot with 90 records.

   Recommendation: Stick with CSV in Cloud Storage bucket unless you want to learn Firestore for future projects?
</div>

-- 

<div class="myprompt">
&gt; Let's plan to spike firestore and then fall back on a csv if we don't like it
</div>

--

<div class="copilot-response">
[Questions follow about alerting mechanisms (email/SMS) and monitoring. For example]  

Error handling and monitoring: If something goes wrong (API down, SMS fails, function crashes), how should you be notified?

   Options:

     - GCP Cloud Monitoring alerts (email you on function failures)
     - Just rely on missing the expected alert (if no SMS arrives, something went wrong)
     - Separate error notification channel (different email/SMS for system errors vs. Bitcoin alerts)
     - Logging only (check Cloud Logging manually if curious)

   Given this is monitoring Bitcoin for buying opportunities, missing an alert could be costly. What level of error visibility do you want?
</div>

--

<div class="myprompt">
&gt; Do you see what the problem would be if I rely on the absence of an alert to know this is broken?
</div>

--

<div class="copilot-response">
Yes - if there's no legitimate dip, you won't get an alert anyway, so silence could mean either "system working, no dip detected" or "system broken." You can't distinguish between the two. So you need some form of active monitoring. Would you prefer...
</div>

---

<div class="myprompt">
&gt; I've updated my instructions. Have a read
</div>

<div class="copilot-response">
✔ Read instructions.md
   └ 41 lines read

 Noted! Key updates:

  - User stories: Use BDD (Given, When, Then) format
  - No separate test stories: TDD is expected, tests are part of the story
  - Story size: Ideally 2 days or less
  - Story mapping: Create in SVG format to plan releases
  - GitHub issues: Stories should be created as issues with --label story --label backlog
  - Workflow labels: backlog → ready for dev → in development

   Ready to create a story map and start writing user stories for the Bitcoin Sniper pilot?
</div>

---

<div class="myprompt">
&gt; Try creating a story map
</div>

<div class="copilot-response">
✔ Create docs/story-map.svg (+238)
</div>

---

!["story map first attempt"](story-map-first-attempt.svg)

---

<div class="myprompt">
&gt;  I wasn't totally happy with the story map. I've renamed it to story-map-first-attempt.svg I've added a critique in a markdown file. Please read that and tell me your thoughts
</div>

--

<div class="doc">
# Critique of the first attempt at a story map

This is a decent attempt at a story map. But there are some things I think we should change.

1. Configuring GCP or deploying a cloud function are tasks, not stories. These are things we would do as part of stories to deliver real working software. So I don't think they belong on a story map.
2. I like story maps in which you would move along the top row to deliver a steel thread. But in this map you would have to work down some of the columns first.
3. You have a column about tracking/storing data which comes after sending an alert, this is the wrong way around isn't it?
4. You have a story to 'structure logging'. This is a task. What story would you do involving logging that did not involve structuring it?
5.  End-to-end test is not a story. Remember we are doing TDD and CI/CD. Our software is *always* tested end to end as part of our deployment pipeline.
6. Now I think of it, setting up a deployment pipeline is the kind of thing that can absorb a lot of time in a story that I'd prefer to have visibility of. Maybe we should identify this as a kind of iteration 0 prerequisite. 
7. You don't need to add time estimates to these stories. You aren't the coder, yet. 
</div>

--
<div class="copilot-response">
Excellent critique! You're absolutely right on all points. Let me address each:

    - GCP config, deployment = tasks not stories - Agreed. These are implementation details within stories, not user-facing value.
    - Steel thread should flow horizontally - Yes! The top row should be the user journey you can walk through left-to-right for the first working slice.
    - Data storage before alerts - Correct! You need to store data before you can detect patterns and alert. My ordering was backwards.
    - "Structure logging" is a task - Right. Logging is a quality aspect of every story, not a separate deliverable.
    - End-to-end test isn't a story - Absolutely. With TDD/CI/CD, this is continuous practice, not a phase.
    - Deployment pipeline = iteration 0 - Smart. Getting the infrastructure and pipeline set up is essential scaffolding before story work begins.
    - No time estimates needed - Fair point. These are sizing conversations for the dev team, not product decisions.

Should I create a revised story map focused on:

    - User-facing value (stories not tasks)
    - Horizontal steel thread flow
    - Proper sequencing (store → analyze → alert)
    - Iteration 0 for infrastructure setup?
</div>

---

<div class="myprompt">
&gt; ok have another go. Call this story-map-attempt-2
</div>

<div class="copilot-response">
Done! I've created a revised story map (story-map-attempt-2.svg) that addresses your critique
</div>

---

!["story map first attempt"](story-map-attempt-2.svg)

---

<div class="myprompt">
&gt; Are you familiar with Mike Cohn's book 'user stories applied'?
</div>

<div class="copilot-response">
Yes, I'm familiar with Mike Cohn's "User Stories Applied: For Agile Software Development" (2004). It's a foundational text on writing effective user stories.

   Key concepts from the book include:

     - User story format: "As a [role], I want [goal] so that [benefit]"
     - INVEST criteria: Independent, Negotiable, Valuable, Estimable, Small, Testable
     - Three Cs: Card (brief description), Conversation (discussion details), Confirmation (acceptance criteria)
     - Story splitting techniques - breaking down large stories
     - Personas and user roles
     - Epics and themes for organizing stories
</div>

--

<div class="myprompt">
&gt; Expand on Cohn's INVEST criteria.
</div>

<div class="copilot-response">
INVEST Criteria for User Stories (Mike Cohn):

    - Independent: Stories should be loosely coupled, allowing them to be developed in any order without creating dependencies. This gives the product owner flexibility in prioritization. If two stories are tightly dependent, consider combining them or finding a way to decouple.
    - Negotiable: A story is not a contract. It's a placeholder for a conversation between the development team and product owner. Details are worked out during planning and development, not written in stone upfront. Stories should leave room for discussion about implementation.
    - Valuable: Every story must deliver value to the user (or customer/stakeholder). Avoid technical tasks masquerading as stories. "Refactor database schema" isn't valuable to users; "Process orders 50% faster" is
    - Estimable: The team must be able to estimate the story's size/effort. If they can't estimate, it's usually because the story is too vague, too large, or the team lacks necessary knowledge. These issues need resolving before development.
    - Small: Stories should be sized to fit within a single iteration/sprint. Large stories (epics) need splitting. "Small" is relative to your team's sprint length, but typically means a few days of work, not weeks.
    - Testable: You must be able to write tests to verify the story is complete. If you can't define success criteria, the story is too vague. This drives clear acceptance criteria (which is where Given/When/Then fits nicely).

   Does this align with how you're thinking about the Bitcoin Sniper stories?
</div>

--

<div class="myprompt">
&gt; I don't necessarily agree with them all in 2025.
</div>

<div class="copilot-response">
Which INVEST criteria do you question in 2025?
</div>

<div class="myprompt">
&gt; I think it's sometimes inevitable that stories depend on each other. You can't build software in literally any order. His emphasis on estimation reflected an era when agile was dominated by scrum - that's also why he talks about sprints. This thinking predated modern ci/cd. And I've had bad experiences with teams taking the idea of 'negotiable' to extremes and trying to kick off stories with no analysis done at all. This is especially messy in a world of distibuted working. Stories need to have clear definition. However, I strongly agree with valuable, small and testable.
</div>

--

<div class="myprompt">
&gt;What story splitting techniques does Cohn talk about?
</div>

<div class="copilot-response">
Cohn's story splitting patterns include:

    - By workflow steps: Split a complex process into individual steps (e.g., "register account" → "enter details", "verify email", "set password")

    - By business rule variations: Different rules/conditions as separate stories (e.g., "calculate shipping" → "domestic shipping", "international shipping", "expedited shipping")

    - By data entry methods: Different ways to accomplish the same goal (e.g., "import contacts" → "manual entry", "CSV upload", "sync from Gmail")

    - By data variations: Different types of data (e.g., "support payment methods", "credit card", "PayPal", "bank transfer")

    - By operations (CRUD): Create, Read, Update, Delete as separate stories

    - By acceptance criteria: When multiple acceptance criteria exist, each could become its own story

    - By performance/quality attributes: Start with basic functionality, then add performance/security/usability stories

    - By simple/complex: Implement simple version first, complex cases later (e.g., "search products" → "exact match" then "fuzzy search")

    - Spike/implementation split: Research spike first, then implementation story
</div>

-- 

<div class="myprompt">
&gt;How do Cohn's guidelines on sizing and spliting stories compare to those in Jeff Patton's book 'User Story Mapping'?
</div>

<div class="copilot-response smaller">
I'm familiar with Jeff Patton's "User Story Mapping" (2014), which came a decade after Cohn and reflects evolved thinking. Key differences:

* Patton on splitting: Emphasizes horizontal slicing - cutting through the full stack to deliver thin end-to-end functionality. This is the "walking skeleton" / "steel thread" approach. Cohn's patterns are more tactical; Patton's is more strategic about delivering complete user value early.

* Patton's "release strategy": Uses the story map to define MVPs by drawing horizontal lines - "everything above this line is Release 1". Less about individual story size, more about what collection of stories delivers a coherent release.

* Patton on sizing: Stories should be sized for learning, not just estimation. Build the smallest thing that lets you validate assumptions. This aligns with modern continuous delivery better than Scrum sprint sizing
     
* Opening the box: Patton talks about "opening the box" on a story - breaking it down only when you're ready to work on it, not upfront. This is more compatible with distributed teams needing clarity - detail comes at the right time.
     
* Narrative flow: Patton emphasizes the story map should tell the user's journey left-to-right. This is what I tried with attempt 2.
     
Does Patton's approach resonate more with how you work?
</div>

--

<div class="myprompt">
&gt;Has anyone else been an influential thinker on user stories since this?
</div>

<div class="copilot-response smaller">

Some influential voices on user stories and product work since Patton (2014):
 * Gojko Adzic - "Impact Mapping" and "Specification by Example" - focuses on connecting stories to business outcomes and using concrete examples as acceptance criteria. Veryaligned with your preference for clear definition and testability.
 * Teresa Torres - "Continuous Discovery Habits" (2021) - emphasizes opportunity solution trees and connecting stories to user outcomes through ongoing discovery. Less about story format, more about ensuring you're solving the right problems.
 * Marty Cagan - "Inspired" / "Empowered" - advocates for outcome-based product teams over feature factories. Questions whether detailed user stories are even necessary if teams focus on problems to solve rather than features to build.
 * Kent Beck / Extreme Programming community - "Vertical slicing" techniques that emphasize thin end-to-end functionality over horizontal layers, closely related to steel threads.
 * Shape Up (Basecamp/37signals) - Jason Fried and DHH's approach uses "pitches" and "scopes" instead of user stories, focusing on appetite (time budget) rather than estimation.
 * #NoEstimates movement - Vasco Duarte and others questioning whether estimation adds value at all, focusing instead on breaking work small and measuring flow.

Are any of these approaches familiar to you, or influencing your thinking on Bitcoin Sniper?
</div>

--

<div class="myprompt">
&gt;I think we need to write ourselves some guidelines on how to identify user stories. These should be based on the best of Cohn and Patton - the classic ideas are still right. I see example mapping more as a technique for driving stories out than a way of writing them down. I'm not a fan of giving teams vague problems and expecting them to freestyle, I don't think many people can really do that. Try drafing some guidelines in a doc.
</div>

<div class="copilot-response">
 ✔ Create docs/user-story-guidelines.md (+201)
</div>

---

<div class="myprompt">
&gt;Have a third attempt at your story map, in the light of these guidelines.
</div>

---

!["story map"](story-map.svg)

---

<div class="myprompt">
&gt; Ok let's start by trying to add the first story
</div>

---

!["picture of first story"](story2.png)

--

<div class="myprompt">
&gt;  How would you showcase or demo that this story is done?
</div>

--

<div class="copilot-response smaller">
Good question. For "Fetch daily Bitcoin price", I'd demonstrate:

Live demo:
  - Trigger the Cloud Function manually (via GCP Console or gcloud CLI)
  - Show it executing successfully (function logs showing "fetching price...")
  - Query Firestore to show the new price record with today's timestamp
  - Show the logged output with the actual price fetched

Alternatively, if the scheduled run already happened:
  - Open Firestore console and show the bitcoin_prices collection
  - Point to today's entry with timestamp ~08:30
  - Show Cloud Function execution logs from this morning confirming it ran

The key is: there's a new price record in Firestore that wasn't there before, with today's date.

But this highlights a potential issue with the story - it's mixing two concerns:
  - Fetching the price (the API call)
  - Storing it (persistence)

Should we split this? Or is it small enough that fetching without storing has no user value, so they belong together in the steel thread?
</div>

--

<div class="myprompt">
&gt; If I were an engineer building this I'd definitely get 'fetch' working first, them 'store' and finally 'schedule'. Without store, it's very difficult to prove 'schedule' is working. But there is a risk here of breaking the story into technical tasks that don't deliver demoable value, right? 
</div>

--

<div class="copilot-response smaller">
Exactly - you've hit the classic tension. As an engineer, the natural build order is:

  - Fetch - call API, log response to console
  - Store - persist to Firestore  
  - Schedule - Cloud Scheduler triggers it daily

But only at step 3 do you have something truly demoable to a stakeholder who cares about the business value, not the technical implementation.

Options:

A) Keep story as-is - "Fetch daily Bitcoin price" includes all three technical steps. It's small (maybe 1-2 days), delivers complete value. Demo shows: "it ran this morning at 08:30 and stored the price."

B) Split into two stories:

  - "Fetch and store Bitcoin price" (manually triggered for now)
  - "Schedule daily price fetch" (add the scheduler)

First story is demoable: "I can manually trigger it and see the price in Firestore." Second adds automation.

C) Accept the steel thread story is slightly larger - it's the minimum viable slice, so it includes all the plumbing even if that's a few days of work.

I lean toward A - keep it together. The story is still small, and splitting creates a first story that's only half-useful. What's your instinct?
</div>

--
<div class="myprompt">
&gt;Well what I'd do here is ask how much work things are - I don't want stories that are too big. But since you are estimating 1-2 days for the complete story, lets go with option A.
</div>

<div class="myprompt">
&gt;Now pretend you are a QA, What do you think you're going to ask about this story?
</div>

--

<div class="copilot-response smaller">
As a QA, I'd ask:

Error scenarios:
  - What happens if Coinbase API is down or returns an error? Do we retry? Log and continue? Alert someone?
  - What if the API returns invalid data (null, negative number, malformed JSON)?
  - What if Firestore write fails?

Duplicate handling:
  - If the function runs twice in the same day (manual trigger + scheduled), do we store both? Overwrite? Prevent duplicates?

Data validation:
  - What's a "reasonable" price range? Should we reject obviously wrong values (e.g., $1 or $10 million)?
  - Do we validate the timestamp format?

Observability:
  - How do I verify it ran successfully without checking Firestore directly?
  - What gets logged? Just "success" or the actual price fetched?

Timezone edge cases:
  - "08:30 London time" - what about DST transitions? (Though you said Cloud Scheduler handles this)
  - What if it runs late (08:45)? Still valid?

Acceptance criteria gaps:
  - "fetched from Coinbase API" - what's the specific response structure we expect?
  - "stored in Firestore" - what's the exact document structure (fields, types)?

Most critical: error handling isn't specified. That's probably covered in a later Release 1 story ("Recover from API failures"), but should this story fail gracefully or just crash?
</div>

--

<div class="myprompt">
&gt;It should certainly not just crash. We have put alerting the user that the system is broken into a separate story, but this story should at least handle failure scenarios
</div>

<div class="copilot-response">
You're right - this story needs to handle failures gracefully even if user alerting comes later. Let me update the issue to add error handling acceptance criteria.
</div>

---

<div class="myprompt">
&gt;Ok let's try adding the next story
</div>

<div class="copilot-response">
Create second steel thread story
  $ cd /Users/stephencornelius/Projects/product-copilot && gh issue create --label story --label backlog --title "Detect significant price dip" --body "## Description

As an investor, I want the system to detect when Bitcoin price has dropped significantly below recent averages, so that I can be alerted to potential buying opportunities....
    └ 53 lines...
</div>

--

!["picture of first story"](story3.png)

--

<div class="copilot-response smaller">
Created issue #3: "Detect significant price dip"

This story covers:
  - Happy path: Detects dip when z-score < -1.0
  - No dip scenario: Normal prices don't trigger detection
  - Insufficient data: Handles the first 13 days gracefully
  - Error handling: Firestore query failures don't crash

The story makes it clear:
  - The detection algorithm (z-score calculation)
  - What gets logged (dip events with all the stats)
  - Dependencies on the first story
  - The 14-day waiting period before full operation

How would you demo this one? You'd need to either wait 14 days for real data, or seed Firestore with historical data to show it detecting a dip.
</div>

--

<div class="myprompt">
&gt;Pretend you are our lead engineer. Tell me why we are struggling to demo this?
</div>

--

<div class="copilot-response smaller">
As the lead engineer, here's my concern:

We can't demo this story in isolation because:
- No visible output - The story says "log the dip event" but logging to Firestore isn't something a stakeholder can easily see. There's no UI, no alert, nothing user-facing.
- Demo requires manual inspection - To prove it works, I'd have to:
- Open GCP Console
- Navigate to Firestore
- Query the dip_events collection
- Show them a database record

That's a technical demonstration, not a business value demonstration.

The real user value comes in the next story - "Receive SMS with price info". That's when the user actually experiences something. They get an SMS on their phone. That's demoable.

So we have a choice:

- Keep stories as-is - accept that story #2 is only demoable to technical stakeholders via Firestore inspection
- Combine stories #2 and #3 - "Detect dip and send SMS alert" becomes one story. It's bigger (maybe 2-3 days), but it delivers real user value you can demo by showing an SMS on your phone.

The steel thread is supposed to be the minimal demoable slice. Right now, stories #2 and #3 together form that slice. Story #2 alone is infrastructure without user impact.

What do you think - combine them?
</div>

--

<div class="myprompt">
&gt;No I think you are off track. Fetching the price, storing it, doing the stats, sending an SMS message where required - that would be a HUGE story. It's practically 'build the application'. Think about this second story a bit harder. We were ok with showcasing data logged to our store for the first story, bearing in mind that in this case our product has no web UI. But we're struggling to work out how to demo our alerting story. 
</div>

--

<div class="copilot-response smaller">
Ah, you're right - I was conflating two different issues. Let me think this through properly.

- Story #1 (Fetch daily Bitcoin price): Easy to demo - open Firestore, show today's price record. Done.
- Story #2 (Detect significant price dip): Also easy to demo in principle - show a dip event record in Firestore. BUT...

The problem is: how do we trigger a dip for the demo?

We can't just run the function and hope there's a real dip today. We need to either:

- Seed Firestore with 14 days of synthetic data where day 15 is a dip
- Temporarily adjust the threshold to make today's price count as a dip
- Have a way to manually trigger detection with test data

Without this, we're blocked on demonstrating story #2 - not because it doesn't have value, but because we can't reliably create the conditions for a dip during a demo.

Story #3 (Receive SMS alert) has the same problem - we need a dip to occur to trigger the SMS. We can't demo the alert without being able to manufacture a dip condition.

Solution: We need testability built in - either:

- A test/demo mode that uses synthetic data
- Ability to manually trigger with injected data
- Lower the threshold temporarily for demo purposes

Is this the issue you're highlighting?
</div>

--

<div class="myprompt">
&gt;Yes now I think you are getting it. What would I typically do to demonstrate any product? I can't usually do it by waiting for real customers on live can I?
</div>

--

<div class="copilot-response smaller">
Right! You'd use test data or a demo/test environment.

For any product demo, you'd typically:

- Use a test/staging environment with synthetic data
- Have sample customers/accounts set up
- Seed the system with known scenarios that showcase the features

For our stories, we need the same approach:

Story #2 (Detect dip): 
- Seed Firestore with 14 days of test price data (e.g., prices around $95k)
- Add today's test price as $89k (a clear dip)
- Run the function
- Show the dip event appears in Firestore

Story #3 (Send SMS alert):
- Use the same test data setup
- Run the function
- Show the SMS arrives on your phone

This means we probably need to add acceptance criteria or notes about testability:
- Function should be triggerable manually (not just by scheduler)
- Should work with existing Firestore data (doesn't care if it's "real" or "test" data)
- Or: have a test mode that uses a separate collection/environment

Without this, we can't properly test OR demo these stories. Should we update the stories to explicitly address testability?
</div>

--

<div class="myprompt">
&gt;Yes
</div>

--

<div class="copilot-response smaller">
Done! Updated both stories with testability:

Story #2 (Fetch daily Bitcoin price):
- Added acceptance criteria for manual triggering
- Added demo instructions: manually trigger, check logs, verify Firestore

Story #3 (Detect significant price dip):
- Clarified function works with any data in Firestore (test or real)
- Added detailed demo instructions: how to seed test data, what scenarios to demo
- Shows both positive (dip detected) and negative (no dip) test cases

Now both stories are properly demoable without waiting for real-world conditions. The key insight: the function doesn't need to know if data is "test" or "real" - it just processes whatever is in Firestore. This means we can seed test data to create demo scenarios.
</div>
--

<div class="myprompt">
&gt;How are we distinguishing between test and real data? Let's ask our lead engineer again.
</div>

--

<div class="copilot-response smaller">
We're not distinguishing between test and real data - and that's a problem.

If I seed Firestore with 14 days of test data at $95k to demo the dip detection, then the system goes live and starts fetching real prices... now we have a mix of fake and real data in the same collection. That pollutes our production data.

Options:
- Separate Firestore collections/databases for test vs prod
  - Test: bitcoin_prices_test collection
  - Prod: bitcoin_prices collection
  - Function needs environment variable or config to know which to use
  - Clean separation, but adds complexity
- Use separate GCP projects entirely
  - Test project for demos with test data
  - Prod project for real operation
  - Cleanest separation, industry standard
  - Can demo in test environment without affecting prod
- Accept that we delete test data before going live
  - Seed test data for demo
  - Delete it all before launching the pilot
  - Simple but risky (might forget, data loss risk)
- Add a flag to each record: {...price data..., is_test: true/false}
  - Function can filter test data out of calculations
  - Keeps data mixed but marked
  - Messy

My recommendation: Option 2 - separate GCP projects. Standard practice, clean separation, no risk of contaminating prod data. We demo in the test project, run the pilot in prod.

What do you think?
</div>

--

<div class="myprompt">
&gt;I am not a lead engineer, but I think if we have only one developer then we need only dev and prod environments and we can simply use a test collection and environment variables. If we scale up we're likely to need a proper staging environment to demonstrate the latest integrated code. Right? 
</div>

--

<div class="copilot-response smaller">
You're absolutely right. For a single developer:

Dev environment:
- Uses test Firestore collections (bitcoin_prices_test, dip_events_test)
- Environment variable: ENVIRONMENT=dev or similar
- Can seed with test data freely
- Used for development and demos

Prod environment:
- Uses production collections (bitcoin_prices, dip_events)
- Environment variable: ENVIRONMENT=prod
- Real data only
- The actual 3-month pilot

Same GCP project, different collections based on environment variable. Simple and sufficient for one developer.

Later, if the team grows, you'd add:

Staging environment:
- Separate GCP project/environment
- Latest integrated code
- Used for UAT and demos to stakeholders
- Can be reset/reseeded as needed

But for now, dev + prod with collection switching is pragmatic.
</div>

---

## And so on...

---
<div class="myprompt">

## Learnings so far

 - ✅ Write instructions and templates for the AI to use
 - ❌ Do all the work and ask the AI for feedback on it
 - ✅ Ask the AI to do the work and you give feedback on it
 - ❌ Ask the AI to do a big task in one go
 - ✅ Tell it to ask you questions and build via dialogue
 - ❌ Simply correct what it gets wrong
 - ✅ Work like a coach - encourage it to think through the problem
 - ✅ Ask the AI to play roles - e.g. 'you are the QA'
 - ✅ Feed back what you learn into your instructions files
 - ✅ Embrace the command line
 - ✅ Write in machine-readable formats like markdown
  
</div>

---

<div class="myprompt">

## Next steps

**For me:**

 - Iterate on the instructions and publish them
 - See if these ideas can be applied systematically
 - Explore further


**For you:**

- Try it!

</div>

---
<div class="myprompt">

## Resources

* [Github Copilot](https://github.com/features/copilot)
* [Github CLI](https://github.com/features/copilot/cli)
* [Using the command line](https://www.makeuseof.com/tag/beginners-guide-mac-terminal/)
* [Markdown](https://www.markdownguide.org/basic-syntax/)
* [Atlassian CLI](https://www.atlassian.com/blog/jira/atlassian-command-line-interface)

* [How I AI podcast](https://www.youtube.com/watch?v=rwmR7m5rvqw) - how this PM uses AI for PRDs, JIRA tickets, and replying to coworkers
* [Teresa Torres blog](https://www.producttalk.org/how-to-choose-which-tasks-to-automate-with-ai/)  - how I choose what tasks to automate with AI

</div>