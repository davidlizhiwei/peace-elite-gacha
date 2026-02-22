#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云语音转换工具
- 语音转文字：使用 Fun-ASR (Paraformer/SenseVoice)
- 文字转语音：使用 CosyVoice (Qwen-TTS)

使用前请确保：
1. 已安装 dashscope SDK: pip3 install dashscope
2. 已配置 DASHSCOPE_API_KEY 环境变量
"""

import os
import sys
import json
from datetime import datetime

# 检查并导入 dashscope
try:
    from dashscope.audio.asr import Transcription
    from dashscope import SpeechSynthesizer
    import dashscope
except ImportError:
    print("错误：请先安装 dashscope SDK")
    print("运行：pip3 install dashscope")
    sys.exit(1)

# 配置
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "voice-output")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==================== 语音转文字 (Fun-ASR) ====================

def speech_to_text(audio_file, model="sensevoice-v1"):
    """
    使用 Fun-ASR 将语音文件转换为文字

    参数:
        audio_file: 音频文件路径 (支持 mp3, wav, m4a, flac 等)
        model: 模型选择
               - sensevoice-v1: 高精度，支持多语言 (默认)
               - paraformer-v2: 快速识别
               - paraformer-mt: 多语言混合

    返回:
        识别的文字结果
    """
    if not DASHSCOPE_API_KEY:
        print("错误：未设置 DASHSCOPE_API_KEY 环境变量")
        return None

    if not os.path.exists(audio_file):
        print(f"错误：音频文件不存在：{audio_file}")
        return None

    print(f"\n🎤 开始识别语音文件：{audio_file}")
    print(f"使用模型：{model}")

    try:
        # 创建转录任务
        transcription = Transcription(model=model)

        # 提交文件进行识别
        result = transcription.call(audio_file)

        if result.status_code == 200:
            # 提取识别结果
            text = result.output.text
            print(f"\n✅ 识别成功！")
            print(f"📝 识别结果：\n{text}")

            # 保存结果
            save_transcription_result(text, audio_file)
            return text
        else:
            print(f"❌ 识别失败：{result.message}")
            print(f"错误代码：{result.status_code}")
            return None

    except Exception as e:
        print(f"❌ 识别过程出错：{e}")
        return None


def save_transcription_result(text, audio_file):
    """保存转录结果到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_name = os.path.basename(audio_file).rsplit('.', 1)[0]
    output_file = os.path.join(OUTPUT_DIR, f"{audio_name}_transcript_{timestamp}.txt")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"音频文件：{audio_file}\n")
        f.write(f"识别时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(text)

    print(f"💾 结果已保存：{output_file}")


# ==================== 文字转语音 (CosyVoice/Qwen-TTS) ====================

def text_to_speech(text, voice="longxiaochun", output_file=None, model="cosyvoice-v2"):
    """
    使用 CosyVoice 将文字转换为语音

    参数:
        text: 要转换的文字
        voice: 音色选择
              - longxiaochun: 龙小春 (男声 - 温暖阳光)
              - longwan: 龙婉 (女声 - 温柔知性)
              - longcheng: 龙诚 (男声 - 成熟稳重)
              - longxi: 龙熙 (女声 - 清新活泼)
              - longhua: 龙华 (男声 - 专业播报)
        output_file: 输出文件路径 (默认自动生成)
        model: 模型选择
              - cosyvoice-v2: 高质量 (默认)
              - cosyvoice-v1: 标准版
              - cosyvoice-v3-flash: 快速版

    返回:
        生成的音频文件路径
    """
    if not DASHSCOPE_API_KEY:
        print("错误：未设置 DASHSCOPE_API_KEY 环境变量")
        return None

    if not text:
        print("错误：文字内容为空")
        return None

    print(f"\n🔊 开始合成语音")
    print(f"使用模型：{model}")
    print(f"音色：{voice}")

    # 自动生成输出文件名
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"tts_{voice}_{timestamp}.mp3")

    try:
        # 调用语音合成 API
        result = SpeechSynthesizer.call(
            model=model,
            voice=voice,
            text=text,
            format='mp3',
            sample_rate=22050,
            volume=50,
            rate=1.0,
            pitch=1.0
        )

        if result.status_code == 200:
            # 保存音频文件
            with open(output_file, 'wb') as f:
                f.write(result.output)

            print(f"\n✅ 语音合成成功！")
            print(f"💾 文件已保存：{output_file}")
            print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")

            return output_file
        else:
            print(f"❌ 合成失败：{result.message}")
            print(f"错误代码：{result.status_code}")
            return None

    except Exception as e:
        print(f"❌ 合成过程出错：{e}")
        return None


# ==================== 批量处理 ====================

