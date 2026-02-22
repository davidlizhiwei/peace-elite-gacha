#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传 Nike 跑鞋图片到钉钉媒体服务器并发送
"""

import os
import time
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

# 图片路径
IMAGE_PATH = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

def get_access_token():
    """获取 access token"""
    resp = requests.get(
        "https://oapi.dingtalk.com/gettoken",
        params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET}
    )
    data = resp.json()
    if data.get("errcode") == 0:
        return data["access_token"]
    raise Exception(f"获取 token 失败：{data}")

def upload_media(access_token, file_path, media_type="image"):
    """上传媒体文件到钉钉"""
    url = f"https://oapi.dingtalk.com/media/upload"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        params = {
            'access_token': access_token,
            'type': media_type
        }

        print(f"↑ 正在上传图片：{os.path.basename(file_path)} ...")
        resp = requests.post(url, params=params, files=files)

    data = resp.json()
    print(f"   上传响应：{json.dumps(data, ensure_ascii=False)}")

    if data.get("errcode") == 0:
        return {
            "media_id": data.get("media_id"),
            "created_at": data.get("created_at")
        }
    else:
        raise Exception(f"上传失败：{data}")

def send_image_by_webhook(media_id):
    """使用 webhook 发送图片消息"""
    # 钉钉图片消息格式
    payload = {
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }

    print(f"→ 正在发送图片消息...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   发送响应：{json.dumps(result, ensure_ascii=False)}")
    return result

def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送图片：{os.path.basename(IMAGE_PATH)}")
    print()

    try:
        # 1. 获取 token
        print("1. 获取 access token...")
        access_token = get_access_token()
        print(f"   ✓ Token: {access_token[:30]}...\n")

        # 2. 上传图片
        print("2. 上传图片到钉钉媒体服务器...")
        upload_result = upload_media(access_token, IMAGE_PATH)
        media_id = upload_result["media_id"]
        print(f"   ✓ 上传成功，media_id: {media_id}\n")

        # 3. 发送图片
        print("3. 发送图片到群聊...")
        send_result = send_image_by_webhook(media_id)

        print()
        if send_result.get("errcode") == 0:
            print("=" * 50)
            print("✅ 图片发送成功！")
        else:
            print(f"❌ 发送失败：{send_result}")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
