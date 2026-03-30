---
name: "ppt-speaker"
description: "提取PPT/PPTX文件中的文本内容并使用Edge TTS进行语音朗读。当用户提到'朗读'、'读一下'、'念给我听'、'听这个PPT'、'PPT朗读'、'演示文稿朗读'等关键词时触发此技能。"
---

# PPT Speaker

这个技能用于提取 PPT/PPTX 文件中的文本内容，并使用 Edge TTS 进行语音朗读，让用户可以通过"听"的方式阅读演示文稿。

## 功能特性

- 自动提取 PPT/PPTX 文本内容
- 按幻灯片顺序朗读
- 使用 Edge TTS 高质量语音合成
- 支持逐段朗读，段落连贯
- 自动过滤图标、图片等非文本内容
- 标题检测与适当停顿

## 依赖要求

- Python 库：`python-pptx` (PPT 文本提取)
- Python 库：`edge-tts` (语音合成)
- Python 库：`pygame` (音频播放，可选)

## 安装依赖

```bash
pip install python-pptx edge-tts pygame
```

## 执行指令

**重要**：根据用户意图选择正确的执行命令：

### 朗读模式（用户要求朗读/听PPT时使用）
```bash
python <script_path> <ppt_path> read
```

### 预览模式（用户只想查看内容时使用）
```bash
python <script_path> <ppt_path> preview
```

### 保存音频模式（用户要求保存音频文件时使用）
```bash
python <script_path> <ppt_path> save
```

## 使用示例

用户说：
- "朗读这个 PPT" → 使用 `read` 参数
- "读一下这个演示文稿" → 使用 `read` 参数
- "把这个 PPT 念给我听" → 使用 `read` 参数
- "我想听这个 PPT 的内容" → 使用 `read` 参数
- "查看这个 PPT 的内容" → 使用 `preview` 参数
- "把这个 PPT 保存成音频" → 使用 `save` 参数
