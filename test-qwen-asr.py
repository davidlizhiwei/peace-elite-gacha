#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云 Fun-ASR 语音识别
根据官方文档：https://github.com/aliyun/alibabacloud-bailian-speech-demo

模型说明：
- fun-asr-mtl: 录音文件识别（多语言）
- qwen3-asr-flash-realtime-2026-02-10: 实时语音识别
"""

import os
import sys
import glob
from datetime import datetime

# 配置 API Key
os.environ["DASHSCOPE_API_KEY"] = "sk-c3276d00c66c4a759315b5cb0989db16"

from dashscope.audio.asr import Recognition, RecognitionCallback

# ==================== 回调类 ====================
class MyRecognitionCallback(RecognitionCallback):
    def __init__(self):
        self.result_text = []

    def on_open(self):
        print('🔗 连接已打开')

    def on_close(self):
        print('🔌 连接已关闭')

    def on_event(self, result):
        try:
            if hasattr(result, 'get_sentence'):
                sentence = result.get_sentence()
                if sentence:
                    if isinstance(sentence, list):
                        for s in sentence:
                            if 'text' in s:
                                text = s['text']
                                self.result_text.append(text)
                                print(f'📝 识别结果：{text}')
                    elif isinstance(sentence, dict) and 'text' in sentence:
                        text = sentence['text']
                        self.result_text.append(text)
                        print(f'📝 识别结果：{text}')
        except Exception as e:
            print(f'❌ 回调错误：{e}')

    def on_error(self, result):
        print(f'❌ 错误：{result}')


# ==================== 主函数 ====================
if __name__ == '__main__':
    print("=" * 60)
    print("阿里云 Fun-ASR 语音识别测试")
    print("=" * 60)

    # 查找最新的 PCM 文件
    pcm_files = glob.glob("/Users/davidli/lobsterai/project/qwen3-tts-realtime-*.pcm")
    pcm_files = [f for f in pcm_files if os.path.getsize(f) > 0]  # 排除空文件

    if not pcm_files:
        print(f"\n❌ 未找到有效的 PCM 音频文件")
        print("请先运行 TTS 测试生成音频文件")
        sys.exit(1)

    audio_file = max(pcm_files, key=os.path.getmtime)  # 使用最新的文件

    print(f"\n🎧 测试音频：{audio_file}")
    print(f"📊 文件大小：{os.path.getsize(audio_file) / 1024:.1f} KB")
    print(f"\n🔍 使用模型：fun-asr-mtl (Fun-ASR 多语言)")

    try:
        # 创建回调
        callback = MyRecognitionCallback()

        # 创建识别实例
        # PCM 格式，24kHz 采样率（与 TTS 生成时一致）
        recognition = Recognition(
            model='fun-asr-mtl',
            callback=callback,
            format='pcm',
            sample_rate=24000
        )

        print(f"\n🎤 开始识别...")

        # 调用识别
        result = recognition.call(audio_file)

        print(f"\n📋 完整结果：")
        print(f"状态码：{result.status_code}")

        # 获取识别文本
        if hasattr(result, 'get_sentence'):
            sentences = result.get_sentence()
            if sentences:
                full_text = ' '.join([s.get('text', '') for s in sentences if isinstance(s, dict)])
                print(f"\n✅ 识别成功！")
                print(f"📝 识别内容：{full_text}")
            else:
                print(f"句子：{sentences}")
        else:
            print(f"结果：{result}")

    except Exception as e:
        print(f"\n❌ 识别出错：{e}")
        import traceback
        traceback.print_exc()
