"""Generate a daily AI Chief of Staff brief for one client."""

from __future__ import annotations

import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import anthropic
import yaml

if os.name == "nt" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
CLIENTS_DIR = ROOT_DIR / "data" / "clients"
OUTPUTS_DIR = ROOT_DIR / "data" / "outputs"

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024

BRIEF_PROMPT = """\
You are an AI Chief of Staff for {name}.

## Client Context

Name: {name}
Role: {role} at {company}
Industry: {industry}
Operating style: {style}
Background: {background}

## Their 90-Day Goals

{goals}

## Currently Active Projects

{projects}

## Known Challenges and Blockers

{challenges}

{standing}

---

Today is {today}.

Generate a focused, specific daily brief for {name}. Every sentence must be grounded in \
the context above. Do not be generic. Do not invent facts. If context is thin on a point, \
skip that point rather than filling it with generic advice.

Use this exact format:

# Good Morning, {name} — {today}

## Top 3 Priorities for Today

1. [Most important action — specific, not generic. Reference their actual projects or goals.]
2. [Second priority — equally specific.]
3. [Third priority.]

## Strategic Note

[One paragraph. What matters most this week and why, given their actual situation.]

## One Decision to Make Today

[Frame a specific decision they are actually facing, with two clear options and a lean \
toward one. Do not frame a hypothetical — use their real context.]

## Operating Reminder

[One sentence. Tied directly to their stated goals and operating style.]
"""

PROJECTS_TEMPLATE = "- {name} ({status}): {goal}"


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
            lines.append(PROJECTS_TEMPLATE.format(
                name=p.get("name", "Unnamed"),
                status=p.get("status", "unknown"),
                goal=p.get("goal", ""),
            ))
            if p.get("notes"):
                lines.append(f"  Note: {p['notes']}")
        else:
            lines.append(f"- {p}")
    return "\n".join(lines)


def build_prompt(context: dict[str, Any]) -> str:
    standing = context.get("standing_instructions", "")
    standing_block = f"## Standing Instructions\n\n{standing}\n" if standing else ""
    return BRIEF_PROMPT.format(
        name=context.get("name", "the client"),
        role=context.get("role", "professional"),
        company=context.get("company", "their company"),
        industry=context.get("industry", "their industry"),
        style=context.get("operating_style", "Action-oriented."),
        background=context.get("background", "Not specified."),
        goals=fmt_list(context.get("goals")),
        projects=fmt_projects(context.get("current_projects")),
        challenges=fmt_list(context.get("challenges")),
        standing=standing_block,
        today=date.today().strftime("%A, %B %d, %Y"),
    )


def log_run(client_id: str, output_file: Path, usage: Any) -> None:
    log_path = CLIENTS_DIR / client_id / "run_log.yaml"
    data = load_yaml(log_path)
    runs = data.get("runs", [])
    if not isinstance(runs, list):
        runs = []
    runs.append({
        "date": date.today().isoformat(),
        "type": "daily_brief",
        "output_file": str(output_file.relative_to(ROOT_DIR)),
        "model": MODEL,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    })
    save_yaml(log_path, {"client_id": client_id, "runs": runs})


def run_brief(client_id: str) -> int:
    context_path = CLIENTS_DIR / client_id / "context.yaml"
    if not context_path.exists():
        print(f"Client context not found: {context_path}", file=sys.stderr)
        print(f"Run python scripts\\onboard_client.py to create it.", file=sys.stderr)
        return 1

    context = load_yaml(context_path)
    name = context.get("name", client_id)
    today = date.today().isoformat()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        return 1

    prompt = build_prompt(context)

    print(f"Generating brief for {name} ({client_id})...")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    brief = message.content[0].text

    # Save output
    output_dir = OUTPUTS_DIR / client_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{today}_brief.md"
    output_file.write_text(brief, encoding="utf-8")

    # Log the run
    log_run(client_id, output_file, message.usage)

    print()
    print(brief)
    print()
    print(f"Saved:  {output_file.relative_to(ROOT_DIR)}")
    print(f"Tokens: {message.usage.input_tokens} in / {message.usage.output_tokens} out")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts\\run_client_brief.py <CLIENT-ID>", file=sys.stderr)
        print("Example: python scripts\\run_client_brief.py CLIENT-001", file=sys.stderr)
        return 1
    return run_brief(sys.argv[1])


if __name__ == "__main__":
    raise SystemExit(main())
