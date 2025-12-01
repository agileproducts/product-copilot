# Using Github Copilot for product management and business analysis

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

]]

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