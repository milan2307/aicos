# AICOS — AI Chief of Staff Service

A done-for-you AI Chief of Staff for ambitious solo builders and entrepreneurs.

## What It Is

Other entrepreneurs want what Milan built in MilanGPT OS — a daily AI brief, weekly opportunity synthesis, and a strategic system running in the background — but they cannot build it themselves.

AICOS delivers that as a service. Milan runs AI agents customised to each client's goals and context, reviews the outputs, and delivers them on a fixed schedule.

**This is a commercial project, separate from MilanGPT OS.**

## What Clients Get

- **Daily brief** — top 3 priorities for today, one decision to make, one strategic note
- **Weekly synthesis** — progress review, what is working, what is stalling, next week priorities
- **Monthly review** *(Professional and Executive tiers)* — strategic health check against 90-day goals

## How to Run

```powershell
# Dashboard: see all clients
python scripts\client_dashboard.py

# Onboard a new client
python scripts\onboard_client.py

# Generate a daily brief
python scripts\run_client_brief.py CLIENT-001

# Generate a weekly synthesis
python scripts\run_weekly_synthesis.py CLIENT-001
```

## Requirements

```
pip install -r requirements.txt
```

Set `ANTHROPIC_API_KEY` as an environment variable before running any script.

## Project Separation

This project is intentionally isolated from MilanGPT OS.

- MilanGPT OS: `C:\Users\milan\Documents\MilanGPT-OS` — Milan's personal system
- AICOS: `C:\Users\milan\Documents\aicos` — commercial client service

Never import between them. Never reference one from the other.
