"""Build a consolidated textX grammar from the modular files in `New Speech/`.

The individual module files follow a light-weight authoring format that allows
us to use `extend <RuleName>:` blocks to collect new alternatives for
placeholder rules defined in the `Core` grammar.  textX itself does not
understand the `module` header or the `extend` directive, so this script takes
care of translating the authoring format into a valid textX grammar.

Running this script will read all module files in dependency order, merge the
rule contributions, and emit a combined grammar to
`New Speech/new_speech.tx`.  The combined grammar can then be consumed by
textX directly.

The script is intentionally dependency-free so that it can be imported from the
test-suite to assert that the grammar compiles.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

MODULE_ORDER: List[str] = [
    "Core.tx",
    "Actions.tx",
    "Communication.tx",
    "Events.tx",
    "Scenarios.tx",
    "StateMachines.tx",
    "Timing.tx",
    "Lifecycle.tx",
    "Causality.tx",
    "Spatial.tx",
    "Quality.tx",
    "Testing.tx",
    "Simulation.tx",
]

# Rules that can be extended via `extend <RuleName>:` blocks.
EXTENDABLE_RULES = {
    "ExtensionElementContribution",
    "ActorItemExtension",
    "MovementStepExtension",
    "MovementDetailExtension",
}


def _normalise_terminal(line: str) -> str:
    """Convert `terminal NAME: /regex/;` to standard textX form.

    Older notes used the `terminal` keyword while the consolidated grammar uses
    plain rule definitions.  This helper keeps comments and unrelated lines
    untouched.
    """

    stripped = line.strip()
    if not stripped.startswith("terminal "):
        return line

    head, _, tail = stripped.partition(":")
    name = head.split()[1]
    if not tail:
        return line

    # Preserve the original indentation from the source line.
    prefix = line[: len(line) - len(line.lstrip(" "))]
    return f"{prefix}{name}:{tail}\n"


def _parse_module(path: Path) -> tuple[str, Dict[str, List[str]]]:
    """Return a sanitised grammar string and extension contributions."""

    content: List[str] = []
    contributions: Dict[str, List[str]] = {}

    lines = path.read_text(encoding="utf8").splitlines()
    i = 0
    while i < len(lines):
        raw_line = lines[i]
        stripped = raw_line.strip()

        # Skip authoring metadata.
        if stripped.startswith("module "):
            i += 1
            continue

        if stripped.startswith("extend "):
            rule = stripped.split()[1]
            rule = rule.rstrip(":")
            block: List[str] = []
            i += 1
            while i < len(lines):
                blk_line = lines[i]
                if ";" in blk_line:
                    before, _, _ = blk_line.partition(";")
                    block.append(before)
                    break
                block.append(blk_line)
                i += 1

            cleaned: List[str] = []
            for entry in block:
                candidate = entry.strip()
                if not candidate or candidate.startswith("//"):
                    continue
                if candidate.startswith("|"):
                    candidate = candidate[1:].strip()
                cleaned.append(candidate.rstrip())

            if cleaned:
                contributions.setdefault(rule, []).extend(cleaned)

            i += 1
            continue

        content.append(_normalise_terminal(raw_line))
        i += 1

    return "\n".join(content) + "\n", contributions


def _format_alternatives(alternatives: Iterable[str]) -> str:
    alts = list(alternatives)
    if not alts:
        return "    ;"

    lines = [f"      {alts[0]}"]
    for alt in alts[1:]:
        lines.append(f"    | {alt}")
    return "\n".join(lines) + "\n;"


def _inject_extensions(grammar: str, contributions: Dict[str, List[str]]) -> str:
    result = grammar
    for rule in EXTENDABLE_RULES:
        alts = contributions.get(rule, [])
        pattern = f"{rule}:"
        start = result.find(pattern)
        if start == -1:
            continue

        if rule == "MovementDetailExtension" and not alts:
            # Remove the rule block entirely and drop the alternative from
            # MovementDetail.
            block_start = start
            block_end = result.find(";", block_start)
            if block_end != -1:
                block_end = result.find("\n", block_end)
                if block_end == -1:
                    block_end = len(result)
                result = result[:block_start] + result[block_end + 1 :]
            # Drop the alternative in MovementDetail, if present.
            alt_line = "    | MovementDetailExtension"
            result = result.replace(alt_line + "\n", "")
            continue

        replacement = _format_alternatives(alts)
        start += len(pattern)
        end = result.find(";", start)
        if end == -1:
            continue
        end_line = result.find("\n", end)
        if end_line == -1:
            end_line = len(result)
        result = result[:start] + "\n" + replacement + result[end_line:]
    return result


def build_new_speech_grammar(root: Path | None = None) -> Path:
    """Create the consolidated grammar and return the output path."""

    root = root or Path(__file__).resolve().parents[1]
    modules_dir = root / "New Speech"
    contributions: Dict[str, List[str]] = {}
    parts: List[str] = []

    for module_name in MODULE_ORDER:
        module_path = modules_dir / module_name
        module_body, module_contrib = _parse_module(module_path)
        parts.append(module_body)
        for key, values in module_contrib.items():
            contributions.setdefault(key, []).extend(values)

    grammar = "\n".join(parts)
    grammar = _inject_extensions(grammar, contributions)

    output_path = modules_dir / "new_speech.tx"
    output_path.write_text(grammar, encoding="utf8")
    return output_path


if __name__ == "__main__":
    path = build_new_speech_grammar()
    print(f"Wrote consolidated grammar to {path}")
