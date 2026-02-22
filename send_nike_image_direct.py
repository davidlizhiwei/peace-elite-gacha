#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接发送 Nike 跑鞋图片到钉钉群
使用企业应用 API 上传并发送图片
"""

import os
import time
import requests
import json


# 配置
CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "robot35511618523509219"
CONVERSATION_ID = "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE"

# API 端点
TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
UPLOAD_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/upload"
SEND_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/send"


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
    print(f"✓ 已获取 access token")
    return result["accessToken"]


def upload_image(access_token, file_path):
    """上传图片到钉钉"""
    url = UPLOAD_URL

    headers = {
        'x-acs-dingtalk-access-token': access_token
    }

    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传图片：{os.path.basename(file_path)} ...")
        response = requests.post(url, headers=headers, files=files)

    response.raise_for_status()
    result = response.json()

    if "mediaId" not in result:
        raise Exception(f"上传失败：{result}")

    print(f"✓ 图片上传成功，mediaId: {result['mediaId']}")
    return {
        "media_id": result["mediaId"],
        "file_name": result.get("fileName", os.path.basename(file_path))
    }


def send_image(robot_code, conversation_id, media_id, file_name, access_token):
    """发送图片到群聊"""
    url = SEND_URL

    headers = {
        'x-acs-dingtalk-access-token': access_token,
        'Content-Type': 'application/json'
    }

    # 钉钉图片消息类型
    payload = {
        "robotCode": robot_code,
        "msgKey": "sampleImage",  # 图片消息类型
        "msgParam": {
            "mediaId": media_id,
            "fileName": file_name
        },
        "conversationId": conversation_id
    }

    print(f"→ 正在发送图片到群聊：{conversation_id} ...")
    response = requests.post(url, headers=headers, json=payload)

    response.raise_for_status()
    result = response.json()

    if result.get("code") != 0:
        raise Exception(f"发送失败：{result}")

    print(f"✓ 图片发送成功！")
    return result


def main():
    # 图片路径
    image_path = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

    if not os.path.exists(image_path):
        print(f"❌ 图片不存在：{image_path}")
        return

    print(f"📷 准备发送图片：{os.path.basename(image_path)}")
    print(f"📍 目标群聊：{CONVERSATION_ID}")
    print()

    try:
        # 1. 获取 token
        access_token = get_access_token()

        # 2. 上传图片
        upload_result = upload_image(access_token, image_path)

        # 3. 发送图片
        send_result = send_image(
            robot_code=ROBOT_CODE,
            conversation_id=CONVERSATION_ID,
            media_id=upload_result["media_id"],
            file_name=upload_result["file_name"],
            access_token=access_token
        )

        print()
        print("=" * 50)
        print("✅ 发送完成！")
        print(f"响应：{json.dumps(send_result, ensure_ascii=False)}")

    except Exception as e:
        print()
        print(f"❌ 发送失败：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
