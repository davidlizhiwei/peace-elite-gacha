#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云 Qwen3-TTS 语音合成
使用 OpenAI 兼容接口调用 qwen3-tts-instruct-flash 模型
"""

import os
import requests
from datetime import datetime

# 配置 API Key
API_KEY = "sk-c3276d00c66c4a759315b5cb0989db16"

# 使用 OpenAI 兼容接口 - 新加坡区域
API_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/audio/speech"

# ==================== 测试语音合成 ====================
print("=" * 60)
print("阿里云 Qwen3-TTS 语音合成测试")
print("=" * 60)

# 测试文字
test_text = "你好！这是阿里云通义千问 Qwen3-TTS 语音合成测试。欢迎使用 Fun-ASR 和 Qwen-TTS 语音服务！"

print(f"\n📝 测试文字：{test_text}")
print(f"\n🔊 开始合成语音...")
print(f"使用模型：qwen3-tts-instruct-flash")

# 保存音频文件
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"/Users/davidli/lobsterai/project/qwen3-tts-{timestamp}.mp3"

try:
    # 构建请求头
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 构建请求体 - 使用 OpenAI 兼容格式
    payload = {
        "model": "qwen3-tts-instruct-flash",
        "input": {
            "text": test_text
        },
        "parameters": {
            "format": "mp3",
            "sample_rate": 22050,
            "rate": 1.0,
            "volume": 50,
            "pitch": 1.0
        }
    }

    print(f"\n发送请求到：{API_URL}")

    # 发送 POST 请求
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    print(f"响应状态码：{response.status_code}")

    if response.status_code == 200:
        # 保存音频文件
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"\n✅ 语音合成成功！")
        print(f"💾 文件已保存：{output_file}")
        print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")
        print(f"\n🎉 测试完成！")
    else:
        print(f"\n❌ 合成失败：{response.status_code}")
        print(f"响应内容：{response.text}")

except Exception as e:
    print(f"\n❌ 测试出错：{e}")
    import traceback
    traceback.print_exc()
