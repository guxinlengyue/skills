---
name: photo-date-rename
description: Bulk rename photos by Date Taken metadata, copy to a working folder, and infer missing dates by visual similarity matching (OpenCV/ORB). Use for Windows photo folders (.jpg/.jpeg/.png/.heic/etc.) when you need consistent YYYY.MM.DD_HHMMSS names and optional similarity-based backfilling.
---

# Photo Date Rename

## Workflow (Windows)

1. Copy photos into a working folder (e.g. `重命名`) to avoid touching originals.
2. Rename files that already have Date Taken.
3. Build a Date Taken index across original + working folder.
4. Match images without Date Taken using ORB feature similarity.
5. Rename those unmatched images based on their best match.

## Scripts

- `scripts/copy_images.ps1`
  - Copy images from `-Source` to `-Dest`.
- `scripts/clear_readonly.ps1`
  - Clear ReadOnly attributes in a folder (prevents rename errors).
- `scripts/rename_by_date_taken.ps1`
  - Rename files with Date Taken only (no fallback). Generates preview CSV.
- `scripts/build_date_index.ps1`
  - Export `date_taken_index.csv` from source + dest.
- `scripts/match_similarity.py`
  - Create `similarity_date_taken_assignments.csv` using ORB matching.
- `scripts/rename_from_similarity.ps1`
  - Rename files based on similarity assignments and log results.

## Quick Run (example)

1. Copy originals into working folder:
   - `powershell -File scripts\copy_images.ps1 -Source <src> -Dest <dst>`
2. Clear ReadOnly (if needed):
   - `powershell -File scripts\clear_readonly.ps1 -Path <dst>`
3. Rename by Date Taken:
   - `powershell -File scripts\rename_by_date_taken.ps1 -Path <dst>`
4. Build date index from both folders:
   - `powershell -File scripts\build_date_index.ps1 -Source <src> -Dest <dst>`
5. Similarity matching (requires OpenCV):
   - `python scripts\match_similarity.py --csv <dst>\date_taken_index.csv --dst <dst>`
6. Rename by similarity results:
   - `powershell -File scripts\rename_from_similarity.ps1 -Path <dst> -Csv <dst>\similarity_date_taken_assignments.csv`

## Notes

- Date Taken is read via Windows Shell property index 12 ("拍摄日期").
- Similarity scores can be low for noisy matches; review `similarity_date_taken_assignments.csv` before renaming if accuracy is critical.
- Collision-safe naming: adds `_01`, `_02`, etc.
- Default format: `YYYY.MM.DD_HHMMSS`.
