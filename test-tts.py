#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云 CosyVoice 语音合成功能
"""

import os
import sys
from datetime import datetime

# 设置 API Key
os.environ["DASHSCOPE_API_KEY"] = ""

try:
    from dashscope import SpeechSynthesizer
    import dashscope

    # 打印欢迎信息
    print("=" * 60)
    print("阿里云 CosyVoice 语音合成测试")
    print("=" * 60)

    # 测试文字
    test_text = "你好！这是阿里云通义千问 CosyVoice 语音合成测试。欢迎使用 Fun-ASR 和 Qwen-TTS 语音服务！"

    print(f"\n📝 测试文字：{test_text}")
    print(f"\n🔊 开始合成语音...")

    # 保存音频文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/Users/davidli/lobsterai/project/test-tts-{timestamp}.mp3"

    # 使用流式调用方式
    audio_chunks = []

    def on_data(data):
        """音频数据回调"""
        audio_chunks.append(data)
        print(f"📊 收到音频数据：{len(data)} 字节")

    # 实例化 SpeechSynthesizer
    synthesizer = SpeechSynthesizer(
        model="cosyvoice-v2",
        voice="longxiaochun",
        on_data=on_data
    )

    # 调用合成
    result = synthesizer.call(text=test_text)

    # 合并音频数据
    if audio_chunks:
        audio_data = b''.join(audio_chunks)
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        print(f"\n💾 文件已保存：{output_file}")
        print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")
        print(f"\n🎉 测试完成！")
    else:
        print("\n❌ 未收到音频数据")

except Exception as e:
    print(f"\n❌ 测试出错：{e}")
    import traceback
    traceback.print_exc()
