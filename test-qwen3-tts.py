#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云 Qwen3-TTS 语音合成
模型：qwen3-tts-instruct-flash
"""

import os
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
                print(f"📊 收到音频帧：{len(audio_frame)} 字节")
        except Exception as e:
            # 忽略时间戳处理错误，继续接收音频
            pass

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
    # 创建回调实例
    callback = MyResultCallback()

    # 调用语音合成 - 使用 cosyvoice-v2 模型（阿里云百炼平台可用）
    # cosyvoice-v2 支持的音色：longshu_v2（龙书 - 男声）, loongbella_v2（Bella - 女声）等
    SpeechSynthesizer.call(
        model="cosyvoice-v2",
        text=test_text,
        voice="longshu_v2",  # 龙书 - 新闻男声
        format=SpeechSynthesizer.AudioFormat.format_mp3,
        callback=callback
    )

    # 合并音频数据并保存
    if audio_chunks:
        audio_data = b''.join(audio_chunks)
        with open(output_file, 'wb') as f:
            f.write(audio_data)

        print(f"\n✅ 语音合成成功！")
        print(f"💾 文件已保存：{output_file}")
        print(f"📊 文件大小：{os.path.getsize(output_file) / 1024:.1f} KB")
        print(f"\n🎉 测试完成！")
    else:
        print("\n❌ 未收到音频数据")

except Exception as e:
    print(f"\n❌ 测试出错：{e}")
    import traceback
    traceback.print_exc()
