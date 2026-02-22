#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速获取会话 ID"""

import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# 获取 token
token_resp = requests.post(
    "https://api.dingtalk.com/v1.0/oauth2/accessToken",
    headers={"Content-Type": "application/json"},
    json={"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
)
token = token_resp.json()["accessToken"]
print(f"Token: {token[:20]}...")

# 获取置顶会话列表
headers = {
    'x-acs-dingtalk-access-token': token,
    'Content-Type': 'application/json'
}

resp = requests.get(
    "https://api.dingtalk.com/v1.0/chat/top",
    headers=headers,
    params={'limit': 20}
)

result = resp.json()
print("\n=== 置顶群聊列表 ===\n")

for chat in result.get("chatList", []):
    print(f"群名称：{chat.get('title', 'N/A')}")
    print(f"群 ID: {chat.get('chatId', 'N/A')}")
    print(f"会话 ID: {chat.get('conversationId', 'N/A')}")
    print(f"群主：{chat.get('ownerNick', 'N/A')}")
    print("-" * 50)
