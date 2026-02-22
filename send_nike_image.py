#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片到钉钉群
使用 Markdown 消息类型展示图片
"""

import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json


def generate_sign(secret: str) -> str:
    """生成加签参数"""
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = f'{timestamp}\n{secret}'
    string_to_sign_enc = string_to_sign.encode('utf-8')

    hmac_code = hmac.new(
        secret_enc,
        string_to_sign_enc,
        digestmod=hashlib.sha256
    ).digest()

    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"&timestamp={timestamp}&sign={sign}"


def send_markdown_image(webhook_url: str, secret: str, image_path: str) -> dict:
    """
    发送 Markdown 消息（包含图片）到钉钉群

    Args:
        webhook_url: 机器人 Webhook URL
        secret: 加签密钥
        image_path: 本地图片路径

    Returns:
        API 响应
    """
    # 生成加签 URL
    url = webhook_url + generate_sign(secret)

    # 获取图片文件名
    image_filename = os.path.basename(image_path)

    # 钉钉 Markdown 图片语法：![图片描述](图片 URL)
    # 由于是本地图片，我们需要使用文件上传方式或者使用链接
    # 这里使用 Markdown 格式，但需要图片有可访问的 URL

    # 方案：发送文本消息说明，图片需要通过其他方式分享
    # 或者使用 link 类型消息

    # 由于 webhook 不支持直接上传本地图片，我们使用 Markdown 消息说明
    markdown_text = f"""## 🏃 Nike 跑鞋 - 超写实产品图

![Nike 跑鞋](file://{image_path})

**产品信息：**
- 品牌：Nike
- 类型：专业跑鞋
- 特点：Flyknit 编织鞋面，气垫鞋底
- 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}

> 图片已生成：`{image_path}`
"""

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Nike 跑鞋 - 超写实产品图",
            "text": markdown_text
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def send_text_with_file_path(webhook_url: str, secret: str, image_path: str) -> dict:
    """
    发送文本消息，包含图片路径信息
    """
    url = webhook_url + generate_sign(secret)

    image_filename = os.path.basename(image_path)
    image_size = os.path.getsize(image_path) / 1024 / 1024  # MB

    content = f"""🏃 Nike 跑鞋 - 超写实产品图已生成！

📷 图片信息：
• 文件名：{image_filename}
• 大小：{image_size:.2f} MB
• 路径：{image_path}
• 时间：{time.strftime('%Y-%m-%d %H:%M:%S')}

✅ 图片已保存到本地，可通过文件管理器查看"""

    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


if __name__ == "__main__":
    # 配置
    WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"
    WEBHOOK_SECRET = ""  # 如果没有设置加签，留空即可

    # 图片路径
    image_path = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

    if not os.path.exists(image_path):
        print(f"❌ 图片不存在：{image_path}")
        exit(1)

    print(f"📷 准备发送图片：{os.path.basename(image_path)}")

    # 发送消息
    result = send_text_with_file_path(WEBHOOK_URL, WEBHOOK_SECRET, image_path)

    print(f"📤 发送结果：{json.dumps(result, ensure_ascii=False)}")

    if result.get("errcode") == 0:
        print("✅ 消息发送成功！")
    else:
        print(f"❌ 发送失败：{result}")
