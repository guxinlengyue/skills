---
name: pdf-figure-annotate
description: Explain each figure in a PDF (by viewing the figure pages) and then add those explanations as highlight comments on the figure captions without removing existing annotations. Use when the user wants figure-by-figure explanations added into a PDF as highlight comments, especially for WPS viewing.
---

# PDF Figure Annotate

## Overview

Explain every figure in a PDF and then add the explanations as highlight comments on the figure captions, preserving existing annotations. This workflow is designed to work well in WPS with highlight comments (no sticky notes).

## Workflow

### 1) Locate and review figures

- Render the figure pages to images and visually inspect each figure.
- Identify the caption text (e.g., "Figure 1:", "Figure 2:").

Recommended tools:
- Use the PDF skill workflow to render pages if layout matters.
- Use `fitz`/PyMuPDF rendering when quick capture is enough.

### 2) Write explanations

- For each figure, write a concise explanation in Chinese.
- Keep each explanation short so it fits well in WPS comment popups.

### 3) Prepare items JSON

Create a JSON list for the annotation script. Use the caption prefix as the `phrase` so the highlight can match the figure caption.

Example `items_figs_zh.json`:

```json
[
  {
    "phrase": "Figure 1:",
    "comment": "?1??????????????????????????????????/???/????/????????????????????"
  },
  {
    "phrase": "Figure 2:",
    "comment": "?2?????????????????????????????????????????????????????????????????????"
  }
]
```

Notes:
- Save the JSON as UTF-8 without BOM.
- Use short phrases (e.g., `Figure 1:`) to improve matching reliability.

### 4) Annotate without removing existing comments

Use the `pdf-highlight-comments` skill script with `--keep-existing` so prior annotations remain:

```bash
python C:\Users\guxin\.codex\skills\public\pdf-highlight-comments\scripts\annotate_highlight_comments.py \
  --keep-existing \
  --input "path\\to\\file.pdf" \
  --items "path\\to\\items_figs_zh.json" \
  --output "path\\to\\file_plus_figs.pdf"
```

## Resources

### scripts/

- Optional helper: create scripts to extract figure captions or generate an items template if needed.
