#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片生成完成的最终总结到钉钉
"""

import requests
import json
import os

WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

# 图片路径
ORIGINAL_IMAGE = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"
COMPRESSED_IMAGE = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# 之前上传的 media_id
MEDIA_ID = "@lALPM2POKobdusHNAyDNAyA"


def send_markdown_summary():
    """发送 Markdown 格式的总结"""
    original_size = os.path.getsize(ORIGINAL_IMAGE) / 1024 / 1024 if os.path.exists(ORIGINAL_IMAGE) else 0
    compressed_size = os.path.getsize(COMPRESSED_IMAGE) / 1024 / 1024 if os.path.exists(COMPRESSED_IMAGE) else 0

    markdown_text = f"""## 🏃 Nike 跑鞋 - 超写实产品图已生成！

✅ **生成完成**

**图片信息：**
| 项目 | 详情 |
|------|------|
| 原始图片 | {original_size:.2f} MB |
| 压缩图片 | {compressed_size:.2f} MB |
| 分辨率 | 1328×1328 |
| 生成模型 | 通义万相 qwen-image-max |

**产品描述：**
- 品牌：Nike
- 类型：专业跑鞋
- 特点：Flyknit 编织鞋面，气垫鞋底
- 风格：超写实产品摄影，工作室灯光

**文件位置：**
- 原始图片：`{ORIGINAL_IMAGE}`
- 压缩图片：`{COMPRESSED_IMAGE}`

> ⚠️ 说明：由于钉钉 webhook 权限限制，图片无法直接在群聊中显示
> 但图片已上传到钉钉服务器 (Media ID: `{MEDIA_ID}`)
> 可通过本地文件查看完整图片"""

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Nike 跑鞋 - 超写实产品图",
            "text": markdown_text
        }
    }

    print("→ 发送总结消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def main():
    print("📷 发送 Nike 跑鞋图片生成总结到钉钉\n")

    result = send_markdown_summary()

    print()
    print("=" * 50)
    if result.get("errcode") == 0:
        print("✅ 总结消息发送成功！")
        print("\n图片已生成并保存到本地，可通过文件路径查看")
    else:
        print(f"❌ 发送失败：{result}")


if __name__ == "__main__":
    main()
