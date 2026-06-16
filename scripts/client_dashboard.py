"""AICOS client dashboard — view all clients and their delivery status."""

from __future__ import annotations

import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

if os.name == "nt" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENTS_FILE = ROOT_DIR / "config" / "clients.yaml"
CLIENTS_DIR = ROOT_DIR / "data" / "clients"
OUTPUTS_DIR = ROOT_DIR / "data" / "outputs"

_COLOR = hasattr(sys.stdout, "isatty") and bool(sys.stdout.isatty())
if os.name == "nt":
    os.system("")


def _c(code: str) -> str:
    return code if _COLOR else ""


RST  = _c("\033[0m")
BOLD = _c("\033[1m")
DIM  = _c("\033[2m")
GRN  = _c("\033[92m")
YLW  = _c("\033[93m")
CYN  = _c("\033[36m")
RED  = _c("\033[31m")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def last_output(client_id: str, output_type: str) -> str:
    """Return the date of the most recent output of a given type, or 'Never'."""
    output_dir = OUTPUTS_DIR / client_id
    if not output_dir.exists():
        return f"{RED}Never{RST}"
    pattern = f"*_{output_type}.md"
    files = sorted(output_dir.glob(pattern), reverse=True)
    if not files:
        return f"{RED}Never{RST}"
    mtime = datetime.fromtimestamp(files[0].stat().st_mtime)
    today = date.today()
    if mtime.date() == today:
        return f"{GRN}Today {mtime.strftime('%H:%M')}{RST}"
    delta = (today - mtime.date()).days
    if delta == 1:
        return f"{YLW}Yesterday{RST}"
    return f"{YLW}{mtime.strftime('%b %d')}{RST}"


def run_log_summary(client_id: str) -> tuple[int, int]:
    """Return (total_runs, runs_this_month)."""
    log_path = CLIENTS_DIR / client_id / "run_log.yaml"
    data = load_yaml(log_path)
    runs = data.get("runs", [])
    if not isinstance(runs, list):
        return 0, 0
    total = len(runs)
    this_month = date.today().strftime("%Y-%m")
    monthly = sum(1 for r in runs if str(r.get("date", "")).startswith(this_month))
    return total, monthly


def status_color(status: str) -> str:
    s = status.lower()
    if s == "active":
        return f"{GRN}{status}{RST}"
    if s == "paused":
        return f"{YLW}{status}{RST}"
    return f"{RED}{status}{RST}"


def tier_color(tier: str) -> str:
    t = tier.lower()
    if t == "executive":
        return f"{CYN}{tier}{RST}"
    if t == "professional":
        return f"{YLW}{tier}{RST}"
    return f"{DIM}{tier}{RST}"


def rule(width: int = 72) -> None:
    print(f"{DIM}{'═' * width}{RST}")


def main() -> None:
    registry = load_yaml(CLIENTS_FILE)
    clients = registry.get("clients", [])

    today_str = date.today().strftime("%a %b %d, %Y")
    active = [c for c in clients if str(c.get("status", "")).lower() == "active"]
    mrr = sum(
        {"starter": 299, "professional": 499, "executive": 799}.get(
            str(c.get("tier", "")).lower(), 0
        )
        for c in active
    )

    rule()
    print(f"  {BOLD}AICOS  ·  AI Chief of Staff Service{RST}  ·  {DIM}{today_str}{RST}")
    rule()

    print(f"\n  {BOLD}Clients:{RST} {len(active)} active   {BOLD}MRR:{RST} {GRN}${mrr}/month{RST}   {BOLD}Target:{RST} {DIM}$897 (3 clients){RST}\n")

    if not clients:
        print(f"  {DIM}No clients yet.{RST}")
        print(f"\n  First action: publish {CYN}docs/linkedin_post.md{RST} on LinkedIn.")
        print(f"  Then run:     {CYN}python scripts\\onboard_client.py{RST}\n")
        rule()
        return

    # Header
    print(f"  {DIM}{'ID':<14} {'Name':<20} {'Tier':<14} {'Status':<10} {'Last Brief':<18} {'Last Synthesis':<18} {'Runs'}{RST}")
    print(f"  {'─' * 100}")

    for c in sorted(clients, key=lambda x: x.get("client_id", "")):
        cid = c.get("client_id", "?")
        context = load_yaml(CLIENTS_DIR / cid / "context.yaml")
        name = context.get("name", f"{DIM}[context missing]{RST}")
        tier = tier_color(str(c.get("tier", "?")))
        status = status_color(str(c.get("status", "?")))
        last_brief = last_output(cid, "brief")
        last_synth = last_output(cid, "synthesis")
        total_runs, monthly_runs = run_log_summary(cid)
        runs_str = f"{total_runs} total ({monthly_runs} this month)"
        print(f"  {CYN}{cid:<14}{RST} {name:<20} {tier:<14} {status:<10} {last_brief:<30} {last_synth:<30} {DIM}{runs_str}{RST}")

    print(f"\n  {BOLD}Commands{RST}")
    print(f"  Onboard new client:   {CYN}python scripts\\onboard_client.py{RST}")
    print(f"  Run brief:            {CYN}python scripts\\run_client_brief.py <CLIENT-ID>{RST}")
    print(f"  Run weekly synthesis: {CYN}python scripts\\run_weekly_synthesis.py <CLIENT-ID>{RST}")
    print()
    rule()


if __name__ == "__main__":
    main()
