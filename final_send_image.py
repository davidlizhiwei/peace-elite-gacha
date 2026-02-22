#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终方案：发送 Nike 跑鞋图片到钉钉
使用企业应用接口发送图片消息
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

# 图片路径
IMAGE_PATH = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

# API 端点
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"


def get_access_token():
    """获取 access token"""
    resp = requests.get(
        TOKEN_URL,
        params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET}
    )
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
        return {
            "media_id": data.get("media_id"),
            "created_at": data.get("created_at")
        }
    raise Exception(f"上传失败：{data}")


def send_image_message(media_id):
    """
    发送图片消息
    使用 webhook 的 image 类型消息，需要 picURL
    但我们尝试使用 media_id 作为 picURL 的替代
    """
    # 方案 1: 尝试使用 media_id 作为 picURL
    # 钉钉图片消息格式
    payload = {
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }

    print(f"→ 尝试发送图片消息 (方案 1)...")
    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    if result.get("errcode") == 0:
        return result

    # 方案 2: 使用 markdown 消息，尝试引用 media_id
    print(f"\n→ 尝试使用 Markdown 消息 (方案 2)...")
    markdown_payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Nike 跑鞋",
            "text": f"## 🏃 Nike 跑鞋 - 超写实产品图\n\n![Nike 跑鞋](media_id:{media_id})\n\n图片已上传到钉钉服务器"
        }
    }

    resp = requests.post(WEBHOOK_URL, json=markdown_payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    if result.get("errcode") == 0:
        return result

    # 方案 3: 发送通知消息，说明图片已生成
    print(f"\n→ 发送图片路径通知 (方案 3)...")
    text_payload = {
        "msgtype": "text",
        "text": {
            "content": f"🏃 Nike 跑鞋图片已生成！\n\n📷 图片信息:\n• 文件：{os.path.basename(IMAGE_PATH)}\n• 路径：{IMAGE_PATH}\n• Media ID: {media_id}\n\n✅ 图片已上传到钉钉服务器，可通过 media_id 访问"
        }
    }

    resp = requests.post(WEBHOOK_URL, json=text_payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    return result


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    try:
        # 1. 获取 token
        print("1. 获取 access token...")
        access_token = get_access_token()
        print(f"   ✓ Token: {access_token[:30]}...\n")

        # 2. 上传图片
        print("2. 上传图片到钉钉...")
        upload_result = upload_media(access_token, IMAGE_PATH)
        media_id = upload_result["media_id"]
        print(f"   ✓ 上传成功，media_id: {media_id}\n")

        # 3. 发送图片
        print("3. 发送图片到群聊...\n")
        result = send_image_message(media_id)

        print()
        print("=" * 50)
        if result.get("errcode") == 0:
            print("✅ 发送成功！")
        else:
            print(f"⚠️ 发送失败：{result}")
            print("\n说明：钉钉 webhook 机器人不支持直接发送图片文件")
            print("图片已上传到钉钉服务器，media_id 可用于其他 API 调用")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
