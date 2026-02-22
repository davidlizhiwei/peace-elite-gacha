#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云 Fun-ASR 实时语音识别
根据官方文档：https://www.alibabacloud.com/help/en/model-studio/real-time-speech-recognition

模型说明：
- fun-asr-realtime: 实时语音识别（稳定版）
- fun-asr-realtime-2025-11-07: 实时语音识别（快照版）
"""

import os
import sys
import glob
import time
from datetime import datetime

# 配置 API Key
os.environ["DASHSCOPE_API_KEY"] = "sk-c3276d00c66c4a759315b5cb0989db16"

from dashscope.audio.asr import Recognition, RecognitionCallback

# ==================== 回调类 ====================
class MyRecognitionCallback(RecognitionCallback):
    def __init__(self):
        self.result_text = []
        self.sentences = []

    def on_open(self):
        print('🔗 连接已打开')

    def on_close(self):
        print('🔌 连接已关闭')

    def on_event(self, result):
        try:
            sentence = result.get_sentence()
            if sentence:
                # 单句识别结果
                if isinstance(sentence, dict):
                    text = sentence.get('text', '')
                    if text and text not in self.result_text:
                        self.result_text.append(text)
                        self.sentences.append(sentence)
                        print(f'📝 识别结果：{text}')
        except Exception as e:
            print(f'❌ 回调错误：{e}')

    def on_complete(self):
        print('✅ 识别完成')

    def on_error(self, result):
        print(f'❌ 错误：{result}')


# ==================== 主函数 ====================
if __name__ == '__main__':
    print("=" * 60)
    print("阿里云 Fun-ASR 实时语音识别测试")
    print("=" * 60)

    # 查找最新的 PCM 文件（TTS 生成的）
    pcm_files = glob.glob("/Users/davidli/lobsterai/project/qwen3-tts-realtime-*.pcm")
    pcm_files = [f for f in pcm_files if os.path.getsize(f) > 0]  # 排除空文件

    if not pcm_files:
        print(f"\n❌ 未找到有效的 PCM 音频文件")
        print("请先运行 TTS 测试生成音频文件")
        sys.exit(1)

    audio_file = max(pcm_files, key=os.path.getmtime)  # 使用最新的文件

    print(f"\n🎧 测试音频：{audio_file}")
    print(f"📊 文件大小：{os.path.getsize(audio_file) / 1024:.1f} KB")
    print(f"\n🔍 使用模型：fun-asr-realtime (Fun-ASR 实时识别)")

    try:
        # 创建回调
        callback = MyRecognitionCallback()

        # 创建识别实例
        # 根据文档：fun-asr-realtime 支持 16kHz 采样率，支持 pcm 格式
        recognition = Recognition(
            model='fun-asr-realtime',
            callback=callback,
            format='pcm',
            sample_rate=24000,  # TTS 生成的是 24kHz，但文档说支持 16kHz，试试 24kHz
            language_hints=['zh', 'en']  # 中文和英文
        )

        print(f"\n🎤 开始识别...")

        # 非流式调用：直接传入文件路径
        result = recognition.call(audio_file)

        print(f"\n📋 完整结果：")
        print(f"状态码：{result.status_code}")

        # 获取识别文本
        sentences = result.get_sentence()
        if sentences:
            if isinstance(sentences, list):
                full_text = ' '.join([s.get('text', '') for s in sentences if isinstance(s, dict) and s.get('text')])
                print(f"\n✅ 识别成功！")
                print(f"📝 识别内容：{full_text}")

                # 打印指标
                print(f"\n📈 指标：")
                print(f"   首包延迟：{recognition.get_first_package_delay()} ms")
                print(f"   尾包延迟：{recognition.get_last_package_delay()} ms")
            else:
                print(f"句子：{sentences}")
        else:
            print(f"未获取到识别结果")
            print(f"回调结果：{callback.result_text}")

    except Exception as e:
        print(f"\n❌ 识别出错：{e}")
        import traceback
        traceback.print_exc()
