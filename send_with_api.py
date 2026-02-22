#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片到钉钉群聊
使用之前成功的 API 组合
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

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
    print(f"✓ Token: {data.get('accessToken', '')[:30]}...")
    return data["accessToken"]


def upload_file(access_token, file_path):
    """上传文件"""
    url = UPLOAD_URL
    headers = {'x-acs-dingtalk-access-token': access_token}

    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传：{os.path.basename(file_path)} ...")
        resp = requests.post(url, headers=headers, files=files)

    data = resp.json()
    print(f"   响应：{json.dumps(data, ensure_ascii=False)}")

    if "mediaId" in data:
        return {"mediaId": data["mediaId"], "fileName": data.get("fileName", os.path.basename(file_path))}
    raise Exception(f"上传失败：{data}")


def send_file(access_token, robot_code, conversation_id, media_id, file_name):
    """发送文件到群聊"""
    url = SEND_URL
    headers = {
        'x-acs-dingtalk-access-token': access_token,
        'Content-Type': 'application/json'
    }

    payload = {
        "robotCode": robot_code,
        "msgKey": "sampleImage",  # 图片类型
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

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    access_token = get_access_token()

    # 上传文件
    print("\n1. 上传文件...")
    upload_result = upload_file(access_token, IMAGE_PATH)
    media_id = upload_result["mediaId"]
    file_name = upload_result["fileName"]
    print(f"✓ 上传成功：media_id={media_id}\n")

    # 尝试不同的 conversation_id
    print("2. 尝试发送...")

    # 可能的 conversation_id 格式
    test_conv_ids = [
        # 之前用过的格式
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE",
        # 其他可能格式
        "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE01",
    ]

    robot_code = "dingdwlipjehprtrzc6s"

    for conv_id in test_conv_ids:
        print(f"\n尝试：{conv_id}")
        result = send_file(access_token, robot_code, conv_id, media_id, file_name)

        if result.get("code") == 0:
            print("\n✅ 发送成功！")
            return
        else:
            print(f"   失败：{result.get('message', result)}")

    print("\n所有尝试都失败了")


if __name__ == "__main__":
    main()
