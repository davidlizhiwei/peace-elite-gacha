#!/usr/bin/env python3
import dashscope
from dashscope import ImageSynthesis

# Set API key
dashscope.api_key = "sk-c3276d00c66c4a759315b5cb0989db16"

# Test image generation
print("Testing DashScope ImageSynthesis...")
print(f"Available models: {dir(ImageSynthesis.Models)}")

# Try with wanx-v1 (size format: "1024*1024" not "1024x1024")
result = ImageSynthesis.call(
    model=ImageSynthesis.Models.wanx_v1,
    prompt="一只可爱的卡通小猫，阳光明媚",
    n=1,
    size="1024*1024"
)

print(f"Result: {result}")
print(f"Status code: {result.status_code}")
print(f"Request ID: {result.request_id}")

if result.output:
    print(f"Output: {result.output}")
    if hasattr(result.output, 'results') and result.output.results:
        print(f"Results: {result.output.results}")
        for i, res in enumerate(result.output.results):
            if hasattr(res, 'url') and res.url:
                print(f"Image {i} URL: {res.url}")
