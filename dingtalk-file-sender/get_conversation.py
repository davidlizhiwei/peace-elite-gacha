#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取钉钉群聊 conversation_id 工具
"""

import requests
import json

# 配置
CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

# API 端点
TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"


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


def get_chat_list_v1(access_token):
    """获取应用可见的群聊列表（使用 v1 API）"""
    url = "https://oapi.dingtalk.com/chat/list"

    params = {
        'access_token': access_token,
        'offset': 0,
        'size': 20
    }

    response = requests.get(url, params=params)
    result = response.json()

    if result.get("errcode") == 0:
        chats = result.get("chat_list", [])
        return chats
    else:
        print(f"获取失败：{result}")
        return []


def get_user_chatids(access_token):
    """获取用户参与的群聊"""
    url = "https://oapi.dingtalk.com/user/get_chatid"

    # 需要先获取用户 userid
    params = {'access_token': access_token}

    # 这个接口需要 userid，比较复杂
    return []


def main():
    print("=== 获取钉钉群聊 conversation_id ===\n")

    try:
        access_token = get_access_token()
    except Exception as e:
        print(f"获取 token 失败：{e}")
        return

    # 方法 1：获取应用可见的群聊
    print("方法 1：获取应用已添加的群聊列表")
    print("-" * 50)
    chats = get_chat_list_v1(access_token)

    if chats:
        print(f"找到 {len(chats)} 个群聊：\n")
        for i, chat in enumerate(chats, 1):
            print(f"{i}. 群名称：{chat.get('name', 'N/A')}")
            print(f"   群 ID (chatid): {chat.get('chatid', 'N/A')}")
            print(f"   会话 ID (conversation_id): {chat.get('conversation_id', 'N/A')}")
            print(f"   群主：{chat.get('owner', 'N/A')}")
            print()
    else:
        print("未找到群聊")

    print("\n" + "=" * 50)
    print("方法 2：从钉钉后台查看")
    print("=" * 50)
    print("""
1. 登录钉钉开发者后台：
   https://open-dev.dingtalk.com/

2. 进入你的应用 → 机器人管理

3. 在"机器人"页面，可以看到已添加的群聊

4. 点击群聊名称，可以看到 conversation_id

或者：
- 在钉钉群聊中，机器人被添加时，webhook URL 里可能包含相关信息
- webhook 格式：https://oapi.dingtalk.com/robot/send?access_token=XXX
    """)

    print("\n" + "=" * 50)
    print("方法 3：从群聊信息获取")
    print("=" * 50)
    print("""
如果你知道群 ID (chatid)，可以用以下接口获取 conversation_id：

GET https://oapi.dingtalk.com/chat/get?access_token=TOKEN&chatid=CHAT_ID

需要我帮你尝试这个方法吗？请提供群 ID。
    """)


if __name__ == "__main__":
    main()
