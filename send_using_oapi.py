#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片到钉钉
使用 oapi.dingtalk.com API
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# API 端点 - 使用 oapi
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"


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
        print(f"↑ 正在上传：{os.path.basename(file_path)} ...")
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

        # 3. 使用 webhook 发送消息
        print("3. 发送消息到群聊...")

        WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

        # 发送文本消息，包含 media_id
        payload = {
            "msgtype": "text",
            "text": {
                "content": f"🏃 Nike 跑鞋 - 超写实产品图已生成！\n\n📷 图片已上传到钉钉服务器\nMedia ID: {media_id}\n\n文件：{os.path.basename(IMAGE_PATH)}"
            }
        }

        resp = requests.post(WEBHOOK_URL, json=payload)
        result = resp.json()
        print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

        print()
        print("=" * 50)
        if result.get("errcode") == 0:
            print("✅ 消息发送成功！")
            print(f"\n图片已上传到钉钉服务器，media_id: {media_id}")
            print("可以使用此 media_id 通过其他 API 发送图片")
        else:
            print(f"❌ 发送失败：{result}")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
