---
name: pdf-highlight-comments
description: Highlight text in PDFs and attach comment text directly to the highlight annotations (no sticky notes). Use when you need WPS-compatible highlights with embedded comments for key sentences or evidence quotes.
---

# PDF Highlight Comments

## Overview

Add yellow highlights to specific phrases in a PDF and attach a comment directly to each highlight annotation (no separate sticky-note annotations). This is intended to display cleanly in WPS.

## Quick Start

1. Prepare a JSON list of phrases and comments (UTF-8, with or without BOM).
2. Run the bundled script to apply highlights with embedded comments.
3. Open the output PDF in WPS to verify.

## Workflow

### 1) Create items JSON

Example `items.json`:

```json
[
  {
    "phrase": "The increasing heterogeneity of student populations poses",
    "comment": "Key point: Increasing learner heterogeneity makes teaching more challenging."
  },
  {
    "phrase": "The framework comprises three specialized agents",
    "comment": "Key point: Three agents: learner, teacher, evaluator."
  }
]
```

Notes:
- `phrase` should match text in the PDF. If it does not match exactly, the script falls back to the first N words (default 6).
- Keep comments short and precise for readability in WPS.
- Comments are written as UTF-16BE in the PDF so Chinese text is preserved.
- If your JSON already contains `?` instead of Chinese characters, recreate it (data loss already happened).

#### Generate items JSON safely (no BOM)

Use the helper script to create a clean UTF-8 JSON file:

```bash
python scripts/generate_items_json.py \
  --output "path/to/items.json" \
  --items "[{\"phrase\": \"Figure 1:\", \"comment\": \"?1...\"}]"
```

Or pass a source file (it will read UTF-8 or UTF-8-SIG and re-write clean UTF-8):

```bash
python scripts/generate_items_json.py \
  --output "path/to/items.json" \
  --items "path/to/raw_items.json"
```

### 2) Run the script

```bash
python scripts/annotate_highlight_comments.py \
  --input "path/to/file.pdf" \
  --items "path/to/items.json" \
  --output "path/to/file_annotated.pdf"
```

Optional flags:
- `--keep-existing` to preserve existing annotations (default clears all annotations first).
- `--all-matches` to apply the comment to every match across the document.
- `--fallback-words 6` to change the fallback match length.

### 3) Verify in WPS

Open the output PDF in WPS. The highlights should show and display the comment when you click the highlight.

## Script Notes

- Highlights are yellow.
- Comments are stored in the highlight annotation content, not as separate notes.
- The script prints a `NOT FOUND` list for any phrases that did not match.

## Resources

### scripts/

- `scripts/annotate_highlight_comments.py` applies highlights and attaches comment text to highlight annotations.
- `scripts/generate_items_json.py` creates a UTF-8 items JSON without BOM.
