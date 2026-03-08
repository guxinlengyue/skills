---
name: cn-output-integrity
description: Verify Chinese output integrity in generated files (docx/pdf/json/txt) and prevent Chinese text from turning into '?'. Use whenever producing Chinese content or filenames on Windows to check encoding and fix before delivery.
---

# CN Output Integrity

## Overview

Ensure Chinese text in generated outputs is preserved correctly (no '?' corruption). Applies to DOCX, PDF annotations, JSON, and TXT outputs.

## Workflow

### 1) Detect corruption before delivery

- If you create a file with Chinese content, immediately re-open and extract text to verify.
- If extracted text contains many '?' and no CJK characters, treat as corruption.

### 2) Fix common causes

- **PowerShell BOM issues**: JSON created via `Set-Content -Encoding UTF8` may include BOM. Re-write via Python with UTF-8 (no BOM).
- **Console encoding**: Avoid passing large Chinese strings via command-line; use Python file writes instead.
- **PDF annotations**: Always write `/Contents` as UTF-16BE hex with BOM.
- **DOCX**: If Chinese appears as '?', rebuild content using Unicode escape strings and re-save.

### 3) Validate the fix

- Re-open the output file and re-extract text to confirm CJK characters are present.
- Only deliver files after validation passes.

## Checks by file type

### DOCX

- Use `python-docx` to re-open and dump text to a UTF-8 `.txt` file for verification.
- If corruption exists, rebuild content using unicode-escaped strings (e.g., `\u4e2d\u6587`).

### PDF annotations

- After writing highlights, read the annotation `/Contents` with `doc.xref_object()` to ensure it is not `?`-filled.
- If corrupted, rewrite `/Contents` using UTF-16BE hex with BOM.

### JSON/TXT

- Always write with Python using `encoding='utf-8'` (no BOM).
- If input is from PowerShell, re-read with `utf-8-sig` then write clean UTF-8.

## Resources

### scripts/

- Optional: add helper scripts for docx/pdf/json validation if needed.
