#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取机器人所在的群聊 conversation_id
"""

import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# 1. 获取 access token
print("1. 获取 access token...")
token_resp = requests.post(
    "https://api.dingtalk.com/v1.0/oauth2/accessToken",
    headers={"Content-Type": "application/json"},
    json={"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
)
token_data = token_resp.json()
access_token = token_data["accessToken"]
print(f"   ✓ Token: {access_token[:30]}...")

# 2. 获取机器人详情
print("\n2. 获取机器人信息...")
headers = {'x-acs-dingtalk-access-token': access_token}

# 尝试获取机器人的 chatId
robot_resp = requests.get(
    "https://api.dingtalk.com/v2/robot/contact/chat/get",
    headers=headers,
    json={"robotCode": "dingdwlipjehprtrzc6s"}
)
print(f"   机器人聊天信息：{robot_resp.json()}")

# 3. 尝试获取机器人参与的会话
print("\n3. 获取机器人会话列表...")
chatlist_resp = requests.get(
    "https://api.dingtalk.com/v1.0/robot/chat/list",
    headers=headers,
    params={'cursor': 0, 'size': 20}
)
chatlist_data = chatlist_resp.json()
print(f"   会话列表：{json.dumps(chatlist_data, ensure_ascii=False)}")

# 4. 尝试旧版 API
print("\n4. 尝试旧版 API 获取 token...")
old_token_resp = requests.get(
    "https://oapi.dingtalk.com/gettoken",
    params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET}
)
old_token = old_token_resp.json()["access_token"]
print(f"   ✓ 旧版 Token: {old_token[:30]}...")

# 获取机器人基本信息
print("\n5. 获取机器人基本信息...")
robot_info_resp = requests.get(
    f"https://oapi.dingtalk.com/robot/get?access_token={old_token}"
)
print(f"   机器人信息：{robot_info_resp.json()}")
