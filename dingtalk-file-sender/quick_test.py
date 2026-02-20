#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试：获取群聊列表并发送文件
使用钉钉开放平台 v2.0 API
"""

import os
import sys
import json
import requests
import time

# 配置
CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "dingdwlipjehprtrzc6s"

# API 端点 (v2.0)
TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"
SEND_URL = "https://oapi.dingtalk.com/robot/send"
CHAT_LIST_URL = "https://oapi.dingtalk.com/chat/top"


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


def list_chats(access_token):
    """获取群聊列表"""
    # v2.0 API 使用不同的认证方式
    url = f"{CHAT_LIST_URL}?access_token={access_token}"

    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        if result.get("errcode") == 0:
            chats = result.get("chat_list", [])

            print("\n=== 群聊列表 ===")
            for i, chat in enumerate(chats, 1):
                print(f"{i}. 名称：{chat.get('name', 'N/A')}")
                print(f"   群 ID: {chat.get('chatid', 'N/A')}")
                print(f"   会话 ID: {chat.get('conversation_id', 'N/A')}")
                print()

            return chats
        else:
            print(f"获取群聊失败：{result}")
            return []
    else:
        print(f"获取群聊失败：{response.status_code} - {response.text}")
        return []


def upload_file(access_token, file_path):
    """上传文件 (v2.0 API)"""
    url = f"{UPLOAD_URL}?access_token={access_token}&type=file"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)

    response.raise_for_status()
    result = response.json()

    if result.get("errcode") == 0:
        print(f"✓ 文件上传成功，media_id: {result.get('media_id')}")
        return {
            "media_id": result.get("media_id"),
            "file_name": os.path.basename(file_path)
        }
    else:
        print(f"文件上传失败：{result}")
        return None


def send_file(access_token, webhook_url, media_id, file_name):
    """发送文件（通过 webhook）"""
    # 注意：webhook 方式发送文件需要使用 media_id
    payload = {
        "msgtype": "file",
        "file": {
            "media_id": media_id
        }
    }

    url = f"{webhook_url}"
    response = requests.post(url, json=payload)
    result = response.json()

    if result.get("errcode") == 0:
        print(f"✓ 文件发送成功！")
        return result
    else:
        print(f"发送失败：{result}")
        return result


def main():
    print("=== 钉钉文件发送测试 ===\n")

    # 1. 获取 token
    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"获取 token 失败：{e}")
        return

    # 2. 获取群聊列表
    chats = list_chats(access_token)

    if not chats:
        print("\n未找到群聊，请确认机器人已添加到群聊")
        print("\n或者你可以直接提供 webhook URL 来发送文件")
        webhook_url = input("请输入 webhook URL（或按回车跳过）：> ").strip()

        if webhook_url:
            # 使用 webhook 方式发送
            test_file = os.path.join(os.path.dirname(__file__), "test_document.pdf")
            if os.path.exists(test_file):
                print(f"\n准备发送文件：{os.path.basename(test_file)}")

                # 先上传文件
                upload_result = upload_file(access_token, test_file)
                if upload_result:
                    # webhook 方式发送文件需要 media_id
                    # 但 webhook 的 file 类型消息需要文件已通过其他方式上传
                    print("\n注意：Webhook 方式发送文件需要先在钉钉后台上传")
                    print("建议使用企业应用方式发送")
            return
        else:
            return

    # 3. 让用户选择群聊
    print("请选择要发送文件的群聊（输入序号，或输入 'q' 退出）：")
    choice = input("> ")

    if choice.lower() == 'q':
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(chats):
            conversation_id = chats[idx]["conversation_id"]
            print(f"\n已选择：{chats[idx]['name']}")
            print(f"会话 ID: {conversation_id}")
        else:
            print("无效的选择")
            return
    except ValueError:
        print("请输入有效的数字")
        return

    # 4. 上传并发送文件
    test_file = os.path.join(os.path.dirname(__file__), "test_document.pdf")

    if not os.path.exists(test_file):
        print(f"测试文件不存在：{test_file}")
        return

    print(f"\n准备发送文件：{os.path.basename(test_file)}")

    upload_result = upload_file(access_token, test_file)
    if not upload_result:
        return

    print("\n文件已上传，但发送文件到群聊需要额外的 API 权限")
    print("请确认你的应用有以下权限：")
    print("  - 群机器人消息发送权限")
    print("  - 企业内部群消息发送权限")


if __name__ == "__main__":
    main()
