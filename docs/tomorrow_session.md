# Tomorrow's Session Guide — June 17, 2026
# Day 2 of 14-day validation experiment

---

## Before Opening Any Terminal

Do these manually, in order:

1. **Post the LinkedIn post** — open `docs/linkedin_post.md`, copy Version A, post it on LinkedIn. Do this first, before any build work. It takes 3 minutes.
2. **Check if anyone responded to yesterday's posts or existing connections** — note any names.
3. Open two terminals: Terminal 1 for AICOS, Terminal 2 for MilanGPT-OS.

---

## TERMINAL 1 — AICOS
### `C:\Users\milan\Documents\aicos`

Paste this prompt at the start of the session:

```
Open AICOS project at C:\Users\milan\Documents\aicos.
Read CLAUDE.md first before anything else.

This is the AI Chief of Staff service I built yesterday — a done-for-you
daily brief and weekly synthesis for paying builders.

Today's priorities for this project:

1. LINKEDIN RESPONSE PREP
   I posted the LinkedIn post this morning (docs/linkedin_post.md Version A).
   Help me write 3 short DM replies for different scenarios:
     a) Someone says "interested, tell me more"
     b) Someone says "how does this work?"
     c) Someone says "sounds good, what's the price?"
   Each reply should be under 4 sentences. No links. Move toward a 20-min call.

2. IF I HAVE A LEAD WITH A NAME
   Tell me their name and run: python scripts\onboard_client.py
   I'll have their details ready.

3. PROSPECT TARGETING (if no inbound yet)
   Help me write 5 personalised short DMs to send directly to specific people
   I'll name from my LinkedIn connections. These should NOT look like the post.
   They should be 2-3 sentences, reference something specific about that person,
   and ask one question.

Do NOT build anything new. No new scripts, no new features. Today is sales only.
```

---

## TERMINAL 2 — MilanGPT-OS
### `C:\Users\milan\Documents\MilanGPT-OS`

Paste this prompt at the start of the session:

```
Open MilanGPT-OS at C:\Users\milan\Documents\MilanGPT-OS.
Read CLAUDE.md first. This is my personal AI operating system, NOT the AICOS project.

Run the morning routine:
  python scripts\daily_command_center.py
  python scripts\safety_scan.py

Today is Day 2 of the 14-day validation experiment.

Two tasks for this project today:

TASK 1 — Redirect RA-001 and RA-002
The existing revenue actions in data/inputs/revenue_actions.yaml point to the
"AI Operations Automation Starter Package" — a logistics-focused offer I'm no
longer pursuing. I've pivoted to AICOS (AI Chief of Staff service for builders
at C:\Users\milan\Documents\aicos — separate project, do not mix).

Update RA-001 and RA-002 to reflect this:
- New linked offer: AICOS — AI Chief of Staff for Builders
- New next_step for RA-001: Privately identify 3 warm prospects for AICOS
  (builders, indie hackers, consultants, small agency owners in my network
  who would benefit from a daily AI brief and weekly synthesis)
- New due dates: RA-001 today, RA-002 tomorrow
Do NOT commit private prospect names. The tracking entry in revenue_actions.yaml
is fine to commit; real prospect details stay local and private.

TASK 2 — Record today's validation entry
After I've used MilanGPT OS for at least one real task or decision today, run:
  python scripts\daily_validation_entry.py
Score it honestly (0-3). Today should score 2+ because I redirected revenue
actions based on agent output — that is the system working as designed.

Do NOT add new assets, do NOT change the dashboard, do NOT start any build work
in this project today.
```

---

## If Sui/Walrus Produces a Result (Terminal 2)

If the Sui/Walrus build in `C:\Users\milan\Documents\exp-sui-walrus` produces
a result, summarise it back here:

```
I have a Sui/Walrus result from the other terminal. Here it is:
[paste only the outcome — what worked, what failed, what the next step is]

Help me record this as a handoff note in MilanGPT OS without including
any raw Speedex or client data. Then update the validation entry if relevant.
```

---

## End of Day Checklist

Before closing terminals:

- [ ] LinkedIn post is live
- [ ] At least 1 DM sent (inbound reply or outbound direct)
- [ ] RA-001 and RA-002 updated in MilanGPT-OS revenue_actions.yaml
- [ ] Validation entry recorded: `python scripts\daily_validation_entry.py`
- [ ] No private prospect names committed to git in either project

---

## What NOT to Do Tomorrow

- Do not build new AICOS features — the service is complete enough to sell
- Do not build new MilanGPT-OS assets — the experiment needs data, not more infrastructure
- Do not mix the two projects in one terminal session
- Do not send a follow-up LinkedIn post — it is too soon
- Do not start Sui/Walrus work in Terminal 1 or 2 — that is its own context
