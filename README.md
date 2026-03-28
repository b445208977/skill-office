# Skill Office

Office 办公辅助技能集合，为 AI 助手提供处理 Office 文档的能力。

## 项目简介

Skill Office 是一套针对 Office 办公场景的 AI 技能工具集，通过模块化的技能设计，让 AI 助手能够更好地处理各类办公文档。每个技能都是独立的功能模块，可以单独使用或组合使用。

## 当前技能

### 📄 PDF Speaker

PDF 文本提取与语音朗读工具。

**功能特性：**
- 自动提取 PDF 文本内容
- 使用 Edge TTS 高质量语音合成
- 支持逐段朗读，方便跟读
- 自动生成音频文件，支持重复播放
- 智能识别标题和段落

**使用场景：**
- 听书学习：将 PDF 文档转为语音，解放双眼
- 内容审核：通过听读方式检查文档内容
- 辅助阅读：帮助视障人士或有阅读困难的用户

**依赖要求：**
```bash
pip install pymupdf edge-tts pygame
```

## 未来规划

Skill Office 将持续扩展，为更多 Office 工具提供 AI 辅助能力：

### 📊 Excel Assistant (规划中)
- 智能数据分析和可视化
- 自动生成图表和报告
- 数据清洗和格式转换
- 公式智能推荐

### 📝 Word Assistant (规划中)
- 文档格式智能调整
- 内容摘要生成
- 多语言翻译
- 模板智能匹配

### 📽️ PowerPoint Assistant (规划中)
- 幻灯片内容生成
- 设计风格推荐
- 演讲稿自动生成
- 图片智能排版

### 📧 Outlook Assistant (规划中)
- 邮件智能分类
- 自动回复生成
- 日程智能管理
- 会议纪要生成

## 项目结构

```
skill-office/
├── pdf-speaker/           # PDF 朗读技能
│   ├── SKILL.md          # 技能描述文件
│   ├── pdf_speaker.py    # 核心脚本
│   └── LICENSE           # MIT 许可证
├── .gitignore            # Git 过滤配置
└── README.md             # 项目说明文档
```

## 如何使用

每个技能目录下都有 `SKILL.md` 文件，详细说明了技能的功能和使用方法。AI 助手会根据用户需求自动调用相应技能。

## 贡献指南

欢迎贡献新技能或改进现有技能！

1. Fork 本仓库
2. 创建新的技能分支 (`git checkout -b feature/new-skill`)
3. 提交更改 (`git commit -am 'Add new skill'`)
4. 推送到分支 (`git push origin feature/new-skill`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。每个技能模块独立授权，详见各技能目录下的 LICENSE 文件。

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。
