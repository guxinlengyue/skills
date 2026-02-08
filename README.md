# skills

这个仓库用于存放 Codex skills。

## 已包含的 skills

- `handwritten-diary-date-rename`
  - 识别手写日记照片中的日期并按日期重命名文件，支持一张图多个日期。
- `photo-date-rename`
  - 按“拍摄日期”元数据重命名照片，并可通过图像相似度推断缺失日期，命名格式为 `YYYY.MM.DD_HHMMSS`。

## 目录结构

每个 skill 文件夹包含：

- `SKILL.md` 使用说明
- `agents/openai.yaml` UI 元数据
- `scripts/` 和/或 `references/`（按需）
