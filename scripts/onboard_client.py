"""AICOS client onboarding — interactive CLI to add a new client."""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

if os.name == "nt" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENTS_FILE = ROOT_DIR / "config" / "clients.yaml"
CLIENTS_DIR = ROOT_DIR / "data" / "clients"

if os.name == "nt":
    os.system("")

_COLOR = hasattr(sys.stdout, "isatty") and bool(sys.stdout.isatty())


def _c(code: str) -> str:
    return code if _COLOR else ""


RST  = _c("\033[0m")
BOLD = _c("\033[1m")
DIM  = _c("\033[2m")
CYN  = _c("\033[36m")
GRN  = _c("\033[92m")
YLW  = _c("\033[93m")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"  {BOLD}{prompt}{RST}{suffix}: ").strip()
    return value if value else default


def ask_list(prompt: str, hint: str = "Enter one per line. Empty line to finish.") -> list[str]:
    print(f"  {BOLD}{prompt}{RST}  {DIM}({hint}){RST}")
    items = []
    while True:
        line = input("    → ").strip()
        if not line:
            break
        items.append(line)
    return items


def next_client_id() -> str:
    registry = load_yaml(CLIENTS_FILE)
    clients = registry.get("clients", [])
    if not isinstance(clients, list) or not clients:
        return "CLIENT-001"
    existing_ids = [c.get("client_id", "") for c in clients]
    nums = []
    for cid in existing_ids:
        try:
            nums.append(int(str(cid).replace("CLIENT-", "")))
        except ValueError:
            pass
    next_num = max(nums) + 1 if nums else 1
    return f"CLIENT-{next_num:03d}"


def main() -> int:
    print()
    print(f"  {BOLD}AICOS — New Client Onboarding{RST}")
    print(f"  {DIM}This creates a local context file for a new client.{RST}")
    print(f"  {DIM}Real client data is gitignored and never committed.{RST}")
    print()

    client_id = next_client_id()
    print(f"  Assigned client ID: {CYN}{client_id}{RST}")
    print()

    # Basic info
    print(f"  {BOLD}── Basic Info ─────────────────────────────────{RST}")
    name    = ask("Client full name")
    company = ask("Company or project name")
    role    = ask("Their role", "Founder")
    industry = ask("Industry / niche")
    tier    = ask("Plan tier", "starter").lower()
    channel = ask("Delivery channel (email / slack / whatsapp)", "email")
    tz      = ask("Timezone", "UTC")
    dtime   = ask("Preferred delivery time (24h)", "07:00")
    print()

    # Goals
    print(f"  {BOLD}── Goals (next 90 days) ────────────────────────{RST}")
    print(f"  {DIM}Be specific. 'Grow revenue' is useless. 'Close 3 clients at $2k/month' is useful.{RST}")
    goals = ask_list("What does this client want to achieve?")
    print()

    # Current projects
    print(f"  {BOLD}── Current Projects ───────────────────────────{RST}")
    projects: list[dict[str, str]] = []
    while True:
        proj_name = ask("Project name (or press Enter to finish)")
        if not proj_name:
            break
        proj_status = ask("  Status", "active")
        proj_goal   = ask("  What is the goal of this project?")
        projects.append({"name": proj_name, "status": proj_status, "goal": proj_goal, "notes": ""})
    print()

    # Challenges
    print(f"  {BOLD}── Challenges and Blockers ─────────────────────{RST}")
    print(f"  {DIM}What is genuinely slowing them down?{RST}")
    challenges = ask_list("List their real challenges")
    print()

    # Operating style
    print(f"  {BOLD}── Operating Style ────────────────────────────{RST}")
    print(f"  {DIM}e.g. 'Decisive, skip context, give options' or 'Strategic, wants the why first'{RST}")
    style = ask("How do they prefer to receive information?")
    print()

    # Background
    print(f"  {BOLD}── Background ─────────────────────────────────{RST}")
    print(f"  {DIM}Domain expertise, constraints, unique context.{RST}")
    background = ask("Any background that helps generate better outputs?")
    print()

    # Standing instructions
    standing = ask("Any standing instructions? (press Enter to skip)")
    print()

    # Build context dict
    context: dict[str, Any] = {
        "client_id": client_id,
        "name": name,
        "company": company,
        "role": role,
        "industry": industry,
        "start_date": date.today().isoformat(),
        "plan_tier": tier,
        "status": "active",
        "goals": goals,
        "current_projects": projects,
        "challenges": challenges,
        "operating_style": style,
        "background": background,
        "standing_instructions": standing,
        "delivery_channel": channel,
        "delivery_time": dtime,
        "timezone": tz,
    }

    # Save context file
    context_path = CLIENTS_DIR / client_id / "context.yaml"
    save_yaml(context_path, context)

    # Save empty run log
    log_path = CLIENTS_DIR / client_id / "run_log.yaml"
    save_yaml(log_path, {"client_id": client_id, "runs": []})

    # Update client registry (config/clients.yaml only has safe metadata)
    registry = load_yaml(CLIENTS_FILE)
    clients_list = registry.get("clients", [])
    if not isinstance(clients_list, list):
        clients_list = []
    clients_list.append({
        "client_id": client_id,
        "tier": tier,
        "status": "active",
        "start_date": date.today().isoformat(),
        "billing_day": 1,
        "delivery_channel": channel,
        "delivery_time": dtime,
        "timezone": tz,
    })
    save_yaml(CLIENTS_FILE, {"clients": clients_list})

    print(f"  {GRN}✓ Client {client_id} created.{RST}")
    print(f"  {DIM}Context: {context_path.relative_to(ROOT_DIR)}{RST}")
    print(f"  {DIM}Log:     {log_path.relative_to(ROOT_DIR)}{RST}")
    print()

    # Offer to run a test brief
    run_test = ask("Run a test brief now to review quality? (y/n)", "y").lower()
    if run_test == "y":
        print()
        result = subprocess.call(
            [sys.executable, str(ROOT_DIR / "scripts" / "run_client_brief.py"), client_id],
            cwd=ROOT_DIR,
        )
        if result != 0:
            print(f"  {YLW}Brief generation failed. Check ANTHROPIC_API_KEY and context file.{RST}")
    else:
        print(f"  Run when ready: {CYN}python scripts\\run_client_brief.py {client_id}{RST}")

    print()
    print(f"  {BOLD}Next steps:{RST}")
    print(f"  1. Review context file and fill any gaps: {CYN}{context_path.relative_to(ROOT_DIR)}{RST}")
    print(f"  2. Read onboarding guide: {CYN}docs\\onboarding.md{RST}")
    print(f"  3. Deliver first brief via {channel}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
