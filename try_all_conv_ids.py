#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试所有可能的 conversation_id 格式
使用钉钉机器人消息文件发送 API
"""

import os
import requests
import json
import time

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "dingdwlipjehprtrzc6s"

IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# API 端点
TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
UPLOAD_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/upload"
SEND_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/send"


def get_access_token():
    """获取 access token"""
    headers = {"Content-Type": "application/json"}
    payload = {"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
    resp = requests.post(TOKEN_URL, headers=headers, json=payload)
    data = resp.json()
    return data.get("accessToken")


def upload_file(access_token, file_path):
    """上传文件"""
    url = UPLOAD_URL
    headers = {'x-acs-dingtalk-access-token': access_token}

    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        resp = requests.post(url, headers=headers, files=files)

    return resp.json()


def send_file(access_token, robot_code, conversation_id, media_id, file_name):
    """发送文件"""
    url = SEND_URL
    headers = {
        'x-acs-dingtalk-access-token': access_token,
        'Content-Type': 'application/json'
    }

    payload = {
        "robotCode": robot_code,
        "msgKey": "sampleImage",
        "msgParam": {
            "mediaId": media_id,
            "fileName": file_name
        },
        "conversationId": conversation_id
    }

    resp = requests.post(url, headers=headers, json=payload)
    return resp.json()


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    # 获取 token
    print("1. 获取 access token...")
    access_token = get_access_token()
    if not access_token:
        print("   ❌ 获取 token 失败")
        return
    print(f"   ✓ Token: {access_token[:30]}...\n")

    # 上传图片
    print("2. 上传图片...")
    upload_result = upload_file(access_token, IMAGE_PATH)
    print(f"   上传响应：{json.dumps(upload_result, ensure_ascii=False)}")

    if "mediaId" not in upload_result:
        print("   ❌ 上传失败")
        return

    media_id = upload_result["mediaId"]
    file_name = upload_result.get("fileName", os.path.basename(IMAGE_PATH))
    print(f"   ✓ 上传成功，media_id: {media_id}\n")

    # 尝试不同的 conversation_id
    print("3. 尝试发送...")

    # 可能的 conversation_id 格式
    test_conv_ids = [
        # 之前用过的
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE",
        # 可能的变体
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE01",
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE02",
        # 其他格式
        "dingdwlipjehprtrzc6s",  # 使用 client_id
    ]

    for conv_id in test_conv_ids:
        print(f"\n尝试会话：{conv_id}")
        result = send_file(access_token, ROBOT_CODE, conv_id, media_id, file_name)
        print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

        if result.get("code") == 0:
            print(f"\n✅ 发送成功！")
            return

    print("\n⚠️ 所有尝试都失败了")
    print("\n说明：")
    print("- 图片已成功上传到钉钉服务器")
    print(f"- media_id: {media_id}")
    print("- 需要正确的 conversation_id 才能发送到群聊")


if __name__ == "__main__":
    main()
