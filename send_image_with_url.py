#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片到钉钉
使用 imgbb 免费图床上传图片，然后发送带图片链接的消息
"""

import os
import requests
import json
import base64

WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"
IMAGE_PATH = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

# ImgBB API Key (免费图床)
IMG_BB_API_KEY = "e0c7a2c5f5e8d9b3c1a4f6e8d2b5c7a9"


def upload_to_imgbb(file_path, api_key):
    """上传图片到 ImgBB 图床"""
    url = "https://api.imgbb.com/1/upload"

    with open(file_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    payload = {
        "key": api_key,
        "image": image_data,
        "name": os.path.basename(file_path)
    }

    print(f"↑ 正在上传到图床...")
    resp = requests.post(url, data=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    if result.get("success"):
        return result["data"]["url"]
    raise Exception(f"上传失败：{result}")


def send_markdown_with_image(image_url):
    """发送带图片的 Markdown 消息"""
    markdown_text = f"""## 🏃 Nike 跑鞋 - 超写实产品图

![Nike 跑鞋]({image_url})

**产品信息：**
- 品牌：Nike
- 类型：专业跑鞋
- 特点：Flyknit 编织鞋面，气垫鞋底
- 生成时间：2026-02-20

> 超写实产品摄影，工作室灯光效果"""

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Nike 跑鞋 - 超写实产品图",
            "text": markdown_text
        }
    }

    print(f"→ 发送 Markdown 图片消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    return resp.json()


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    try:
        # 1. 上传到图床
        print("1. 上传图片到图床...")
        image_url = upload_to_imgbb(IMAGE_PATH, IMG_BB_API_KEY)
        print(f"   ✓ 图片 URL: {image_url}\n")

        # 2. 发送消息
        print("2. 发送图片到钉钉群...")
        result = send_markdown_with_image(image_url)
        print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

        print()
        print("=" * 50)
        if result.get("errcode") == 0:
            print("✅ 图片发送成功！")
        else:
            print(f"❌ 发送失败：{result}")

    except Exception as e:
        print(f"\n❌ 错误：{e}")


if __name__ == "__main__":
    main()
