# User Story Guidelines

## Purpose

These guidelines help us identify and write effective user stories that are clear, valuable, and actionable. They draw on proven practices from Cohn and Patton whilst acknowledging modern realities of distributed teams, continuous delivery, and the need for clarity.

## What Makes a Good User Story?

### Essential Qualities (The Core Three)

**Valuable:** Every story must deliver tangible value to a user or stakeholder. Avoid technical tasks disguised as stories. Ask "what can the user do after this story that they couldn't do before?"

**Small:** Stories should be completable in a few days at most. If a story feels large, split it. Small stories flow faster through the system, provide quicker feedback, and reduce risk.

**Testable:** You must be able to write clear tests that verify the story is complete. If you can't define success criteria, the story is too vague or needs more analysis.

### Supporting Qualities

**Clear and well-defined:** Stories need sufficient detail before development begins. "Negotiable" doesn't mean "vague". Implementation details can be worked out, but the problem, context, and acceptance criteria should be clear. This is especially important for distributed teams.

**Acknowledges dependencies:** Some stories naturally depend on others. Don't pretend otherwise. Use your story map to sequence work logically. Dependencies aren't failures - they're reality.

## Story Format

### Title
Use a brief, action-oriented title that describes what the user does or receives:
- ✅ "Receive SMS alert with price information"
- ✅ "View price history and dip events"
- ❌ "Implement SMS integration" (technical task, not user value)
- ❌ "Configure Twilio" (infrastructure task, not a story)

### Acceptance Criteria (Given/When/Then)
Use BDD format to specify clear, testable conditions:

```
GIVEN [context/precondition]
WHEN [action or trigger]
THEN [expected outcome]
```

Example:
```
GIVEN a dip is detected (price >1σ below 14-day mean)
WHEN the alert is sent
THEN I receive an SMS within 30 minutes
AND the SMS includes current price, mean, and standard deviation
AND the alert is logged in Firestore
```

Multiple scenarios can be added as additional Given/When/Then blocks if needed.

### Additional Context (Optional)
Include any background, constraints, or technical notes that help the team understand the story. But keep it brief - details can be discussed during planning.

## Identifying Stories Using Story Mapping

### 1. Start with User Activities (Top Row)
What are the high-level things users do? These become the columns of your story map.
- Keep them user-centric and sequential
- Think "what's the user's journey?"
- Example: "Collect Price Data → Identify Dips → Receive Alerts"

### 2. Define the Steel Thread (First Row of Stories)
The steel thread is the minimal end-to-end slice that delivers complete user value. It should:
- Flow horizontally across all activities (left to right)
- Touch every layer of the architecture
- Deliver something a user can actually use (even if basic)
- Be deployable and testable

This is your walking skeleton - prove the system works end-to-end before adding enhancements.

### 3. Add Depth (Stories Below the Steel Thread)
Once you have the steel thread, add stories underneath each activity that:
- Enhance the basic functionality
- Handle edge cases and error conditions
- Improve usability or performance
- Add robustness and completeness

Stories further down are lower priority - they can wait until after the steel thread is proven.

### 4. Draw Release Lines
Horizontal lines across your story map define releases:
- Everything above the first line = Steel thread / Walking skeleton
- Everything above the second line = Release 1 / MVP
- Below that = Future iterations

## Story Splitting Techniques

When a story is too large, try these splitting patterns:

**By workflow steps:** Break a process into sequential steps
- Example: "Register and verify account" → "Enter registration details", "Verify email address"

**By simple/complex:** Start with the simple case, handle complex cases later
- Example: "Detect dips" → "Detect using basic threshold", "Add historical context"

**By happy path/edge cases:** Implement the main scenario first, error handling second
- Example: "Send alert" → "Send SMS when service available", "Retry on transient failures"

**By data variations:** Different types or sources of data
- Example: "Fetch price data" → "Fetch from Coinbase", "Fallback to alternative API"

**By performance/quality:** Basic functionality first, then non-functional improvements
- Example: "Store price data" → "Store to Firestore", "Optimize query performance"

**Horizontally (through the stack):** Cut thin vertical slices rather than horizontal layers
- ✅ "Display last 7 days of prices" (database → API → UI)
- ❌ "Build price history database tables" (just one layer, no user value)

## What Is NOT a Story

**Infrastructure tasks:** "Set up GCP project", "Configure CI/CD pipeline", "Deploy to production"
- These are tasks that support stories but don't deliver user value directly
- Track them as "Iteration 0" prerequisites or as tasks within stories

**Technical refactoring:** "Refactor calculation module", "Optimize database queries"
- Unless they directly enable user value, these are technical tasks
- Consider: what user story does this enable or improve?

**Testing activities:** "Write unit tests", "Perform end-to-end testing"
- Testing is part of every story (we practice TDD)
- Don't create separate test stories

**Generic maintenance:** "Update dependencies", "Fix technical debt"
- These might be tasks within a sprint but aren't user stories
- If they're critical, frame them as enabling value: "Upgrade library to enable secure payments"

## Labels and Workflow

Stories should progress through these states using GitHub labels:

**backlog:** Story identified but not yet detailed. May be just a title or placeholder.

**ready for dev:** Story is fully defined with clear acceptance criteria, dependencies identified, and team understands the work. Ready to be picked up.

**in development:** Story is actively being worked on by the team.

## Guidelines for "Ready for Dev"

A story is ready for development when:

- [ ] Title clearly describes user value
- [ ] Acceptance criteria written in Given/When/Then format
- [ ] Team understands what "done" looks like
- [ ] Dependencies identified and either complete or acknowledged
- [ ] Any required design, research, or decisions are complete
- [ ] Story is small enough to complete in a few days
- [ ] No obvious blocking questions remain

## Anti-Patterns to Avoid

❌ **Vague stories:** "As a user, I want better performance" - What does better mean? How do you test it?

❌ **Technical stories:** "As a developer, I want to refactor the database" - No user value

❌ **Too large:** "As a user, I want a complete dashboard" - This is an epic, split it

❌ **Implementation-focused:** "Implement REST API endpoint" - Describe user value, not technical solution

❌ **Missing acceptance criteria:** "As a user, I want to see alerts" - How? When? What's included?

## Examples

### Good Story
**Title:** Receive SMS alert with price information

**Acceptance Criteria:**
```
GIVEN a dip is detected (price >1σ below 14-day mean)
WHEN the alert is sent at 08:30 London time
THEN I receive an SMS
AND the SMS includes current price, 14-day mean, and standard deviation
AND the SMS is delivered within 30 minutes
AND the alert delivery is logged in Firestore
```

**Notes:** Use Twilio for SMS delivery. If SMS fails, email fallback should trigger (separate story).

### Poor Story (Fixed)

❌ **Original:** "Set up Twilio integration"
- Problem: Technical task, no user value, not testable from user perspective

✅ **Fixed:** "Receive SMS alert with price information" (as above)
- The Twilio setup becomes a task within this story

---

## Summary

Good user stories are:
- **Valuable** - users can do something they couldn't before
- **Small** - completable in days, not weeks
- **Testable** - clear acceptance criteria using Given/When/Then
- **Clear** - well-defined before development starts
- **Sequenced logically** - dependencies acknowledged and respected

Use story mapping to identify your steel thread first, then add depth. Draw release lines to define your MVP and future iterations.

Remember: stories are about delivering value to users, not about documenting technical tasks or architecture.
