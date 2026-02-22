#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云语音转换工具
- 语音转文字：使用 Fun-ASR (paraformer-mtl)
- 文字转语音：使用 CosyVoice (cosyvoice-v2)

使用前请确保：
1. 已安装 dashscope SDK: pip3 install dashscope
2. 已配置 DASHSCOPE_API_KEY 环境变量

模型说明：
- 语音合成：qwen3-tts-instruct-flash (指令模式) / cosyvoice-v2 (预设音色)
- 实时语音合成：qwen3-tts-instruct-flash-realtime
- 实时语音识别：qwen3-asr-flash-realtime-2026-02-10
- 录音语音识别：fun-asr-mtl
"""

import os
import sys
from datetime import datetime

# 配置 API Key
os.environ["DASHSCOPE_API_KEY"] = "sk-c3276d00c66c4a759315b5cb0989db16"

from dashscope import SpeechSynthesizer
from dashscope.audio.tts.speech_synthesizer import ResultCallback

# 音频数据缓存
audio_chunks = []

# ==================== 回调函数 ====================
class MyResultCallback(ResultCallback):
    """自定义回调类"""

    def on_open(self):
        print("🔗 WebSocket 连接已打开")

    def on_complete(self):
        print("✅ 语音合成完成")

    def on_error(self, response):
        print(f"❌ 错误：{response}")

    def on_close(self):
        print("🔌 WebSocket 连接已关闭")

    def on_event(self, result):
        """接收音频数据"""
        try:
            audio_frame = result.get_audio_frame()
            if audio_frame:
                audio_chunks.append(audio_frame)
        except Exception:
            # 忽略时间戳处理错误，继续接收音频
            pass

# ==================== 文字转语音 ====================
def text_to_speech(text, model="cosyvoice-v2", voice="longshu_v2", output_file=None):
    """
    文字转语音

    参数:
        text: 要转换的文字
        model: 模型名称
               - cosyvoice-v2: CosyVoice v2 模型
               - cosyvoice-v3-flash: CosyVoice v3 Flash 模型
               - cosyvoice-v3-plus: CosyVoice v3 Plus 模型
        voice: 音色名称
               - longshu_v2: 龙书 (男声 - 新闻播报)
               - loongbella_v2: Bella (女声 - 新闻女声)
               - longcheng: 龙诚 (男声)
               - longxiaochun: 龙小春 (男声)
        output_file: 输出文件路径

    返回:
        生成的音频文件路径
    """
    global audio_chunks
    audio_chunks = []  # 重置缓存

    print(f"\n🔊 开始合成语音...")
    print(f"使用模型：{model}")
    print(f"音色：{voice}")

    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/Users/davidli/lobsterai/project/tts-{timestamp}.mp3"

    try:
        callback = MyResultCallback()

        SpeechSynthesizer.call(
            model=model,
            text=text,
            voice=voice,
            format=SpeechSynthesizer.AudioFormat.format_mp3,
            callback=callback
        )

        if audio_chunks:
            audio_data = b''.join(audio_chunks)
            with open(output_file, 'wb') as f:
                f.write(audio_data)

            print(f"\n✅ 语音合成成功！")
            print(f"💾 文件已保存：{output_file}")
            print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")
            return output_file
        else:
            print("\n❌ 未收到音频数据")
            return None

    except Exception as e:
        print(f"\n❌ 合成出错：{e}")
        return None

# ==================== 语音转文字 ====================
def speech_to_text(audio_file, model="paraformer-mtl"):
    """
    语音转文字

    参数:
        audio_file: 音频文件路径
        model: 模型名称
               - paraformer-mtl: Fun-ASR 多语言模型
               - paraformer-v2: Fun-ASR v2 模型

    返回:
        识别的文字结果
    """
    from dashscope.audio.asr import Transcription

    print(f"\n🎤 开始识别语音文件：{audio_file}")
    print(f"使用模型：{model}")

    try:
        transcription = Transcription(model=model)
        result = transcription.call(audio_file)

        if result.status_code == 200:
            text = result.output.text
            print(f"\n✅ 识别成功！")
            print(f"📝 识别结果：\n{text}")
            return text
        else:
            print(f"❌ 识别失败：{result.message}")
            return None

    except Exception as e:
        print(f"❌ 识别出错：{e}")
        return None

# ==================== 主函数 ====================
def main():
    """主函数 - 测试语音合成"""
    print("=" * 60)
    print("阿里云语音转换工具 - 测试")
    print("=" * 60)

    # 测试文字
    test_text = "你好！这是阿里云通义千问语音合成测试。欢迎使用 Fun-ASR 和 Qwen-TTS 语音服务！"

    print(f"\n📝 测试文字：{test_text}")

    # 测试文字转语音
    result = text_to_speech(
        text=test_text,
        model="cosyvoice-v2",
        voice="longshu_v2"
    )

    if result:
        print(f"\n🎉 测试完成！")
    else:
        print(f"\n❌ 测试失败！")

if __name__ == "__main__":
    main()
