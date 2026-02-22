"""
阿里云语音 Skills
- TTS: 文字转语音 (Qwen3-TTS)
- STT: 语音转文字 (Fun-ASR)

使用方法:
    from skills import tts, stt

    # 文字转语音
    result = tts.text_to_speech("你好，这是测试文字")

    # 语音转文字
    result = stt.speech_to_text("audio.pcm")
"""

from .tts import text_to_speech, AVAILABLE_VOICES
from .stt import speech_to_text, AVAILABLE_MODELS, SUPPORTED_LANGUAGES

__all__ = [
    "text_to_speech",
    "speech_to_text",
    "AVAILABLE_VOICES",
    "AVAILABLE_MODELS",
    "SUPPORTED_LANGUAGES",
]
