#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Webhook 发送消息到钉钉群
"""

import requests
import json

# 配置
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"
CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# API 端点
TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"


def get_access_token():
    """获取 access token"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "appKey": CLIENT_ID,
        "appSecret": CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return result["accessToken"]


def upload_file(access_token, file_path):
    """上传文件"""
    import os
    url = f"{UPLOAD_URL}?access_token={access_token}&type=file"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)

    response.raise_for_status()
    result = response.json()

    if result.get("errcode") == 0:
        return {
            "media_id": result.get("media_id"),
            "created_at": result.get("created_at")
        }
    else:
        raise Exception(f"上传失败：{result}")


def send_text_by_webhook(content, at_all=False):
    """发送文本消息"""
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "isAtAll": at_all
        }
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    return response.json()


def send_markdown_by_webhook(title, markdown_text):
    """发送 Markdown 消息"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": markdown_text
        }
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    return response.json()


def send_link_by_webhook(title, text, message_url, pic_url=""):
    """发送链接卡片消息"""
    payload = {
        "msgtype": "link",
        "link": {
            "title": title,
            "text": text,
            "messageUrl": message_url,
            "picUrl": pic_url
        }
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    return response.json()


def main():
    import os
    print("=== 发送消息到钉钉群 ===\n")

    # 1. 发送文本消息测试
    print("1. 发送文本消息测试...")
    result = send_text_by_webhook("你好，这是来自 Python 脚本的测试消息！\n时间：2026-02-20")

    if result.get("errcode") == 0:
        print("   ✓ 文本消息发送成功！\n")
    else:
        print(f"   ✗ 文本消息失败：{result}\n")

    # 2. 上传文件
    test_file = os.path.join(os.path.dirname(__file__), "test_document.pdf")
    print(f"2. 上传文件：{os.path.basename(test_file)}")

    if not os.path.exists(test_file):
        print(f"   ✗ 文件不存在：{test_file}")
        return

    access_token = get_access_token()
    upload_result = upload_file(access_token, test_file)
    print(f"   ✓ 上传成功")
    print(f"   media_id: {upload_result['media_id']}")
    print(f"   created_at: {upload_result['created_at']}\n")

    # 3. 发送 Markdown 消息（带文件信息）
    print("3. 发送文件通知（Markdown 格式）...")

    markdown_text = f"""## 📄 文件上传通知

**文件名：** test_document.pdf
**大小：** 测试文件
**上传时间：** {upload_result['created_at']}

> ⚠️ 注意：钉钉 Webhook 机器人不支持直接发送文件消息
> 请使用企业应用方式发送真实文件，或使用链接方式分享文件

---
*此消息由 Python 脚本自动生成*"""

    result = send_markdown_by_webhook("文件上传通知", markdown_text)

    if result.get("errcode") == 0:
        print("   ✓ Markdown 消息发送成功！\n")
    else:
        print(f"   ✗ Markdown 消息失败：{result}\n")

    # 4. 发送链接消息（示例）
    print("4. 发送链接卡片消息...")

    result = send_link_by_webhook(
        title="测试文档下载",
        text="这是一个测试 PDF 文件的下载链接",
        message_url="https://example.com/download/test.pdf"  # 替换为实际文件链接
    )

    if result.get("errcode") == 0:
        print("   ✓ 链接消息发送成功！\n")
    else:
        print(f"   ✗ 链接消息失败：{result}\n")

    print("=" * 50)
    print("总结：")
    print("- Webhook 方式支持：文本、Markdown、链接卡片消息")
    print("- Webhook 方式不支持：直接发送文件（file 类型）")
    print("- 如需发送真实文件，请使用企业应用方式（需要 conversation_id）")


if __name__ == "__main__":
    main()
