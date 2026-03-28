---
name: "ppt-speaker"
description: "Extracts text from PPT/PPTX files and reads aloud using Edge TTS. Invoke when user wants to listen to PowerPoint content or needs PPT narration."
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

## 使用方法

当用户提供 PPT 文件路径时，AI 会：

1. 提取 PPT 文本内容
2. 清理和格式化文本，合并段落
3. 使用 Edge TTS 生成语音
4. 播放音频或保存音频文件

## 依赖要求

- Python 库：`python-pptx` (PPT 文本提取)
- Python 库：`edge-tts` (语音合成)
- Python 库：`pygame` (音频播放，可选)

## 安装依赖

```bash
pip install python-pptx edge-tts pygame
```

## 执行脚本

脚本位置：`.trae/skills/ppt-speaker/ppt_speaker.py`

## 使用示例

用户说：
- "帮我读一下这个 PPT"
- "把这个演示文稿念给我听"
- "我想听这个 PPT 的内容"

AI 会自动调用此技能完成朗读任务。
