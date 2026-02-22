#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 Fun-ASR 语音识别 Skill
根据官方文档：https://www.alibabacloud.com/help/en/model-studio/real-time-speech-recognition

模型：fun-asr-realtime (实时语音识别)
接口：非流式 call (适合录音文件)
延迟：~400ms 首包延迟

使用方法:
    from fun_asr import speech_to_text

    # 简单调用
    result = speech_to_text("audio.pcm")

    # 指定语言
    result = speech_to_text("audio.wav", language_hints=["zh", "en"])

    # 开启语义断句
    result = speech_to_text("audio.mp3", semantic_punctuation_enabled=True)
"""

import os
import glob
from datetime import datetime
from typing import List, Optional, Dict, Any

import dashscope
from dashscope.audio.asr import Recognition, RecognitionCallback

# ==================== 配置 ====================
# API Key 从环境变量获取
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-c3276d00c66c4a759315b5cb0989db16")
dashscope.api_key = DASHSCOPE_API_KEY

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 支持的模型 ====================
AVAILABLE_MODELS = {
    "fun-asr-realtime": "实时语音识别 (稳定版，推荐)",
    "fun-asr-realtime-2025-11-07": "实时语音识别 (快照版，远场 VAD 优化)",
    "fun-asr-realtime-2025-09-15": "实时语音识别 (多语言)",
}

# ==================== 支持的语言 ====================
SUPPORTED_LANGUAGES = {
    "zh": "中文",
    "en": "英文",
    "ja": "日语",
    "ko": "韩语",
    "vi": "越南语",
    "id": "印尼语",
    "th": "泰语",
}

# ==================== 回调类 ====================
class ASRResultCallback(RecognitionCallback):
    """ASR 结果回调类"""

    def __init__(self):
        self.sentences = []
        self.full_text = []

    def on_open(self) -> None:
        """连接打开回调"""
        print(f'[ASR] 🔗 连接已打开')

    def on_close(self) -> None:
        """连接关闭回调"""
        print(f'[ASR] 🔌 连接已关闭')

    def on_event(self, result) -> None:
        """事件回调"""
        try:
            sentence = result.get_sentence()
            if sentence:
                if isinstance(sentence, dict):
                    text = sentence.get('text', '')
                    if text:
                        self.full_text.append(text)
                        self.sentences.append(sentence)
                        print(f'[ASR] 📝 {text}')
        except Exception as e:
            print(f'[ASR] ❌ 回调错误：{e}')

    def on_complete(self) -> None:
        """完成回调"""
        print(f'[ASR] ✅ 识别完成')

    def on_error(self, result) -> None:
        """错误回调"""
        print(f'[ASR] ❌ 错误：{result}')


# ==================== 主函数 ====================
def speech_to_text(
    audio_file: str,
    model: str = "fun-asr-realtime",
    language_hints: Optional[List[str]] = None,
    sample_rate: int = 24000,
    audio_format: str = "pcm",
    semantic_punctuation_enabled: bool = False,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    语音转文字

    参数:
        audio_file: 音频文件路径 (支持 pcm, wav, mp3, opus, speex, aac, amr)
        model: 模型名称 (fun-asr-realtime, fun-asr-realtime-2025-11-07)
        language_hints: 语言提示列表 (["zh", "en"])
        sample_rate: 采样率 (Hz)，默认 24000
        audio_format: 音频格式 (pcm, wav, mp3, opus, speex, aac, amr)
        semantic_punctuation_enabled: 是否开启语义断句
        verbose: 是否打印日志

    返回:
        dict: {
            "success": bool,
            "text": str (完整识别文本),
            "sentences": list (句子列表),
            "first_package_delay": float (首包延迟 ms),
            "last_package_delay": float (尾包延迟 ms),
            "request_id": str,
            "error": str (错误信息，如果有)
        }
    """
    if not os.path.exists(audio_file):
        return {"success": False, "error": f"文件不存在：{audio_file}"}

    if verbose:
        print("=" * 60)
        print("阿里云 Fun-ASR 语音识别")
        print("=" * 60)
        print(f"🎧 音频：{audio_file}")
        print(f"📊 大小：{os.path.getsize(audio_file) / 1024:.1f} KB")
        print(f"🔍 模型：{model}")
        print(f"🌐 语言：{language_hints or '自动检测'}")

    try:
        # 创建回调
        callback = ASRResultCallback()

        # 创建识别实例
        recognition = Recognition(
            model=model,
            callback=callback,
            format=audio_format,
            sample_rate=sample_rate,
            language_hints=language_hints or ["zh", "en"],
            semantic_punctuation_enabled=semantic_punctuation_enabled
        )

        if verbose:
            print(f"\n🎤 开始识别...")

        # 非流式调用：直接传入文件路径
        result = recognition.call(audio_file)

        # 获取识别文本
        sentences = result.get_sentence()
        full_text = ""

        if sentences:
            if isinstance(sentences, list):
                full_text = ' '.join([
                    s.get('text', '')
                    for s in sentences
                    if isinstance(s, dict) and s.get('text')
                ])
            elif isinstance(sentences, dict):
                full_text = sentences.get('text', '')

        # 获取指标
        first_delay = recognition.get_first_package_delay()
        last_delay = recognition.get_last_package_delay()
        request_id = recognition.get_last_request_id()

        if verbose:
            if full_text:
                print(f"\n✅ 识别成功！")
                print(f"📝 内容：{full_text}")
                print(f"⚡ 首包延迟：{first_delay:.1f} ms")
                print(f"⚡ 尾包延迟：{last_delay:.1f} ms")
                print(f"📋 Request ID: {request_id}")
            else:
                print(f"\n⚠️ 未获取到识别结果")

        return {
            "success": True,
            "text": full_text,
            "sentences": sentences if sentences else [],
            "first_package_delay": first_delay,
            "last_package_delay": last_delay,
            "request_id": request_id
        }

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ 识别失败：{error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "text": "",
            "sentences": []
        }


# ==================== 辅助函数 ====================
def find_latest_tts_audio() -> Optional[str]:
    """查找最新的 TTS 生成的音频文件"""
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    project_dir = os.path.dirname(parent_dir)

    pcm_files = glob.glob(os.path.join(project_dir, "qwen3-tts-realtime-*.pcm"))
    pcm_files = [f for f in pcm_files if os.path.getsize(f) > 0]

    if pcm_files:
        return max(pcm_files, key=os.path.getmtime)
    return None


# ==================== 命令行调用 ====================
if __name__ == "__main__":
    import sys

    # 从命令行获取文件路径
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        # 自动查找最新的 TTS 音频文件
        audio_file = find_latest_tts_audio()
        if not audio_file:
            print("❌ 未找到音频文件，请提供文件路径")
            print("用法：python fun-asr.py <音频文件>")
            sys.exit(1)
        print(f"自动选择最新音频：{audio_file}")

    # 执行识别
    result = speech_to_text(audio_file)

    if result["success"]:
        print(f"\n🎉 完成！识别内容：{result['text']}")
    else:
        print(f"\n❌ 失败：{result.get('error', '未知错误')}")
        sys.exit(1)
