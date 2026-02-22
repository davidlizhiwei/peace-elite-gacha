#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用企业应用接口发送图片到群聊
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "robot35511618523509219"

# 图片路径
IMAGE_PATH = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

# API 端点
TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
UPLOAD_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/upload"
SEND_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/send"


def get_access_token():
    """获取 access token"""
    resp = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/json"},
        json={"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
    )
    data = resp.json()
    print(f"✓ Token: {data.get('accessToken', '')[:30]}...")
    return data["accessToken"]


def upload_file(access_token, file_path):
    """上传文件"""
    headers = {'x-acs-dingtalk-access-token': access_token}

    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传图片：{os.path.basename(file_path)} ...")
        resp = requests.post(UPLOAD_URL, headers=headers, files=files)

    data = resp.json()
    print(f"   上传响应：{json.dumps(data, ensure_ascii=False)}")

    if "mediaId" in data:
        return {"media_id": data["mediaId"], "file_name": data.get("fileName", os.path.basename(file_path))}
    raise Exception(f"上传失败：{data}")


def send_image_message(access_token, robot_code, conversation_id, media_id, file_name):
    """发送图片消息到群聊"""
    headers = {
        'x-acs-dingtalk-access-token': access_token,
        'Content-Type': 'application/json'
    }

    # 图片消息类型
    payload = {
        "robotCode": robot_code,
        "msgKey": "sampleImage",
        "msgParam": {
            "mediaId": media_id,
            "fileName": file_name
        },
        "conversationId": conversation_id
    }

    print(f"→ 发送图片到会话：{conversation_id}")
    resp = requests.post(SEND_URL, headers=headers, json=payload)
    result = resp.json()
    print(f"   发送响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送图片：{os.path.basename(IMAGE_PATH)}\n")

    # 需要 conversation_id - 尝试几个可能的值
    # 从之前 webhook 成功发送来看，机器人确实在某个群里
    # 让我们尝试获取机器人信息来找到 conversation_id

    access_token = get_access_token()

    # 上传文件
    print("\n1. 上传文件...")
    upload_result = upload_file(access_token, IMAGE_PATH)
    media_id = upload_result["media_id"]
    file_name = upload_result["file_name"]
    print(f"✓ 上传成功：media_id={media_id}\n")

    # 现在需要找到 conversation_id
    # 尝试使用机器人发送消息的 API 来获取
    print("2. 尝试获取机器人会话...")

    # 尝试调用机器人会话列表 API
    headers = {'x-acs-dingtalk-access-token': access_token}

    # 尝试获取机器人的 chatId
    chat_resp = requests.get(
        "https://api.dingtalk.com/v1.0/robots/chats",
        headers=headers
    )
    print(f"   机器人聊天列表：{chat_resp.json()}")

    # 如果上面不行，尝试其他方式
    # 使用旧版 API 获取机器人信息
    token_old = requests.get(
        "https://oapi.dingtalk.com/gettoken",
        params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET}
    ).json()["access_token"]

    # 获取机器人详情
    robot_info_resp = requests.get(
        f"https://oapi.dingtalk.com/robot/get?access_token={token_old}"
    )
    print(f"   机器人信息：{robot_info_resp.json()}")


if __name__ == "__main__":
    main()
