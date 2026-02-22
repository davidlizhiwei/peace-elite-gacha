#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取机器人所在群聊的 conversation_id"""

import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"
ROBOT_CODE = "robot35511618523509219"

# 1. 先获取 access token
print("1. 获取 access token...")
token_resp = requests.post(
    "https://api.dingtalk.com/v1.0/oauth2/accessToken",
    headers={"Content-Type": "application/json"},
    json={"appKey": CLIENT_ID, "appSecret": CLIENT_SECRET}
)
token_data = token_resp.json()
access_token = token_data["accessToken"]
print(f"   ✓ Token: {access_token[:20]}...")

# 2. 获取机器人详情
print("\n2. 获取机器人详情...")
headers = {'x-acs-dingtalk-access-token': access_token}
robot_resp = requests.get(
    f"https://api.dingtalk.com/v1.0/robots/{ROBOT_CODE}",
    headers=headers
)
print(f"   机器人信息：{robot_resp.json()}")

# 3. 尝试获取机器人参与的会话
print("\n3. 尝试获取机器人会话列表...")
headers = {'x-acs-dingtalk-access-token': access_token}
chatlist_resp = requests.get(
    "https://api.dingtalk.com/v1.0/chat/list",
    headers=headers,
    params={'cursor': 0, 'size': 20}
)
print(f"   会话列表：{chatlist_resp.json()}")

# 4. 尝试使用 webhook 发送测试消息，看看能否获取 conversationId
print("\n4. 尝试通过 webhook 发送测试消息...")

def generate_sign(secret: str) -> str:
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = f'{timestamp}\n{secret}'
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"&timestamp={timestamp}&sign={sign}"

# 发送一个测试消息
test_payload = {
    "msgtype": "text",
    "text": {"content": "测试消息 - 获取会话信息"}
}
result = requests.post(WEBHOOK_URL, json=test_payload)
print(f"   测试结果：{result.json()}")
