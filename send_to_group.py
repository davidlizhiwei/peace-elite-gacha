#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用群机器人 API 发送图片到群聊
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# 图片路径
IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# API 端点
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"

# 机器人 webhook（用于发送）
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"


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


def send_image_by_webhook(media_id):
    """
    使用 webhook 发送图片消息
    钉钉机器人 webhook 发送图片需要 pic_url 参数
    """
    # 钉钉 webhook 图片消息格式
    # 需要一个公网可访问的图片 URL
    # 但我们没有，所以尝试其他方式

    # 方案 1: 尝试使用 media_id 作为 pic_url（可能不行）
    payload = {
        "msgtype": "image",
        "image": {
            "pic_url": media_id  # 尝试使用 media_id
        }
    }

    print("→ 尝试方案 1：使用 media_id 作为 pic_url...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    if result.get("errcode") == 0:
        return True

    # 方案 2: 发送带说明的文本消息
    print("\n→ 方案 2：发送说明消息...")
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"🏃 Nike 跑鞋 - 超写实产品图已生成！\n\n📷 图片信息:\n• 文件：{os.path.basename(IMAGE_PATH)}\n• 路径：{IMAGE_PATH}\n• Media ID: {media_id}\n\n✅ 图片已成功上传到钉钉服务器"
        }
    }

    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    return result.get("errcode") == 0


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片到钉钉群\n")

    try:
        # 1. 获取 token
        print("1. 获取 access token...")
        access_token = get_access_token()
        print(f"   ✓ Token 获取成功\n")

        # 2. 上传图片
        print("2. 上传图片到钉钉媒体服务器...")
        media_id = upload_media(access_token, IMAGE_PATH)
        print(f"   ✓ 上传成功，media_id: {media_id}\n")

        # 3. 发送消息
        print("3. 发送消息到群聊...\n")
        success = send_image_by_webhook(media_id)

        print()
        print("=" * 50)
        if success:
            print("✅ 消息发送成功！")
            print(f"\n说明：图片已上传到钉钉服务器 (media_id: {media_id})")
            print("但由于 webhook 限制，发送的是说明消息而非直接显示图片")
        else:
            print("❌ 发送失败")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
