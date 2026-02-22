#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼语音服务测试
使用 OpenAI 兼容接口调用

模型说明：
- 语音合成：qwen3-tts-instruct-flash
- 实时语音合成：qwen3-tts-instruct-flash-realtime
- 实时语音识别：qwen3-asr-flash-realtime-2026-02-10
- 录音语音识别：fun-asr-mtl
"""

import os
import requests
import base64
from datetime import datetime

# 配置 API Key
API_KEY = "sk-c3276d00c66c4a759315b5cb0989db16"

# 正确的 API 端点
API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

print("=" * 60)
print("阿里云百炼语音服务测试")
print("=" * 60)

# ==================== 测试语音合成 ====================
print("\n" + "=" * 60)
print("1. 测试语音合成 (qwen3-tts-instruct-flash)")
print("=" * 60)

test_text = "你好！这是阿里云通义千问 Qwen3-TTS 语音合成测试。"

print(f"\n📝 测试文字：{test_text}")
print(f"🔊 使用模型：qwen3-tts-instruct-flash")

# 保存音频文件
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"/Users/davidli/lobsterai/project/qwen3-tts-{timestamp}.mp3"

try:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 使用正确的格式：包含 input 和 messages
    payload = {
        "model": "qwen3-tts-instruct-flash",
        "input": {
            "text": test_text
        },
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": test_text
                    }
                ]
            }
        ],
        "parameters": {
            "format": "mp3"
        }
    }

    url = f"{API_BASE}/audio/speech"
    print(f"\n发送请求到：{url}")
    print(f"请求内容：{payload}")

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    print(f"\n响应状态码：{response.status_code}")
    print(f"响应内容：{response.text[:500] if response.text else 'empty'}")

    if response.status_code == 200:
        result = response.json()
        # 检查是否有音频数据
        if "output" in result and "audio" in result["output"]:
            audio_base64 = result["output"]["audio"]
            audio_data = base64.b64decode(audio_base64)
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            print(f"\n✅ 语音合成成功！")
            print(f"💾 文件已保存：{output_file}")
            print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")
        else:
            print(f"\n响应格式：{result}")
    else:
        print(f"\n❌ 合成失败")

except Exception as e:
    print(f"\n❌ 测试出错：{e}")
    import traceback
    traceback.print_exc()