def batch_speech_to_text(audio_files, model="sensevoice-v1"):
    """批量转换多个音频文件"""
    results = []
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] 处理：{audio_file}")
        result = speech_to_text(audio_file, model)
        results.append({"file": audio_file, "text": result})
    return results


def batch_text_to_speech(texts, voice="longxiaochun", model="cosyvoice-v2"):
    """批量合成多个文本"""
    results = []
    for i, text in enumerate(texts, 1):
        print(f"\n[{i}/{len(texts)}] 合成第 {i} 条")
        result = text_to_speech(text, voice, model=model)
        results.append({"text": text[:50] + "...", "file": result})
    return results


# ==================== 命令行界面 ====================

def print_help():
    """打印帮助信息"""
    help_text = """
╔══════════════════════════════════════════════════════════╗
║           阿里云语音转换工具 - 使用帮助                  ║
╠══════════════════════════════════════════════════════════╣
║  用法：python3 alibaba-voice-converter.py [命令] [选项]  ║
╠══════════════════════════════════════════════════════════╣
║  命令：                                                  ║
║    stt <音频文件>     语音转文字 (Speech-to-Text)        ║
║    tts <文字>         文字转语音 (Text-to-Speech)        ║
║    ttsf <文件>        从文件读取文字转语音               ║
║    list-voices        列出所有可用音色                   ║
║    help               显示此帮助信息                     ║
╠══════════════════════════════════════════════════════════╣
║  选项：                                                  ║
║    --model <模型>     指定模型 (默认：sensevoice-v1/     ║
║                       cosyvoice-v2)                      ║
║    --voice <音色>     指定音色 (TTS 专用)                ║
║    --output <文件>    指定输出文件路径                   ║
╠══════════════════════════════════════════════════════════╣
║  示例：                                                  ║
║    python3 alibaba-voice-converter.py stt recording.mp3  ║
║    python3 alibaba-voice-converter.py tts "你好世界"     ║
║    python3 alibaba-voice-converter.py tts "你好"         ║
║            --voice longwan --output hello.mp3            ║
╚══════════════════════════════════════════════════════════╝
    """
    print(help_text)


def list_voices():
    """列出所有可用音色"""
    voices = {
        "CosyVoice v2 (推荐)": [
            ("longxiaochun", "龙小春", "男声 - 温暖阳光"),
            ("longwan", "龙婉", "女声 - 温柔知性"),
            ("longcheng", "龙诚", "男声 - 成熟稳重"),
            ("longxi", "龙熙", "女声 - 清新活泼"),
            ("longhua", "龙华", "男声 - 专业播报"),
        ],
        "CosyVoice v1": [
            ("aiqi", "艾琪", "女声 - 温柔"),
            ("aiyou", "艾悠", "女声 - 甜美"),
            ("aitong", "艾童", "男声 - 沉稳"),
        ]
    }

    print("\n🎤 可用音色列表：\n")
    for model, voice_list in voices.items():
        print(f"📻 {model}:")
        for voice_id, name, desc in voice_list:
            print(f"   • {voice_id:15} - {name:6} ({desc})")
        print()


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    # 解析参数
    args = sys.argv[2:]
    model = "sensevoice-v1"
    voice = "longxiaochun"
    output = None

    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        elif args[i] == "--voice" and i + 1 < len(args):
            voice = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output = args[i + 1]
            i += 2
        else:
            i += 1

    # 执行命令
    if command == "help":
        print_help()

    elif command == "list-voices":
        list_voices()

    elif command == "stt":
        if len(args) == 0:
            print("错误：请指定音频文件路径")
            print("示例：python3 alibaba-voice-converter.py stt recording.mp3")
            return
        audio_file = args[0]
        # 根据命令自动设置 TTS 模型
        if "--model" not in sys.argv:
            model = "sensevoice-v1"
        speech_to_text(audio_file, model)

    elif command == "tts":
        if len(args) == 0:
            print("错误：请指定要转换的文字")
            print("示例：python3 alibaba-voice-converter.py tts \"你好世界\"")
            return
        text = args[0]
        # 根据命令自动设置 TTS 模型
        if "--model" not in sys.argv:
            model = "cosyvoice-v2"
        text_to_speech(text, voice, output)

    elif command == "ttsf":
        if len(args) == 0:
            print("错误：请指定文本文件路径")
            print("示例：python3 alibaba-voice-converter.py ttsf input.txt")
            return
        text_file = args[0]
        if not os.path.exists(text_file):
            print(f"错误：文件不存在：{text_file}")
            return
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        if "--model" not in sys.argv:
            model = "cosyvoice-v2"
        text_to_speech(text, voice, output)

    else:
        print(f"未知命令：{command}")
        print_help()


if __name__ == "__main__":
    main()
