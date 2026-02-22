#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终尝试：使用 webhook 发送 image 类型消息
需要一个公网可访问的图片 URL
"""

import os
import requests
import json
import base64

WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"
IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# 尝试使用 free 图床
def upload_to_free_imgbb(file_path):
    """上传图片到 imgbb（不需要 API key 的方式）"""
    # 使用 https://imgbb.com/ 的匿名上传
    url = "https://api.imgbb.com/1/upload"

    # 读取图片并 base64 编码
    with open(file_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # 尝试不使用 API key（匿名上传）
    payload = {
        "image": image_data,
        "name": os.path.basename(file_path)
    }

    print("↑ 正在上传到 imgbb...")
    resp = requests.post(url, data=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    if result.get("success") and "url" in result.get("data", {}):
        return result["data"]["url"]
    return None


def upload_to_catbox(file_path):
    """上传到 catbox.moe"""
    url = "https://catbox.moe/user/api.php"

    with open(file_path, 'rb') as f:
        files = {
            'reqtype': (None, 'fileupload'),
            'file': (os.path.basename(file_path), f)
        }
        print("↑ 正在上传到 catbox.moe...")
        resp = requests.post(url, files=files)

    result = resp.text.strip()
    print(f"   响应：{result}")

    if result.startswith("https://"):
        return result
    return None


def send_image_via_webhook(image_url):
    """使用 webhook 发送图片消息"""
    # 钉钉 webhook image 消息需要 pic_url
    payload = {
        "msgtype": "image",
        "image": {
            "pic_url": image_url
        }
    }

    print(f"→ 发送图片消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def send_markdown_via_webhook(image_url):
    """使用 Markdown 发送图片"""
    markdown_text = f"""## 🏃 Nike 跑鞋 - 超写实产品图

![Nike 跑鞋]({image_url})

**产品信息：**
- 品牌：Nike
- 类型：专业跑鞋
- 特点：Flyknit 编织鞋面，气垫鞋底

> 超写实产品摄影，工作室灯光效果"""

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Nike 跑鞋",
            "text": markdown_text
        }
    }

    print(f"→ 发送 Markdown 图片消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    # 尝试不同的图床
    image_url = None

    # 1. 尝试 catbox.moe
    print("1. 尝试上传到 catbox.moe...")
    image_url = upload_to_catbox(IMAGE_PATH)

    # 2. 如果失败，尝试 imgbb
    if not image_url:
        print("\n2. 尝试上传到 imgbb...")
        image_url = upload_to_free_imgbb(IMAGE_PATH)

    if not image_url:
        print("\n❌ 图片上传失败")
        print("使用 webhook 发送文本通知...")

        # 发送文本通知
        payload = {
            "msgtype": "text",
            "text": {
                "content": f"🏃 Nike 跑鞋图片已生成！\n\n📷 文件：{os.path.basename(IMAGE_PATH)}\n路径：{IMAGE_PATH}"
            }
        }
        resp = requests.post(WEBHOOK_URL, json=payload)
        result = resp.json()
        print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
        return

    print(f"\n✓ 图片上传成功，URL: {image_url}\n")

    # 3. 发送图片消息
    print("3. 发送图片到钉钉...")

    # 先尝试 image 类型
    result = send_image_via_webhook(image_url)

    if result.get("errcode") != 0:
        print("\nimage 类型失败，尝试 Markdown...")
        result = send_markdown_via_webhook(image_url)

    print()
    print("=" * 50)
    if result.get("errcode") == 0:
        print("✅ 图片发送成功！")
    else:
        print(f"❌ 发送失败：{result}")


if __name__ == "__main__":
    main()
