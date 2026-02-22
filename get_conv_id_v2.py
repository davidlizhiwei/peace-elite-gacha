#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取机器人所在群聊的 conversation_id
使用正确的 API
"""

import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# 1. 获取 access token
print("1. 获取 access token (v1.0)...")
token_resp = requests.post(
    "https://api.dingtalk.com/v1.0/oauth2/accessToken",
    headers={"Content-Type": "application/json"},
    json={"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
)
token_data = token_resp.json()
access_token = token_data["accessToken"]
print(f"   ✓ Token: {access_token[:30]}...")

# 2. 获取机器人详情
print("\n2. 获取机器人详情...")
headers = {'x-acs-dingtalk-access-token': access_token}

# 尝试不同的 API 端点
endpoints = [
    "https://api.dingtalk.com/v1.0/robots",
    "https://api.dingtalk.com/v1.0/robot/list",
    "https://api.dingtalk.com/v1.0/robot/contact",
]

for endpoint in endpoints:
    try:
        resp = requests.get(endpoint, headers=headers)
        print(f"   {endpoint}: {resp.json()}")
    except Exception as e:
        print(f"   {endpoint}: 错误 - {e}")

# 3. 获取群聊列表
print("\n3. 获取群聊列表...")
chat_endpoints = [
    ("https://oapi.dingtalk.com/chat/list", "GET"),
    ("https://api.dingtalk.com/v1.0/chat/top", "GET"),
    ("https://api.dingtalk.com/v1.0/chat/list", "GET"),
]

for endpoint, method in chat_endpoints:
    try:
        if "oapi" in endpoint:
            resp = requests.get(endpoint, params={"access_token": access_token})
        else:
            resp = requests.get(endpoint, headers=headers)
        print(f"   {endpoint}: {resp.json()}")
    except Exception as e:
        print(f"   {endpoint}: 错误 - {e}")

# 4. 使用 webhook 发送测试消息，看能否获取群信息
print("\n4. 使用 webhook 发送测试消息...")
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

payload = {
    "msgtype": "text",
    "text": {"content": "测试消息 - 获取群信息"}
}
resp = requests.post(WEBHOOK_URL, json=payload)
print(f"   Webhook 响应：{resp.json()}")

# 查看响应头
print(f"   响应头：{dict(resp.headers)}")
