"""Generate a weekly synthesis or monthly review for one client."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import anthropic
import yaml

if os.name == "nt" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENTS_DIR = ROOT_DIR / "data" / "clients"
OUTPUTS_DIR = ROOT_DIR / "data" / "outputs"

MODEL_WEEKLY  = "claude-haiku-4-5-20251001"
MODEL_MONTHLY = "claude-sonnet-4-6"
MAX_TOKENS = 1500

WEEKLY_PROMPT = """\
You are an AI Chief of Staff for {name}.

## Client Context

Name: {name}
Role: {role} at {company}
Industry: {industry}
Operating style: {style}

## Their 90-Day Goals

{goals}

## Currently Active Projects

{projects}

## Known Challenges and Blockers

{challenges}

{standing}

## Briefs from This Week

{briefs}

---

Today is {today} (Friday). Generate a weekly synthesis for {name}.

Every point must be grounded in the context and briefs above. Do not be generic. \
If the weekly briefs are missing, base the synthesis entirely on the context file.

Use this exact format:

# Weekly Synthesis — Week of {week_start}

## Progress This Week

[What has moved forward. Be specific. Reference actual projects.]

## What's Working

[2-3 things that are generating momentum. Be concrete.]

## What's Stalling

[1-2 things that need a decision or change. Be honest, not motivational.]

## Priorities for Next Week

1. [Most important — specific]
2. [Second priority]
3. [Third priority]

## Strategic Recommendation

[One paragraph. The single most important insight for {name} right now, \
based on their goals and current trajectory.]

## Question to Sit With This Weekend

[One honest question that, if answered clearly, would unlock the next level for them.]
"""

MONTHLY_PROMPT = """\
You are an AI Chief of Staff for {name}.

## Client Context

Name: {name}
Role: {role} at {company}
Industry: {industry}
Operating style: {style}

## Their 90-Day Goals

{goals}

## Currently Active Projects

{projects}

## Challenges and Blockers

{challenges}

{standing}

## Recent Briefs and Syntheses

{briefs}

---

Today is {today}. Generate a monthly strategic review for {name}.

Use this exact format:

# Monthly Strategic Review — {month_label}

## Goal Progress

[How far has {name} moved toward each of their 90-day goals? Be honest. \
Rate each goal: On Track / At Risk / Stalled.]

## What to Keep Doing

[2-3 things that are clearly working and should continue.]

## What to Change

[1-2 things that are not working and need a different approach.]

## Opportunity Score

[Based on everything you know about {name}'s context: what is the highest-leverage \
thing they could start, stop, or change in the next 30 days? Give a clear recommendation.]

## Updated 90-Day Priority

[If the 90-day goals need updating based on what you know, suggest the change. \
If they are still correct, confirm them.]

## One Honest Assessment

[One paragraph of direct, honest feedback on {name}'s current trajectory. \
Do not be motivational. Be useful.]
"""


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")


def fmt_list(items: Any) -> str:
    if not items:
        return "None specified."
    if isinstance(items, list):
        return "\n".join(f"- {item}" for item in items if item)
    return str(items)


def fmt_projects(projects: Any) -> str:
    if not projects:
        return "- None specified."
    if not isinstance(projects, list):
        return str(projects)
    lines = []
    for p in projects:
        if isinstance(p, dict):
            line = f"- {p.get('name', 'Unnamed')} ({p.get('status', 'unknown')}): {p.get('goal', '')}"
            lines.append(line)
        else:
            lines.append(f"- {p}")
    return "\n".join(lines)


def collect_recent_briefs(client_id: str, days: int = 7) -> str:
    output_dir = OUTPUTS_DIR / client_id
    if not output_dir.exists():
        return "No briefs available for this period."

    cutoff = date.today() - timedelta(days=days)
    briefs = []
    for brief_file in sorted(output_dir.glob("*_brief.md")):
        try:
            brief_date = date.fromisoformat(brief_file.name[:10])
        except ValueError:
            continue
        if brief_date >= cutoff:
            content = brief_file.read_text(encoding="utf-8", errors="replace").strip()
            briefs.append(f"### {brief_date.strftime('%A %b %d')}\n\n{content[:800]}")

    if not briefs:
        return "No briefs found for this period."
    return "\n\n---\n\n".join(briefs)


def log_run(client_id: str, output_file: Path, run_type: str, usage: Any, model: str) -> None:
    log_path = CLIENTS_DIR / client_id / "run_log.yaml"
    data = load_yaml(log_path)
    runs = data.get("runs", [])
    if not isinstance(runs, list):
        runs = []
    runs.append({
        "date": date.today().isoformat(),
        "type": run_type,
        "output_file": str(output_file.relative_to(ROOT_DIR)),
        "model": model,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    })
    save_yaml(log_path, {"client_id": client_id, "runs": runs})


def run_synthesis(client_id: str, monthly: bool = False) -> int:
    context_path = CLIENTS_DIR / client_id / "context.yaml"
    if not context_path.exists():
        print(f"Client context not found: {context_path}", file=sys.stderr)
        return 1

    context = load_yaml(context_path)
    name = context.get("name", client_id)
    today_str = date.today().strftime("%A, %B %d, %Y")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        return 1

    standing = context.get("standing_instructions", "")
    standing_block = f"## Standing Instructions\n\n{standing}\n" if standing else ""

    common = dict(
        name=name,
        role=context.get("role", "professional"),
        company=context.get("company", "their company"),
        industry=context.get("industry", "their industry"),
        style=context.get("operating_style", "Action-oriented."),
        goals=fmt_list(context.get("goals")),
        projects=fmt_projects(context.get("current_projects")),
        challenges=fmt_list(context.get("challenges")),
        standing=standing_block,
        today=today_str,
    )

    if monthly:
        days_back = 35
        model = MODEL_MONTHLY
        run_type = "monthly_review"
        month_label = date.today().strftime("%B %Y")
        briefs = collect_recent_briefs(client_id, days=days_back)
        prompt = MONTHLY_PROMPT.format(briefs=briefs, month_label=month_label, **common)
        output_suffix = "monthly_review"
        label = "Monthly Review"
    else:
        days_back = 7
        model = MODEL_WEEKLY
        run_type = "weekly_synthesis"
        week_start = (date.today() - timedelta(days=date.today().weekday())).strftime("%B %d, %Y")
        briefs = collect_recent_briefs(client_id, days=days_back)
        prompt = WEEKLY_PROMPT.format(briefs=briefs, week_start=week_start, **common)
        output_suffix = "synthesis"
        label = "Weekly Synthesis"

    print(f"Generating {label} for {name} ({client_id})...")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    output_text = message.content[0].text

    output_dir = OUTPUTS_DIR / client_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{date.today().isoformat()}_{output_suffix}.md"
    output_file.write_text(output_text, encoding="utf-8")

    log_run(client_id, output_file, run_type, message.usage, model)

    print()
    print(output_text)
    print()
    print(f"Saved:  {output_file.relative_to(ROOT_DIR)}")
    print(f"Tokens: {message.usage.input_tokens} in / {message.usage.output_tokens} out  (model: {model})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate weekly synthesis or monthly review for a client.")
    parser.add_argument("client_id", help="Client ID, e.g. CLIENT-001")
    parser.add_argument("--monthly", action="store_true", help="Generate monthly review instead of weekly synthesis")
    args = parser.parse_args()
    return run_synthesis(args.client_id, monthly=args.monthly)


if __name__ == "__main__":
    raise SystemExit(main())
