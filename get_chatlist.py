#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用旧版 API 获取群聊列表"""

import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# 1. 获取 access token (旧版)
print("1. 获取 access token...")
token_resp = requests.get(
    "https://oapi.dingtalk.com/gettoken",
    params={
        "appkey": CLIENT_ID,
        "appsecret": CLIENT_SECRET
    }
)
token_data = token_resp.json()
print(f"   Token 响应：{token_data}")

if token_data.get("errcode") != 0:
    print("   ❌ 获取 token 失败")
    exit(1)

access_token = token_data["access_token"]
print(f"   ✓ Token: {access_token[:30]}...")

# 2. 获取应用管理员信息
print("\n2. 获取管理员信息...")
user_resp = requests.get(
    f"https://oapi.dingtalk.com/user/get",
    params={"access_token": access_token, "userid": "manager"}
)
print(f"   管理员：{user_resp.json()}")

# 3. 获取群聊列表 (旧版 API)
print("\n3. 获取群聊列表...")
chatlist_resp = requests.post(
    "https://oapi.dingtalk.com/chat/list",
    headers={"Content-Type": "application/json"},
    params={"access_token": access_token},
    json={"cursor": 0, "size": 20}
)
chatlist_data = chatlist_resp.json()
print(f"   群聊列表响应：{json.dumps(chatlist_data, ensure_ascii=False)}")

# 4. 打印群聊信息
if chatlist_data.get("errcode") == 0:
    chat_list = chatlist_data.get("chat_list", [])
    print(f"\n=== 找到 {len(chat_list)} 个群聊 ===\n")
    for chat in chat_list:
        print(f"群名称：{chat.get('title', 'N/A')}")
        print(f"群 ID: {chat.get('chatid', 'N/A')}")
        print(f"群主：{chat.get('ownerNick', 'N/A')}")
        print(f"创建时间：{chat.get('create_time', 'N/A')}")
        print("-" * 50)
