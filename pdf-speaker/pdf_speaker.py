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

    def __init__(self, pdf_path: str, voice: str = "zh-CN-XiaoxiaoNeural"):
        self.pdf_path = Path(pdf_path)
        self.voice = voice
        self.text_content = []

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
                        if len(para_text) >= 5:
                            all_paragraphs.append({
                                'page': page_num,
                                'text': para_text,
                                'is_title': self.is_title(para_text)
                            })
                        current_para = []
                    continue
                
                current_para.append(line)
                
                if line[-1] in '。！？.!?」』）)】':
                    para_text = ''.join(current_para)
                    if len(para_text) >= 5:
                        all_paragraphs.append({
                            'page': page_num,
                            'text': para_text,
                            'is_title': self.is_title(para_text)
                        })
                    current_para = []
            
            if current_para:
                para_text = ''.join(current_para)
                if len(para_text) >= 5:
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
                prig�(f"正在播放...")
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
