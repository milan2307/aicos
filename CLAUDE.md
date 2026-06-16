# AICOS — AI Chief of Staff Service

## CRITICAL: What This Project Is and Is Not

**This is NOT MilanGPT OS.**

| | MilanGPT OS | AICOS |
|---|---|---|
| Location | `C:\Users\milan\Documents\MilanGPT-OS` | `C:\Users\milan\Documents\aicos` |
| Purpose | Milan's personal AI operating system | Commercial service sold to other builders |
| Clients | Milan only | External paying clients |
| Git remote | github.com/milan2307/MilanGPT-OS | github.com/milan2307/aicos |
| Data | Milan's goals, assets, opportunities | Client context files (private, gitignored) |

**Never mix these two projects. Never import from one into the other. Never reference MilanGPT-OS paths in this codebase.**

---

## What AICOS Does

AICOS is a done-for-you AI Chief of Staff service for ambitious solo builders and entrepreneurs.

**What a client pays for:**
- Daily AI brief: top 3 priorities, one decision to make, one strategic note
- Weekly synthesis: progress review, what's working, what's stalling, next week priorities
- Monthly review: strategic health check against their 90-day goals

**What Milan does:**
- Onboards clients using `scripts/onboard_client.py`
- Runs briefs using `scripts/run_client_brief.py <CLIENT-ID>`
- Reviews output before delivering to the client
- Delivers via their chosen channel (email / Slack / WhatsApp)

**What Claude does:**
- Reads the client's context file
- Generates the brief, synthesis, and review via API
- All outputs are in `data/outputs/<CLIENT-ID>/`

---

## Pricing

| Tier | Price | What They Get |
|------|-------|---------------|
| Starter | $299/month | Daily brief + weekly synthesis |
| Professional | $499/month | Daily brief + weekly synthesis + monthly review + 1 async Q&A/week |
| Executive | $799/month | All above + 30-min monthly call with Milan |

Target: 10 clients at Starter = $2,990/month MRR.

---

## Project Structure

```
aicos/
├── CLAUDE.md               ← you are here
├── README.md
├── requirements.txt        ← anthropic, pyyaml
├── config/
│   └── clients.yaml        ← client registry (IDs and tier only, no PII)
├── data/
│   ├── clients/
│   │   ├── CLIENT_TEMPLATE.yaml   ← committed schema template
│   │   └── CLIENT-XXX/            ← gitignored — real client context lives here
│   │       ├── context.yaml
│   │       └── run_log.yaml
│   └── outputs/                   ← gitignored — generated briefs and reports
│       └── CLIENT-XXX/
│           └── YYYY-MM-DD_brief.md
├── docs/
│   ├── offer.md            ← what the service is and what clients get
│   ├── pricing.md          ← pricing tiers and positioning
│   ├── onboarding.md       ← step-by-step for Milan to onboard a new client
│   └── linkedin_post.md    ← ready-to-post first marketing content
└── scripts/
    ├── client_dashboard.py       ← view all clients and their status
    ├── onboard_client.py         ← interactive CLI to add a new client
    ├── run_client_brief.py       ← generate daily brief for one client
    └── run_weekly_synthesis.py   ← generate weekly synthesis for one client
```

---

## Environment

- **Python:** 3.x
- **API key:** `ANTHROPIC_API_KEY` environment variable — same key as MilanGPT-OS, never hardcoded
- **Model:** `claude-haiku-4-5-20251001` for briefs, `claude-sonnet-4-6` for monthly reviews
- **OS:** Windows 11, PowerShell

---

## How to Run

```powershell
# See all clients and their status
python scripts\client_dashboard.py

# Add a new client
python scripts\onboard_client.py

# Generate today's brief for a client
python scripts\run_client_brief.py CLIENT-001

# Generate weekly synthesis for a client
python scripts\run_weekly_synthesis.py CLIENT-001
```

---

## Privacy Rules

- **Never commit real client names, companies, emails, or personal details**
- `data/clients/CLIENT_TEMPLATE.yaml` is the only client file committed
- All real client context goes in `data/clients/CLIENT-XXX/context.yaml` (gitignored)
- All outputs go in `data/outputs/` (gitignored)
- The `config/clients.yaml` registry contains only client IDs, tiers, and start dates — no PII

---

## Current Status

| Metric | Value |
|--------|-------|
| Clients | 0 |
| MRR | $0 |
| Target | 3 clients / $897+ MRR in 30 days |
| First action | Publish `docs/linkedin_post.md` on LinkedIn |
