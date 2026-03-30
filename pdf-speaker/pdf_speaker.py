#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Speaker - PDF 文本提取与语音朗读工具
使用 pymupdf 提取文本，edge-tts 进行语音合成
"""

import os
import sys
import asyncio
import tempfile
import re
from pathlib import Path

try:
    import fitz
except ImportError:
    print("请安装 pymupdf: pip install pymupdf")
    sys.exit(1)

try:
    import edge_tts
except ImportError:
    print("请安装 edge-tts: pip install edge-tts")
    sys.exit(1)

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class PDFSpeaker:
    """PDF 朗读器类"""

    # 需要过滤的图标和标记字符
    ICON_PATTERNS = [
        r'[\U0001F600-\U0001F64F]',  # 表情符号
        r'[\U0001F300-\U0001F5FF]',  # 杂项符号和象形文字
        r'[\U0001F680-\U0001F6FF]',  # 交通和地图符号
        r'[\U0001F900-\U0001F9FF]',  # 补充符号和象形文字
        r'[\U0001FA00-\U0001FA6F]',  # 国际象棋符号
        r'[\U0001FA70-\U0001FAFF]',  # 符号和象形文字扩展A
        r'[\U00002700-\U000027BF]',  # 装饰符号
        r'[\U00002600-\U000026FF]',  # 杂项符号
        r'[\U0000FE00-\U0000FE0F]',  # 变体选择符
        r'[\U0001F000-\U0001F02F]',  # 麻将牌
        r'[\U0001F0A0-\U0001F0FF]',  # 扑克牌
        r'[\U00002500-\U0000257F]',  # 制表符
        r'[\U00002580-\U0000259F]',  # 方块元素
        r'[\U00002190-\U000021FF]',  # 箭头
        r'[\U000027F0-\U000027FF]',  # 补充箭头A
        r'[\U00002900-\U0000297F]',  # 补充箭头B
        r'[\U00002300-\U000023FF]',  # 杂项技术符号
        r'[\U00002460-\U000024FF]',  # 圈号字母数字
        r'[\U000025A0-\U000025FF]',  # 几何图形
        r'[\U00002B00-\U00002BFF]',  # 杂项符号和箭头
        r'[\U00003000-\U0000303F]',  # CJK符号和标点
        r'[\U00003200-\U000032FF]',  # 圈号CJK字母和月份
        r'[\U0000FF00-\U0000FFEF]',  # 半角和全角形式
        r'[●○■□▲△▼▽◆◇★☆♠♣♥♦]',  # 常见符号
        r'[✓✔✕✖✗✘]',  # 勾叉符号
        r'[→←↑↓↔↕↖↗↘↙]',  # 箭头
        r'[▶◀►◄]',  # 播放控制符号
        r'[①②③④⑤⑥⑦⑧⑨⑩]',  # 圆圈数字
        r'[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽]',  # 括号数字
        r'[⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑]',  # 点数字
    ]
    
    # 需要过滤的标记性文本模式
    MARKER_PATTERNS = [
        r'^[●○■□▲△▼▽◆◇★☆]+$',  # 纯符号行
        r'^\s*[✓✔✕✖✗✘]+\s*$',  # 纯勾叉符号行
        r'^\s*[\d]+\s*$',  # 纯数字行（页码等）
        r'^[→←↑↓↔↕↖↗↘↙▶◀►◄]+$',  # 纯箭头行
    ]

    def __init__(self, pdf_path: str, voice: str = "zh-CN-XiaoxiaoNeural"):
        self.pdf_path = Path(pdf_path)
        self.voice = voice
        self.text_content = []

    def clean_text(self, text: str) -> str:
        """清理文本，移除图标和标记字符"""
        cleaned = text
        for pattern in self.ICON_PATTERNS:
            cleaned = re.sub(pattern, '', cleaned)
        
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned

    def is_marker_line(self, text: str) -> bool:
        """判断是否是标记行（需要过滤）"""
        for pattern in self.MARKER_PATTERNS:
            if re.match(pattern, text):
                return True
        
        cleaned = self.clean_text(text)
        if len(cleaned) <= 2 and not re.search(r'[\u4e00-\u9fff\w]', cleaned):
            return True
        
        return False

    def is_title(self, text: str) -> bool:
        """判断文本是否是标题"""
        patterns = [
            r'^[一二三四五六七八九十]+[、．.]',
            r'^[\d]+[\.．][\d]*[\.．]?\s*\S',
            r'^第[一二三四五六七八九十\d]+[章节篇部]',
        ]
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        return False

    def extract_text(self) -> list:
        """提取 PDF 文本内容，智能合并为完整段落"""
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF 文件不存在: {self.pdf_path}")

        doc = fitz.open(self.pdf_path)
        all_paragraphs = []

        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            
            lines = text.split('\n')
            
            current_para = []
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    if current_para:
                        para_text = ''.join(current_para)
                        para_text = self.clean_text(para_text)
                        if len(para_text) >= 5 and not self.is_marker_line(para_text):
                            all_paragraphs.append({
                                'page': page_num,
                                'text': para_text,
                                'is_title': self.is_title(para_text)
                            })
                        current_para = []
                    continue
                
                if self.is_marker_line(line):
                    continue
                
                current_para.append(line)
                
                if line[-1] in '。！？.!?」』）)】':
                    para_text = ''.join(current_para)
                    para_text = self.clean_text(para_text)
                    if len(para_text) >= 5 and not self.is_marker_line(para_text):
                        all_paragraphs.append({
                            'page': page_num,
                            'text': para_text,
                            'is_title': self.is_title(para_text)
                        })
                    current_para = []
            
            if current_para:
                para_text = ''.join(current_para)
                para_text = self.clean_text(para_text)
                if len(para_text) >= 5 and not self.is_marker_line(para_text):
                    all_paragraphs.append({
                        'page': page_num,
                        'text': para_text,
                        'is_title': self.is_title(para_text)
                    })

        doc.close()
        self.text_content = all_paragraphs
        return self.text_content

    async def generate_audio(self, text: str, output_path: str) -> bool:
        """使用 edge-tts 生成音频文件"""
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            return True
        except Exception as e:
            print(f"生成音频失败: {e}")
            return False

    def play_audio(self, audio_path: str):
        """播放音频文件 (MP3格式)"""
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                return
            except Exception as e:
                print(f"pygame 播放失败: {e}")

        if sys.platform == "win32":
            import subprocess
            subprocess.run(['powershell', '-c', f'-c (New-Object -ComObject WMPlayer.OCX).openPlayer("{audio_path}")'], check=False)
            import time
            time.sleep(3)
        elif sys.platform == "darwin":
            os.system(f'afplay "{audio_path}"')
        else:
            os.system(f'mpg123 "{audio_path}" 2>/dev/null || mpv "{audio_path}" --no-video 2>/dev/null')

    async def speak_text(self, text: str, keep_audio: bool = False):
        """朗读单段文本"""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            print(f"正在生成语音...")
            success = await self.generate_audio(text, tmp_path)
            if success:
                print(f"正在播放...")
                self.play_audio(tmp_path)
        finally:
            if not keep_audio and os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def read_all(self, pause_between: float = 1.0, title_pause: float = 0.5):
        """朗读所有内容"""
        if not self.text_content:
            self.extract_text()

        total = len(self.text_content)
        print(f"\n共 {total} 段内容待朗读\n")
        print("=" * 50)

        for idx, item in enumerate(self.text_content, 1):
            is_title = item.get('is_title', False)
            prefix = "[标题] " if is_title else ""
            print(f"\n[第 {item['page']} 页] 第 {idx}/{total} 段: {prefix}")
            text_preview = item['text'][:80] + "..." if len(item['text']) > 80 else item['text']
            print(text_preview)
            print("-" * 30)

            await self.speak_text(item['text'])

            if idx < total:
                pause = title_pause if is_title else pause_between
                await asyncio.sleep(pause)

        print("\n朗读完成！")

    async def save_all_audio(self, output_dir: str):
        """将所有内容保存为音频文件"""
        if not self.text_content:
            self.extract_text()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        total = len(self.text_content)
        print(f"\n正在生成音频文件，共 {total} 段...")

        for idx, item in enumerate(self.text_content, 1):
            audio_file = output_path / f"paragraph_{idx:04d}.mp3"
            print(f"[{idx}/{total}] 生成: {audio_file.name}")
            await self.generate_audio(item['text'], str(audio_file))

        print(f"\n音频文件已保存到: {output_path}")


def print_content(pdf_path: str):
    """打印 PDF 内容预览"""
    speaker = PDFSpeaker(pdf_path)
    content = speaker.extract_text()

    print(f"\n文件: {pdf_path}")
    print(f"共 {len(content)} 段内容\n")
    print("=" * 60)

    for idx, item in enumerate(content, 1):
        is_title = item.get('is_title', False)
        prefix = "[标题] " if is_title else ""
        print(f"\n[第 {item['page']} 页] 第 {idx} 段: {prefix}")
        print(item['text'])
        print("-" * 40)


async def read_pdf(pdf_path: str, mode: str = "read"):
    """读取 PDF 并朗读"""
    speaker = PDFSpeaker(pdf_path)
    speaker.extract_text()

    if mode == "read":
        await speaker.read_all()
    elif mode == "save":
        output_dir = Path(pdf_path).stem + "_audio"
        await speaker.save_all_audio(output_dir)


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python pdf_speaker.py <pdf_path>          # 预览内容")
        print("  python pdf_speaker.py <pdf_path> read     # 朗读内容")
        print("  python pdf_speaker.py <pdf_path> save     # 保存音频文件")
        sys.exit(1)

    pdf_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "preview"

    if mode == "preview":
        print_content(pdf_path)
    elif mode in ["read", "save"]:
        asyncio.run(read_pdf(pdf_path, mode))
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()
