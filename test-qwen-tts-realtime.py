#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云 Qwen3-TTS 实时语音合成
根据官方示例代码：https://github.com/aliyun/alibabacloud-bailian-speech-demo

模型说明：
- qwen3-tts-flash-realtime: 实时语音合成（标准版）
- qwen3-tts-instruct-flash-realtime: 实时语音合成（指令控制版）
"""

import os
import base64
import threading
import time
import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat

# ==================== 配置 API Key ====================
os.environ["DASHSCOPE_API_KEY"] = "sk-c3276d00c66c4a759315b5cb0989db16"
dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]

# ==================== 回调类 ====================
class MyCallback(QwenTtsRealtimeCallback):
    def __init__(self, output_file):
        self.complete_event = threading.Event()
        self.output_file = output_file
        self.file = open(output_file, 'wb')
        self.received_bytes = 0

    def on_open(self) -> None:
        print('🔗 连接已打开')

    def on_close(self, close_status_code, close_msg) -> None:
        self.file.close()
        print(f'🔌 连接已关闭：code={close_status_code}, msg={close_msg}')

    def on_event(self, response: str) -> None:
        try:
            type = response.get('type')

            if type == 'session.created':
                print(f'📋 会话创建：{response.get("session", {}).get("id", "unknown")}')

            elif type == 'response.audio.delta':
                recv_audio_b64 = response.get('delta')
                if recv_audio_b64:
                    audio_data = base64.b64decode(recv_audio_b64)
                    self.file.write(audio_data)
                    self.received_bytes += len(audio_data)
                    print(f'📊 收到音频数据：{len(audio_data)} 字节 (累计：{self.received_bytes})')

            elif type == 'response.done':
                print('✅ 响应完成')

            elif type == 'session.finished':
                print('🏁 会话结束')
                self.complete_event.set()

        except Exception as e:
            print(f'❌ 回调错误：{e}')

    def wait_for_finished(self):
        self.complete_event.wait()


# ==================== 主函数 ====================
if __name__ == '__main__':
    print("=" * 60)
    print("阿里云 Qwen3-TTS 实时语音合成测试")
    print("=" * 60)

    # 测试文字
    test_text = "你好！这是阿里云通义千问 Qwen3-TTS 实时语音合成测试。欢迎使用 Fun-ASR 和 Qwen-TTS 语音服务！"

    print(f"\n📝 测试文字：{test_text}")

    # 输出文件
    output_file = f"/Users/davidli/lobsterai/project/qwen3-tts-realtime-{time.strftime('%Y%m%d_%H%M%S')}.pcm"

    # 创建回调
    callback = MyCallback(output_file)

    # 创建实时 TTS 实例
    # 如需使用指令控制功能，将 model 替换为 qwen3-tts-instruct-flash-realtime
    qwen_tts_realtime = QwenTtsRealtime(
        model='qwen3-tts-flash-realtime',
        callback=callback,
        # 北京地域 URL（API Key 是北京区域的）
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
    )

    print(f"\n🔊 开始连接...")
    qwen_tts_realtime.connect()

    print(f"⚙️  配置会话...")
    qwen_tts_realtime.update_session(
        voice='Cherry',  # 音色：Cherry, Bella, Ethan 等
        response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        mode='server_commit'
    )

    print(f"📤 发送文本...")
    qwen_tts_realtime.append_text(test_text)
    time.sleep(0.1)

    print(f"⏹️  结束输入...")
    qwen_tts_realtime.finish()

    print(f"⏳ 等待完成...")
    callback.wait_for_finished()

    print(f"\n✅ 测试完成！")
    print(f"💾 文件已保存：{output_file}")
    print(f"📊 文件大小：{callback.received_bytes / 1024:.1f} KB")

    # 打印指标
    session_id = qwen_tts_realtime.get_session_id()
    first_audio_delay = qwen_tts_realtime.get_first_audio_delay()
    print(f"\n📈 指标：")
    print(f"   会话 ID: {session_id}")
    print(f"   首音延迟：{first_audio_delay} ms")
