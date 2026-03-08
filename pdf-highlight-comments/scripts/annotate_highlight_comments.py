#!/usr/bin/env python3
"""
Annotate a PDF by highlighting phrases and attaching comments directly
to the highlight annotations (no sticky-note comments).
"""

import argparse
import json
from pathlib import Path

import fitz  # PyMuPDF


def _read_text(path: Path) -> str:
    # PowerShell's UTF-8 output often includes BOM; handle both.
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8")


def _looks_corrupted(text: str) -> bool:
    # Heuristic: many '?' with no CJK characters usually indicates prior corruption.
    if "?" not in text:
        return False
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            return False
    return True


def load_items(path: Path):
    raw = _read_text(path)
    if _looks_corrupted(raw):
        print("WARNING: items JSON appears to contain '?' in place of non-ASCII characters.")
        print("         Recreate the items file using UTF-8 (no conversion) to avoid data loss.")
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("items JSON must be a list of {phrase, comment} objects")
    items = []
    for i, obj in enumerate(data, start=1):
        if not isinstance(obj, dict):
            raise ValueError(f"items[{i}] must be an object")
        phrase = obj.get("phrase", "").strip()
        comment = obj.get("comment", "").strip()
        if not phrase or not comment:
            raise ValueError(f"items[{i}] requires non-empty phrase and comment")
        items.append({"phrase": phrase, "comment": comment})
    return items


def remove_all_annots(doc: fitz.Document):
    for page in doc:
        annot = page.first_annot
        while annot:
            nxt = annot.next
            page.delete_annot(annot)
            annot = nxt


def set_contents_utf16(doc: fitz.Document, annot: fitz.Annot, text: str):
    # PDF Unicode string: UTF-16BE with BOM, stored as hex string
    utf16 = text.encode("utf-16-be")
    hexstr = "FEFF" + utf16.hex().upper()
    doc.xref_set_key(annot.xref, "Contents", f"<{hexstr}>")


def add_highlight_with_comment(page: fitz.Page, rects, comment: str):
    annot = page.add_highlight_annot(rects)
    annot.set_colors(stroke=(1, 1, 0))  # yellow
    annot.update()
    set_contents_utf16(page.parent, annot, comment)


def try_search(page: fitz.Page, phrase: str):
    return page.search_for(phrase)


def main():
    parser = argparse.ArgumentParser(
        description="Highlight phrases in a PDF and attach comments to the highlights."
    )
    parser.add_argument("--input", required=True, help="Input PDF path")
    parser.add_argument("--items", required=True, help="JSON file with phrases and comments")
    parser.add_argument("--output", help="Output PDF path")
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Keep existing annotations (default clears all annotations first)",
    )
    parser.add_argument(
        "--all-matches",
        action="store_true",
        help="Apply the comment to all matches across the document",
    )
    parser.add_argument(
        "--fallback-words",
        type=int,
        default=6,
        help="Fallback to first N words if full phrase is not found",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    items_path = Path(args.items)
    output_path = Path(args.output) if args.output else input_path.with_stem(input_path.stem + "_annotated")

    items = load_items(items_path)

    doc = fitz.open(input_path)
    if not args.keep_existing:
        remove_all_annots(doc)

    not_found = []
    for item in items:
        phrase = item["phrase"]
        comment = item["comment"]
        found = False

        for page in doc:
            rects = try_search(page, phrase)
            if rects:
                add_highlight_with_comment(page, rects, comment)
                found = True
                if not args.all_matches:
                    break
        if found:
            continue

        # fallback: first N words
        words = phrase.split()
        if args.fallback_words > 0 and len(words) > args.fallback_words:
            short_phrase = " ".join(words[: args.fallback_words])
        else:
            short_phrase = phrase

        for page in doc:
            rects = try_search(page, short_phrase)
            if rects:
                add_highlight_with_comment(page, rects, comment)
                found = True
                if not args.all_matches:
                    break

        if not found:
            not_found.append(phrase)

    if not_found:
        print("NOT FOUND:")
        for p in not_found:
            print(f"- {p}")

    doc.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
