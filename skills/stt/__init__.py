"""
STT Skills - 语音转文字
"""
from .fun_asr import speech_to_text, AVAILABLE_MODELS, SUPPORTED_LANGUAGES, find_latest_tts_audio

__all__ = ["speech_to_text", "AVAILABLE_MODELS", "SUPPORTED_LANGUAGES", "find_latest_tts_audio"]
