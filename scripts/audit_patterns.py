#!/usr/bin/env python3
"""Audit plain text or markdown files against common AI writing patterns."""

import argparse
import re
import sys
from pathlib import Path

# Heuristic patterns associated with formulaic or AI-generated prose
PATTERNS = [
    ("Delve / Inquire into", r"\bdelve\b", "Replace with investigate, examine, or explore."),
    ("Tapestry / Mosaic metaphor", r"\b(rich\s+)?tapestry\b", "Replace with simpler concrete descriptions."),
    ("Testament to", r"\b(is\s+a\s+)?testament\s+to\b", "State the result or evidence directly."),
    ("Beacon of", r"\bbeacon\s+of\b", "State the role or accomplishment directly."),
    ("Crucial / Paramount / Pivotal", r"\b(crucial|paramount|pivotal)\b", "Use essential, key, or explain why it matters."),
    ("Unnecessary Signposting", r"\b(it\s+is\s+worth\s+noting|it\s+is\s+important\s+to\s+remember)\b", "Cut the meta-signpost and state the fact."),
    ("Formulaic Closers", r"\b(in\s+conclusion|to\s+summarize|all\s+in\s+all|in\s+summary)\b", "End on the final substantive point instead."),
    ("Em Dash Overuse", r"—", "Review em dash usage; replace with periods or commas where appropriate."),
    ("Not only... but also structure", r"\bnot\s+only\b[\s\S]{1,60}\bbut\s+also\b", "Use active direct sentences instead of paired contrast."),
    ("Superficial Hedging", r"\b(can\s+be\s+seen\s+as|might\s+be\s+considered)\b", "Be decisive or attribute the claim."),
]

def audit_file(file_path: Path) -> int:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return 1

    lines = content.splitlines()
    matches_found = 0

    print(f"\n--- Auditing: {file_path} ({len(lines)} lines) ---")
    for idx, line in enumerate(lines, 1):
        for name, pattern, fix in PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                matches_found += 1
                matched_text = match.group(0)
                print(f"  Line {idx}: [{name}] Found '{matched_text}'")
                print(f"    Suggestion: {fix}")

    if matches_found == 0:
        print("  ✓ No high-frequency AI writing flags detected!")
    else:
        print(f"\nTotal potential AI writing patterns detected: {matches_found}")

    return 0

def main():
    parser = argparse.ArgumentParser(description="Audit text files for AI writing patterns.")
    parser.add_argument("files", nargs="+", type=Path, help="Files to audit")
    args = parser.parse_args()

    exit_code = 0
    for file_path in args.files:
        if not file_path.exists():
            print(f"File not found: {file_path}", file=sys.stderr)
            exit_code = 1
            continue
        audit_file(file_path)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
