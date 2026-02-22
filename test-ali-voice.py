#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云语音服务
- 语音合成：qwen3-tts-instruct-flash
- 实时语音合成：qwen3-tts-instruct-flash-realtime
- 实时语音识别：qwen3-asr-flash-realtime-2026-02-10
- 录音语音识别：fun-asr-mtl
"""

import os
import sys
from datetime import datetime

# 设置 API Key
os.environ["DASHSCOPE_API_KEY"] = ""

try:
    from dashscope import SpeechSynthesizer
    import dashscope

    # ==================== 测试语音合成 ====================
    print("=" * 60)
    print("阿里云 Qwen3-TTS 语音合成测试")
    print("=" * 60)

    # 测试文字
    test_text = "你好！这是阿里云通义千问 Qwen3-TTS 语音合成测试。欢迎使用 Fun-ASR 和 Qwen-TTS 语音服务！"

    print(f"\n📝 测试文字：{test_text}")
    print(f"\n🔊 开始合成语音...")

    # 保存音频文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/Users/davidli/lobsterai/project/test-tts-{timestamp}.mp3"

    # 使用正确的模型名称
    result = SpeechSynthesizer.call(
        model="qwen3-tts-instruct-flash",
        voice="longxiaochun",
        text=test_text,
        format='mp3'
    )

    print(f"\n✅ 语音合成成功！")
    print(f"结果类型：{type(result)}")

    # 获取音频数据
    audio_data = result.get_audio_data()

    if audio_data:
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        print(f"💾 文件已保存：{output_file}")
        print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")
        print(f"\n🎉 语音合成测试完成！")
    else:
        print("\n❌ 音频数据为空")

except Exception as e:
    print(f"\n❌ 测试出错：{e}")
    import traceback
    traceback.print_exc()
