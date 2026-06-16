# Client Onboarding Guide

This is Milan's step-by-step process for onboarding a new AICOS client.
Follow this exactly. Do not skip steps.

---

## Step 1 — Confirm the Client

Before running any scripts:

- [ ] Client has agreed to the price and tier in writing (message or email)
- [ ] You have their full name, company, and preferred contact channel
- [ ] You know their timezone and preferred delivery time
- [ ] First payment is confirmed or invoiced

---

## Step 2 — Assign a Client ID

Client IDs are sequential: CLIENT-001, CLIENT-002, etc.

Check `config/clients.yaml` for the last assigned ID and use the next one.

---

## Step 3 — Run the Onboarding Script

```powershell
cd C:\Users\milan\Documents\aicos
python scripts\onboard_client.py
```

The script will:
1. Ask you for all client details
2. Create `data/clients/CLIENT-XXX/context.yaml` with what you entered
3. Create `data/clients/CLIENT-XXX/run_log.yaml` (empty)
4. Add the client to `config/clients.yaml`
5. Optionally run a test brief so you can review quality before delivering

---

## Step 4 — Fill the Context File Thoroughly

Open `data/clients/CLIENT-XXX/context.yaml` and make sure every field is filled properly.

The brief quality is entirely determined by the context quality. Vague context produces vague briefs.

**What to do if you do not have enough context:**
- Send the client a short intake form (3-5 questions max)
- Or spend 30 minutes on a call and take notes directly into the YAML

Minimum acceptable context to generate a good brief:
- At least 3 specific goals
- At least 2 current projects with their status
- At least 1 challenge or blocker
- Operating style described in one honest sentence

---

## Step 5 — Generate and Review the First Brief

```powershell
python scripts\run_client_brief.py CLIENT-XXX
```

Read the output carefully:
- Does it reference their actual goals, not generic ones?
- Are the 3 priorities specific to their real situation?
- Is the decision framing relevant to something they are actually facing?
- Would you be proud to send this?

If no: update `context.yaml` and rerun. Do not deliver a generic brief.

---

## Step 6 — Deliver the First Brief

Deliver via their chosen channel (email, Slack, or WhatsApp).

Template for the first delivery:

```
Hi [Name],

Welcome to AICOS. Here is your first daily brief.

I have based this on the context you gave me. As I learn more about 
your situation, the output will get sharper. If anything feels off 
or needs adjusting, just reply and I will update your context.

[paste brief here]

Milan
```

---

## Step 7 — Confirm the Delivery Schedule

Send one follow-up message after the first brief:

```
Quick note on the schedule:
- Daily brief: weekdays before [their delivery time]
- Weekly synthesis: every Friday before 5pm [their timezone]
- [If Professional/Executive: monthly review on the last Friday of each month]

Reply any time if your priorities shift and I need to update your context.
```

---

## Step 8 — Log the Onboarding

Update `config/clients.yaml` to set `status: active`.

Make a note in your own MilanGPT OS validation log if this was a real revenue event.

---

## Ongoing: Weekly Rhythm

Every weekday morning (before the delivery time):
1. `python scripts\run_client_brief.py CLIENT-XXX`
2. Read it. Is it grounded and specific?
3. Deliver.

Every Friday:
1. `python scripts\run_weekly_synthesis.py CLIENT-XXX`
2. Read it. Does it reflect the real week?
3. Deliver.

Every month (Professional/Executive):
1. Update context with anything that changed this month
2. Run monthly review (same script as weekly synthesis, pass `--monthly` flag)
3. Deliver with a personal note
