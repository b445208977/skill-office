---
name: "pdf-speaker"
description: "提取PDF文件中的文本内容并使用Edge TTS进行语音朗读。当用户提到'朗读'、'读一下'、'念给我听'、'听这个PDF'、'PDF朗读'等关键词时触发此技能。"
---

# PDF Speaker

这个技能用于提取 PDF 文件中的文本内容，并使用 Edge TTS 进行语音朗读，让用户可以通过"听"的方式阅读 PDF 文档。

## 功能特性

- 自动提取 PDF 文本内容
- 过滤图标、表情符号等干扰内容
- 使用 Edge TTS 高质量语音合成
- 支持逐段朗读，方便跟读
- 自动生成音频文件，支持重复播放

## 依赖要求

- Python 库：`pymupdf` (PDF 文本提取)
- Python 库：`edge-tts` (语音合成)
- Python 库：`pygame` (音频播放，可选)

## 安装依赖

```bash
pip install pymupdf edge-tts pygame
```

## 执行指令

**重要**：根据用户意图选择正确的执行命令：

### 朗读模式（用户要求朗读/听PDF时使用）
```bash
python <script_path> <pdf_path> read
```

### 预览模式（用户只想查看内容时使用）
```bash
python <script_path> <pdf_path> preview
```

### 保存音频模式（用户要求保存音频文件时使用）
```bash
python <script_path> <pdf_path> save
```

## 使用示例

用户说：
- "朗读这个 PDF" → 使用 `read` 参数
- "读一下这个 PDF" → 使用 `read` 参数
- "把这个 PDF 念给我听" → 使用 `read` 参数
- "我想听这个 PDF 的内容" → 使用 `read` 参数
- "查看这个 PDF 的内容" → 使用 `preview` 参数
- "把这个 PDF 保存成音频" → 使用 `save` 参数�
