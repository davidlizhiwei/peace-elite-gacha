#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用之前上传的 media_id 发送图片
钉钉媒体上传后，media_id 在 3 天内有效
"""

import requests
import json

# 之前成功上传的 media_id
MEDIA_ID = "@lALPM2POKobdusHNAyDNAyA"

# 机器人 webhook
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"


def try_send_image(media_id):
    """尝试发送 image 类型消息"""
    # 钉钉 webhook image 消息格式
    # 根据文档，需要 pic_url 参数
    # 但我们尝试使用 media_id
    payload = {
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }

    print("→ 尝试发送 image 类型消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def try_send_file(media_id):
    """尝试发送 file 类型消息"""
    payload = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }

    print("→ 尝试发送 file 类型消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def try_send_markdown(media_id):
    """尝试发送 Markdown 消息"""
    markdown_text = f"""## 🏃 Nike 跑鞋 - 超写实产品图

![Nike 跑鞋](dingtalk://dingtalk/media?media_id={media_id})

**产品信息：**
- 品牌：Nike
- 类型：专业跑鞋

> Media ID: `{media_id}`"""

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Nike 跑鞋",
            "text": markdown_text
        }
    }

    print("→ 尝试发送 Markdown 消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def main():
    print(f"📷 使用已上传的 media_id 发送 Nike 跑鞋图片\n")
    print(f"Media ID: {MEDIA_ID}\n")

    # 尝试不同的消息类型
    print("=" * 50)

    # 1. image 类型
    result = try_send_image(MEDIA_ID)
    if result.get("errcode") == 0:
        print("\n✅ image 类型发送成功！")
        return

    # 2. file 类型
    print()
    result = try_send_file(MEDIA_ID)
    if result.get("errcode") == 0:
        print("\n✅ file 类型发送成功！")
        return

    # 3. Markdown 类型
    print()
    result = try_send_markdown(MEDIA_ID)
    if result.get("errcode") == 0:
        print("\n✅ Markdown 类型发送成功！")
        return

    print("\n⚠️ 所有方式都失败了")
    print("钉钉 webhook 不支持直接使用 media_id 发送图片")


if __name__ == "__main__":
    main()
