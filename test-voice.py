#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云语音合成功能
使用 Qwen Image Max 的 API Key
"""

import os
import sys

# 设置 API Key (使用 qwen-image-max 的 key)
# 注意：需要确认这个 key 是否有语音服务的权限
os.environ["DASHSCOPE_API_KEY"] = ""

# 导入语音转换工具
sys.path.insert(0, os.path.dirname(__file__))
from alibaba-voice-converter import text_to_speech, speech_to_text

# 测试文字转语音
print("=" * 60)
print("测试 1: 文字转语音 (CosyVoice)")
print("=" * 60)

test_text = """
你好！这是阿里云通义千问语音合成测试。
今天天气真好，阳光明媚，万里无云。
欢迎使用 Fun-ASR 和 CosyVoice 语音服务！
"""

result = text_to_speech(
    text=test_text,
    voice="longxiaochun",
    model="cosyvoice-v2"
)

if result:
    print(f"\n✅ 测试成功！音频文件：{result}")
else:
    print("\n❌ 测试失败，请检查 API Key 配置")
