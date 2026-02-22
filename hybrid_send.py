#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合方式发送：使用 oapi 上传，使用 v1.0 发送
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "dingdwlipjehprtrzc6s"

IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# API 端点
V1_TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
OAPI_TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
OAPI_UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"
V1_SEND_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/send"


def get_v1_token():
    """获取 v1.0 access token"""
    headers = {"Content-Type": "application/json"}
    payload = {"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
    resp = requests.post(V1_TOKEN_URL, headers=headers, json=payload)
    data = resp.json()
    return data.get("accessToken")


def get_oapi_token():
    """获取 oapi access token"""
    resp = requests.get(OAPI_TOKEN_URL, params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET})
    data = resp.json()
    if data.get("errcode") == 0:
        return data["access_token"]
    return None


def upload_via_oapi(access_token, file_path):
    """通过 oapi 上传"""
    url = f"{OAPI_UPLOAD_URL}?access_token={access_token}&type=image"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传（oapi）：{os.path.basename(file_path)} ...")
        resp = requests.post(url, files=files)

    data = resp.json()
    print(f"   响应：{json.dumps(data, ensure_ascii=False)}")

    if data.get("errcode") == 0:
        return data.get("media_id")
    return None


def send_via_v1(access_token, robot_code, conversation_id, media_id, file_name):
    """通过 v1.0 发送"""
    url = V1_SEND_URL
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

    print(f"→ 发送到会话：{conversation_id}")
    resp = requests.post(url, headers=headers, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片（混合方式）\n")

    # 1. 获取 tokens
    print("1. 获取 tokens...")
    v1_token = get_v1_token()
    oapi_token = get_oapi_token()

    if not v1_token or not oapi_token:
        print("   ❌ 获取 token 失败")
        return

    print(f"   ✓ v1.0 Token: {v1_token[:30]}...")
    print(f"   ✓ oapi Token: {oapi_token[:30]}...\n")

    # 2. 通过 oapi 上传
    print("2. 上传图片（使用 oapi）...")
    media_id = upload_via_oapi(oapi_token, IMAGE_PATH)

    if not media_id:
        print("   ❌ 上传失败")
        return

    print(f"   ✓ 上传成功，media_id: {media_id}\n")

    # 3. 通过 v1.0 发送
    print("3. 发送图片（使用 v1.0 API）...")

    test_conv_ids = [
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE",
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE01",
    ]

    file_name = os.path.basename(IMAGE_PATH)

    for conv_id in test_conv_ids:
        print(f"\n尝试：{conv_id}")
        result = send_via_v1(v1_token, ROBOT_CODE, conv_id, media_id, file_name)

        if result.get("code") == 0:
            print(f"\n✅ 发送成功！")
            return

    print("\n⚠️ 所有 conversation_id 都失败了")

    #  fallback: 使用 webhook 发送通知
    print("\n4. 使用 webhook 发送通知...")
    WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

    payload = {
        "msgtype": "text",
        "text": {
            "content": f"🏃 Nike 跑鞋图片已生成！\n\n📷 图片已上传到钉钉服务器\nMedia ID: {media_id}\n\n✅ 图片文件：{file_name}"
        }
    }

    resp = requests.post(WEBHOOK_URL, json=payload)
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")

    if result.get("errcode") == 0:
        print("\n✅ 通知消息发送成功！")


if __name__ == "__main__":
    main()
