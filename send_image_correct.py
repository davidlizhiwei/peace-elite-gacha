#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片到钉钉
使用正确的 API 端点
"""

import os
import sys
import json
import requests
import time

# 配置
CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "dingdwlipjehprtrzc6s"

# 图片路径（压缩后）
IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# API 端点 - 使用 oapi.dingtalk.com
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"
SEND_URL = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"


def get_access_token():
    """获取 access token"""
    resp = requests.get(TOKEN_URL, params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET})
    data = resp.json()
    if data.get("errcode") == 0:
        return data["access_token"]
    raise Exception(f"获取 token 失败：{data}")


def upload_media(access_token, file_path, media_type="image"):
    """上传媒体文件"""
    url = f"{UPLOAD_URL}?access_token={access_token}&type={media_type}"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传图片：{os.path.basename(file_path)} ...")
        resp = requests.post(url, files=files)

    data = resp.json()
    print(f"   响应：{json.dumps(data, ensure_ascii=False)}")

    if data.get("errcode") == 0:
        return data.get("media_id")
    raise Exception(f"上传失败：{data}")


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    try:
        # 1. 获取 token
        print("1. 获取 access token...")
        access_token = get_access_token()
        print(f"   ✓ Token 获取成功\n")

        # 2. 上传图片
        print("2. 上传图片...")
        media_id = upload_media(access_token, IMAGE_PATH)
        print(f"   ✓ 上传成功，media_id: {media_id}\n")

        # 3. 发送图片消息（使用 media_id）
        print("3. 发送图片消息...")

        # 注意：我们需要一个有效的 conversation_id
        # 由于 webhook 可以发送消息，说明机器人在某个群里
        # 让我们尝试使用 webhook 发送图片消息

        WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

        # 尝试使用 file 类型发送（需要 media_id）
        payload = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }

        print(f"→ 发送文件消息到群聊...")
        resp = requests.post(WEBHOOK_URL, json=payload)
        result = resp.json()
        print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

        print()
        print("=" * 50)
        if result.get("errcode") == 0:
            print("✅ 发送成功！")
        else:
            print(f"⚠️ 发送失败：{result}")
            print("\n尝试使用 Markdown 消息...")

            # 尝试 Markdown 消息
            markdown_payload = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "Nike 跑鞋",
                    "text": f"## 🏃 Nike 跑鞋 - 超写实产品图\n\n![Nike 跑鞋](media_id:{media_id})\n\n图片已上传到钉钉服务器，media_id: `{media_id}`"
                }
            }

            resp = requests.post(WEBHOOK_URL, json=markdown_payload)
            result = resp.json()
            print(f"   Markdown 响应：{json.dumps(result, ensure_ascii=False)}")

            if result.get("errcode") == 0:
                print("\n✅ Markdown 消息发送成功！")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
