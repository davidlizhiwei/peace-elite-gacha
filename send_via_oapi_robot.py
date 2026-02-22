#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 oapi.dingtalk.com 群机器人 API 发送图片
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# API 端点
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"
# 群机器人发送消息 API
SEND_URL = "https://oapi.dingtalk.com/topapi/robot/send"


def get_access_token():
    """获取 access token"""
    resp = requests.get(TOKEN_URL, params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET})
    data = resp.json()
    if data.get("errcode") == 0:
        return data["access_token"]
    raise Exception(f"获取 token 失败：{data}")


def upload_media(access_token, file_path):
    """上传媒体文件"""
    url = f"{UPLOAD_URL}?access_token={access_token}&type=image"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传：{os.path.basename(file_path)} ...")
        resp = requests.post(url, files=files)

    data = resp.json()
    print(f"   响应：{json.dumps(data, ensure_ascii=False)}")

    if data.get("errcode") == 0:
        return data.get("media_id")
    raise Exception(f"上传失败：{data}")


def send_image_to_group(access_token, conversation_id, media_id):
    """发送图片到群聊"""
    url = f"{SEND_URL}?access_token={access_token}"
    headers = {"Content-Type": "application/json"}

    # 图片消息
    payload = {
        "chatid": conversation_id,
        "msgtype": "image",
        "image": {
            "media_id": media_id
        }
    }

    print(f"→ 发送到群聊：{conversation_id}")
    resp = requests.post(url, headers=headers, json=payload)
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
        print(f"   ✓ Token 获取成功\n")

        # 2. 上传图片
        print("2. 上传图片...")
        media_id = upload_media(access_token, IMAGE_PATH)
        print(f"   ✓ 上传成功，media_id: {media_id}\n")

        # 3. 获取群聊列表
        print("3. 获取群聊列表...")
        chatlist_url = f"https://oapi.dingtalk.com/chat/list?access_token={access_token}"
        resp = requests.post(chatlist_url, headers={"Content-Type": "application/json"}, json={"cursor": 0, "size": 20})
        chatlist_data = resp.json()
        print(f"   群聊列表响应：{json.dumps(chatlist_data, ensure_ascii=False)}")

        if chatlist_data.get("errcode") == 0 and chatlist_data.get("chat_list"):
            chats = chatlist_data["chat_list"]
            print(f"\n找到 {len(chats)} 个群聊:")
            for i, chat in enumerate(chats):
                print(f"  {i+1}. {chat.get('title', 'N/A')} - chatid: {chat.get('chatid', 'N/A')}")

            # 尝试发送到第一个群聊
            if chats:
                chat_id = chats[0].get("chatid")
                if chat_id:
                    print(f"\n4. 发送到群聊：{chat_id}")
                    result = send_image_to_group(access_token, chat_id, media_id)

                    if result.get("errcode") == 0:
                        print("\n✅ 发送成功！")
                        return

        # fallback: webhook 通知
        print("\n5. 使用 webhook 发送通知...")
        WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

        payload = {
            "msgtype": "text",
            "text": {
                "content": f"🏃 Nike 跑鞋图片已生成！\n\n📷 Media ID: {media_id}\n文件：{os.path.basename(IMAGE_PATH)}"
            }
        }

        resp = requests.post(WEBHOOK_URL, json=payload)
        result = resp.json()
        print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

        if result.get("errcode") == 0:
            print("\n✅ 通知消息发送成功！")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
