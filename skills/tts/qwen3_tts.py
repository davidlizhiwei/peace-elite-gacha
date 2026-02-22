#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 Qwen3-TTS 语音合成 Skill
根据官方文档：https://github.com/aliyun/alibabacloud-bailian-speech-demo

模型：qwen3-tts-flash-realtime (实时语音合成)
接口：WebSocket
延迟：~400ms 首音延迟

使用方法:
    from qwen3_tts import text_to_speech

    # 简单调用
    audio_file = text_to_speech("你好，这是测试文字")

    # 指定音色
    audio_file = text_to_speech("你好", voice="Cherry")

    # 指令模式（需要 qwen3-tts-instruct-flash-realtime）
    audio_file = text_to_speech("你好", use_instruct=True, instructions="语速较快")
"""

import os
import base64
import threading
import time
from datetime import datetime
from typing import Optional

import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat

# ==================== 配置 ====================
# API Key 从环境变量获取
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-c3276d00c66c4a759315b5cb0989db16")
dashscope.api_key = DASHSCOPE_API_KEY

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 可用音色 ====================
AVAILABLE_VOICES = {
    "Cherry": "女声 - 温柔甜美",
    "Bella": "女声 - 知性优雅",
    "Ethan": "男声 - 沉稳磁性",
    "longshu_v2": "龙书 - 男声 (新闻播报)",
    "loongbella_v2": "Bella v2 - 女声 (新闻播报)",
}

# ==================== 回调类 ====================
class TTSResultCallback(QwenTtsRealtimeCallback):
    """TTS 结果回调类"""

    def __init__(self, output_file: str):
        self.complete_event = threading.Event()
        self.output_file = output_file
        self.file = open(output_file, 'wb')
        self.received_bytes = 0
        self.first_audio_time = None
        self.start_time = None

    def on_open(self) -> None:
        """连接打开回调"""
        self.start_time = time.time()
        print(f'[TTS] 🔗 连接已打开')

    def on_close(self, close_status_code: int, close_msg: str) -> None:
        """连接关闭回调"""
        self.file.close()
        duration = time.time() - self.start_time if self.start_time else 0
        print(f'[TTS] 🔌 连接已关闭 (耗时：{duration:.2f}s)')

    def on_event(self, response: dict) -> None:
        """事件回调"""
        try:
            event_type = response.get('type')

            if event_type == 'session.created':
                session_id = response.get('session', {}).get('id', 'unknown')
                print(f'[TTS] 📋 会话创建：{session_id}')

            elif event_type == 'response.audio.delta':
                audio_b64 = response.get('delta')
                if audio_b64:
                    audio_data = base64.b64decode(audio_b64)
                    self.file.write(audio_data)
                    self.received_bytes += len(audio_data)

                    if self.first_audio_time is None:
                        self.first_audio_time = time.time()
                        delay = (self.first_audio_time - self.start_time) * 1000
                        print(f'[TTS] 📊 首音延迟：{delay:.1f}ms')

            elif event_type == 'response.done':
                print(f'[TTS] ✅ 响应完成')

            elif event_type == 'session.finished':
                print(f'[TTS] 🏁 会话结束')
                self.complete_event.set()

        except Exception as e:
            print(f'[TTS] ❌ 回调错误：{e}')

    def wait_for_finished(self):
        """等待完成"""
        self.complete_event.wait()

    def get_first_audio_delay(self) -> float:
        """获取首音延迟 (ms)"""
        if self.first_audio_time and self.start_time:
            return (self.first_audio_time - self.start_time) * 1000
        return 0


# ==================== 主函数 ====================
def text_to_speech(
    text: str,
    voice: str = "Cherry",
    use_instruct: bool = False,
    instructions: Optional[str] = None,
    output_file: Optional[str] = None,
    verbose: bool = True
) -> dict:
    """
    文字转语音

    参数:
        text: 要转换的文字
        voice: 音色名称 (Cherry, Bella, Ethan, longshu_v2, loongbella_v2)
        use_instruct: 是否使用指令模式
        instructions: 指令文本（如"语速较快，带有上扬语调"）
        output_file: 输出文件路径（默认自动生成）
        verbose: 是否打印日志

    返回:
        dict: {
            "success": bool,
            "file": str (音频文件路径),
            "size": int (文件大小字节),
            "first_audio_delay": float (首音延迟 ms),
            "session_id": str,
            "error": str (错误信息，如果有)
        }
    """
    if not text:
        return {"success": False, "error": "文字内容为空"}

    # 生成输出文件名
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"tts_{timestamp}.pcm")

    # 选择模型
    model = "qwen3-tts-instruct-flash-realtime" if use_instruct else "qwen3-tts-flash-realtime"

    # WebSocket URL (北京地域)
    ws_url = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"

    if verbose:
        print("=" * 60)
        print("阿里云 Qwen3-TTS 语音合成")
        print("=" * 60)
        print(f"📝 文字：{text[:50]}...")
        print(f"🔊 模型：{model}")
        print(f"🎤 音色：{voice}")
        print(f"💾 输出：{output_file}")

    try:
        # 创建回调
        callback = TTSResultCallback(output_file)

        # 创建实时 TTS 实例
        qwen_tts_realtime = QwenTtsRealtime(
            model=model,
            callback=callback,
            url=ws_url
        )

        # 连接
        qwen_tts_realtime.connect()

        # 配置会话
        session_args = {
            "voice": voice,
            "response_format": AudioFormat.PCM_24000HZ_MONO_16BIT,
            "mode": "server_commit"
        }

        if use_instruct and instructions:
            session_args["instructions"] = instructions
            session_args["optimize_instructions"] = True

        qwen_tts_realtime.update_session(**session_args)

        # 发送文本
        if verbose:
            print(f"📤 发送文本...")

        qwen_tts_realtime.append_text(text)
        time.sleep(0.1)
        qwen_tts_realtime.finish()

        # 等待完成
        if verbose:
            print(f"⏳ 等待完成...")

        callback.wait_for_finished()

        # 获取结果
        file_size = os.path.getsize(output_file)
        first_delay = callback.get_first_audio_delay()
        session_id = qwen_tts_realtime.get_session_id()

        if verbose:
            print(f"\n✅ 合成成功！")
            print(f"💾 文件：{output_file}")
            print(f"📊 大小：{file_size / 1024:.1f} KB")
            print(f"⚡ 首音延迟：{first_delay:.1f} ms")
            print(f"📋 会话 ID: {session_id}")

        return {
            "success": True,
            "file": output_file,
            "size": file_size,
            "first_audio_delay": first_delay,
            "session_id": session_id
        }

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ 合成失败：{error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "file": output_file if os.path.exists(output_file) else None
        }


# ==================== 命令行调用 ====================
if __name__ == "__main__":
    import sys

    # 默认测试文字
    default_text = "你好！这是阿里云通义千问 Qwen3-TTS 语音合成测试。"

    # 从命令行获取文字
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = default_text

    # 执行转换
    result = text_to_speech(text, voice="Cherry")

    if result["success"]:
        print(f"\n🎉 完成！音频文件：{result['file']}")
    else:
        print(f"\n❌ 失败：{result.get('error', '未知错误')}")
        sys.exit(1)
