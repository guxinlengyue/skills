---
name: handwritten-diary-date-rename
description: Identify handwritten dates in diary photo images and rename files accordingly, including multiple dates in a single image. Use for scanned or photographed handwritten diary pages (.jpg/.jpeg/.png/.heic) where dates appear in the top header or within the body and filenames need to reflect those dates.
---

# Handwritten Diary Date Rename

## Overview

识别手写日记照片中的日期并按日期重命名文件，支持一张图多个日期（按出现顺序用下划线拼接）。

## Workflow

1. 确认处理目录，必要时先复制到工作目录以免影响原图。
2. 运行日期裁剪脚本，生成便于查看的顶部和中部日期条：
   `python scripts/make_date_crops.py --src <folder>`
3. 逐张查看原图或裁剪图，记录日期。统一格式 `YYYY.MM.DD`。一图多日期按从上到下或从前到后顺序。
4. 制作映射表 CSV（列名 `old`,`new`），示例：

```csv
old,new
IMG_0001.jpg,2012.05.11
IMG_0002.jpg,2012.05.14_2012.05.15_2012.05.16
```

5. 执行重命名：
   `powershell -File scripts/rename_from_map.ps1 -Path <folder> -Csv <csv>`
6. 用 `Get-ChildItem` 复核。

## Notes

- 日期常出现在页眉日期栏或正文括号行。
- 字迹不清或日期冲突时，先向用户确认再改名。
- `make_date_crops.py` 需要 Pillow（PIL）。
- `rename_from_map.ps1` 若 `new` 没有扩展名，会保留原文件扩展名；若重名会自动追加 `_01`,`_02`。

## Resources

- `scripts/make_date_crops.py`: 生成顶部和中部日期条裁剪图，便于阅读日期。
- `scripts/rename_from_map.ps1`: 按 CSV 映射批量改名，自动处理扩展名和重名。
