#!/usr/bin/env python3
"""
Generate an items JSON file for highlight comments without BOM/garbling.
"""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generate items JSON for pdf-highlight-comments (UTF-8 without BOM)."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON path (UTF-8 without BOM)",
    )
    parser.add_argument(
        "--items",
        required=True,
        help=(
            "JSON list or file path containing a JSON list of {phrase, comment}. "
            "If it is a file path, it will be read with UTF-8/UTF-8-SIG."
        ),
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    items_arg = args.items.strip()

    if items_arg.startswith("["):
        data = json.loads(items_arg)
    else:
        in_path = Path(items_arg)
        text = in_path.read_text(encoding="utf-8-sig")
        data = json.loads(text)

    if not isinstance(data, list):
        raise SystemExit("items must be a JSON list of {phrase, comment}")

    for i, obj in enumerate(data, start=1):
        if not isinstance(obj, dict):
            raise SystemExit(f"items[{i}] must be an object")
        if not obj.get("phrase") or not obj.get("comment"):
            raise SystemExit(f"items[{i}] requires phrase and comment")

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote items JSON: {output_path}")


if __name__ == "__main__":
    main()
