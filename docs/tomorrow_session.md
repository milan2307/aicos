# Tomorrow's Session Guide — June 17, 2026
# Day 2 of the 14-day validation experiment
# Three active projects. Three terminals. No mixing.

---

## The Three Projects

| | Project | Path | What gets built |
|---|---|---|---|
| T1 | **MilanGPT-OS** | `C:\Users\milan\Documents\MilanGPT-OS` | Personal AI OS — refinement, A016 toward 100% |
| T2 | **AICOS** | `C:\Users\milan\Documents\aicos` | Commercial service — sales and first client |
| T3 | **Sui/Walrus** | `C:\Users\milan\Documents\exp-sui-walrus` | Blockchain build — TradeProof v0.1 |

---

## Before Opening Any Terminal (5 minutes)

1. **Post the LinkedIn post** — `aicos/docs/linkedin_post.md` Version A. Do this first. It takes 3 minutes and is the highest-leverage action of the day.
2. Check for any replies to existing posts or DMs.
3. Open three terminals.

---

## TERMINAL 1 — MilanGPT-OS
### `C:\Users\milan\Documents\MilanGPT-OS`
### Purpose: Refine and improve the OS itself

**What this project is:** Your personal AI operating system. You love it and want to keep building it. It is not a morning-routine-only project — it is an active, evolving build.

**Tomorrow's build focus:** A016 is at 45%. The queue write-back (ET-005) is done but basic. The next meaningful improvement is making the daily loop smarter — specifically, making the morning command center show *what changed since yesterday* and *what is at risk today*, not just static priorities.

**Paste this prompt to start the session:**

```
Open MilanGPT-OS at C:\Users\milan\Documents\MilanGPT-OS.
Read CLAUDE.md first. This is my personal AI OS — separate from AICOS and Sui/Walrus.

Run the morning routine:
  python scripts\daily_command_center.py
  python scripts\safety_scan.py
  python scripts\next_priority.py --os-only

Three things for this project today:

1. REDIRECT REVENUE ACTIONS
   Update data/inputs/revenue_actions.yaml:
   RA-001 and RA-002 currently point to "AI Operations Automation Starter Package"
   (logistics offer I'm no longer pursuing). Redirect them to AICOS prospects —
   builders, indie hackers, consultants who want an AI Chief of Staff.
   No private names in the committed file.

2. BUILD — Improve the daily command center
   A016 is 45% complete. The most useful next improvement is making
   daily_command_center.py show "what changed since yesterday" by comparing
   today's validation log and asset state with the previous day.
   This closes the biggest gap in the morning routine — right now it shows
   status but not momentum or drift.

3. RECORD VALIDATION ENTRY
   After doing at least one real task with the OS today:
     python scripts\daily_validation_entry.py
   Score it honestly (0–3). The redirect of revenue actions based on agent
   output should count as a real OS-driven decision.

Do not touch AICOS data. Do not touch Sui/Walrus files.
If the Sui/Walrus terminal produces a result, paste only the outcome here
to summarise into MilanGPT OS — no raw client or Speedex data.
```

---

## TERMINAL 2 — AICOS
### `C:\Users\milan\Documents\aicos`
### Purpose: Sell the service and get the first client

**What this project is:** Done-for-you AI Chief of Staff for builders. The code is complete. Today is sales only — no new scripts, no new features.

**Tomorrow's focus:** The LinkedIn post goes live. Prep for the first DM response. If someone responds, onboard them immediately.

**Paste this prompt to start the session:**

```
Open AICOS at C:\Users\milan\Documents\aicos.
Read CLAUDE.md first. This is the commercial AI Chief of Staff service —
separate from MilanGPT-OS and Sui/Walrus. Do not mix them.

The LinkedIn post went live this morning (docs/linkedin_post.md Version A).

Three things for this project today:

1. RESPONSE PLAYBOOK
   Write 3 short DM replies for these scenarios:
     a) "Interested, tell me more"
     b) "How does this work exactly?"
     c) "What's the price?"
   Each reply: under 4 sentences, no links, move toward a 20-minute call.

2. OUTBOUND (if no inbound yet)
   I'll give you 3-5 names of LinkedIn connections who could be good AICOS clients
   (builders, indie founders, consultants).
   Write a personalised 2-3 sentence DM for each. No copy-paste template —
   each one should reference something specific about that person.

3. FIRST CLIENT ONBOARDING (if someone said yes)
   Run: python scripts\onboard_client.py
   I'll have their name, company, goals, and delivery preference ready.

Do not build anything new. No new scripts. No new features.
```

---

## TERMINAL 3 — Sui/Walrus
### `C:\Users\milan\Documents\exp-sui-walrus`
### Purpose: Build TradeProof v0.1

**What this project is:** Sui blockchain + Walrus storage build. BT-003 is the active task. This runs independently of the other two projects.

**Tomorrow's focus:** Continue the TradeProof build. Capture any result and summarise it back into MilanGPT-OS Terminal 1 at end of day.

**Paste this prompt to start the session:**

```
Open the Sui/Walrus project at C:\Users\milan\Documents\exp-sui-walrus.
This is the blockchain build project — separate from MilanGPT-OS and AICOS.
Do not mix them.

Active task: BT-003 — TradeProof v0.1
Acceptance criteria:
  - sui --version works in PowerShell
  - walrus --version works in PowerShell
  - Existing logioracle Move package builds or build errors are captured
  - TradeProof v0.1 scope is documented
  - At least one Move test exists for proof creation or shipment status

Start by checking the current state of the repo and telling me exactly
where we left off and what the next concrete step is.
```

**When the session ends or produces a result:**
Switch to Terminal 1 (MilanGPT-OS) and paste:
```
The Sui/Walrus terminal produced this result: [outcome only, no client data]
Help me record this as a handoff note in MilanGPT OS.
```

---

## End of Day Checklist

- [ ] LinkedIn post live (AICOS)
- [ ] At least 1 DM sent or replied to (AICOS)
- [ ] RA-001 and RA-002 redirected to AICOS offer (MilanGPT-OS)
- [ ] Daily command center improvement started or scoped (MilanGPT-OS)
- [ ] Validation entry recorded — `python scripts\daily_validation_entry.py` (MilanGPT-OS)
- [ ] Sui/Walrus result summarised into MilanGPT-OS if applicable (Terminal 3 → Terminal 1)
- [ ] No private names or client data committed in any project

---

## The Rule Across All Three

Each terminal is its own universe. When Claude Code is open in one terminal,
it only knows about that project. The CLAUDE.md in each project enforces this.
Never paste context from one project into another session.
