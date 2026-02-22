# 阿里云语音 Skills

基于阿里云百炼平台的语音处理工具包

## 功能特性

| 功能 | 模型 | 延迟 | 支持格式 |
|------|------|------|---------|
| **TTS** (文字转语音) | qwen3-tts-flash-realtime | ~400ms | PCM (24kHz) |
| **STT** (语音转文字) | fun-asr-realtime | ~400ms | pcm, wav, mp3, opus, aac, amr |

## 安装

无需额外安装，只需配置 API Key：

```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

## 使用方法

### 1. TTS - 文字转语音

```python
from skills import text_to_speech

# 简单调用
result = text_to_speech("你好，这是测试文字")

# 指定音色
result = text_to_speech("你好", voice="Cherry")

# 查看可用音色
from skills import AVAILABLE_VOICES
print(AVAILABLE_VOICES)
# {'Cherry': '女声 - 温柔甜美', 'Bella': '女声 - 知性优雅', ...}
```

**参数说明：**
- `text`: 要转换的文字
- `voice`: 音色 (Cherry, Bella, Ethan, longshu_v2, loongbella_v2)
- `use_instruct`: 是否使用指令模式
- `instructions`: 指令文本（如"语速较快，带有上扬语调"）
- `output_file`: 输出文件路径（默认自动生成）
- `verbose`: 是否打印日志

**返回结果：**
```python
{
    "success": True,
    "file": "/path/to/audio.pcm",
    "size": 215040,  # 文件大小（字节）
    "first_audio_delay": 420.4,  # 首音延迟（ms）
    "session_id": "sess_xxx"
}
```

### 2. STT - 语音转文字

```python
from skills import speech_to_text

# 简单调用
result = speech_to_text("audio.pcm")

# 指定语言
result = speech_to_text("audio.wav", language_hints=["zh", "en"])

# 开启语义断句（适合会议转写）
result = speech_to_text("audio.mp3", semantic_punctuation_enabled=True)
```

**参数说明：**
- `audio_file`: 音频文件路径
- `model`: 模型 (fun-asr-realtime, fun-asr-realtime-2025-11-07)
- `language_hints`: 语言提示 (["zh", "en"])
- `sample_rate`: 采样率 (默认 24000)
- `audio_format`: 音频格式 (pcm, wav, mp3, ...)
- `semantic_punctuation_enabled`: 语义断句

**返回结果：**
```python
{
    "success": True,
    "text": "你好，这是识别结果。",
    "sentences": [...],  # 句子列表（含时间戳）
    "first_package_delay": 391.7,  # 首包延迟（ms）
    "last_package_delay": 1037.1,  # 尾包延迟（ms）
    "request_id": "xxx"
}
```

## 命令行调用

### TTS

```bash
# 使用默认文字
python3 skills/tts/qwen3_tts.py

# 指定文字
python3 skills/tts/qwen3_tts.py "你好，这是测试文字"
```

### STT

```bash
# 自动查找最新 TTS 音频
python3 skills/stt/fun_asr.py

# 指定文件
python3 skills/stt/fun_asr.py audio.pcm
```

## 完整示例

```python
from skills import text_to_speech, speech_to_text

# 1. 文字转语音
tts_result = text_to_speech("你好，这是测试文字", voice="Cherry")

if tts_result["success"]:
    audio_file = tts_result["file"]
    print(f"生成音频：{audio_file}")

    # 2. 语音转文字
    stt_result = speech_to_text(audio_file)

    if stt_result["success"]:
        print(f"识别结果：{stt_result['text']}")
        print(f"首包延迟：{stt_result['first_package_delay']:.1f}ms")
```

## 支持的语言

| 代码 | 语言 |
|------|------|
| zh | 中文 |
| en | 英文 |
| ja | 日语 |
| ko | 韩语 |
| vi | 越南语 |
| id | 印尼语 |
| th | 泰语 |

## 注意事项

1. **音频格式**：
   - TTS 生成 PCM 格式（24kHz 单声道 16bit）
   - STT 支持多种格式，但需正确设置 `sample_rate` 和 `format`

2. **文件大小**：
   - TTS 输出约 5KB/秒（24kHz PCM）
   - STT 输入建议 < 100MB

3. **延迟**：
   - TTS 首音延迟：~400ms
   - STT 首包延迟：~400ms

4. **错误处理**：
   - 检查 `result["success"]`
   - 错误信息在 `result["error"]`

## 文件结构

```
skills/
├── __init__.py          # 包入口
├── README.md            # 本文档
├── tts/
│   ├── __init__.py
│   ├── qwen3_tts.py     # TTS 实现
│   └── output/          # TTS 输出目录
└── stt/
    ├── __init__.py
    ├── fun_asr.py       # STT 实现
    └── output/          # STT 输出目录
```

## 技术栈

- **TTS**: Qwen3-TTS-Flash-Realtime (WebSocket)
- **STT**: Fun-ASR-Realtime (非流式 call)
- **SDK**: DashScope Python SDK

## 相关链接

- [阿里云百炼控制台](https://bailian.console.aliyun.com/)
- [Qwen3-TTS 文档](https://github.com/aliyun/alibabacloud-bailian-speech-demo)
- [Fun-ASR 文档](https://www.alibabacloud.com/help/en/model-studio/real-time-speech-recognition)
