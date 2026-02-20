#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取钉钉群聊 conversationId 的工具
"""

import os
import requests
import json
from typing import List, Dict


class DingTalkConversationManager:
    """钉钉会话管理器"""

    TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    CHAT_LIST_URL = "https://api.dingtalk.com/v1.0/chat/top"
    CHAT_GET_URL = "https://api.dingtalk.com/v1.0/chat"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token: str = ""

    def _get_access_token(self) -> str:
        """获取 access token"""
        if self._access_token:
            return self._access_token

        headers = {"Content-Type": "application/json"}
        payload = {
            "appKey": self.client_id,
            "appSecret": self.client_secret
        }

        response = requests.post(self.TOKEN_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        self._access_token = result["accessToken"]
        return self._access_token

    def list_top_chats(self, limit: int = 20) -> List[Dict]:
        """
        获取置顶会话列表

        Args:
            limit: 返回数量限制

        Returns:
            会话列表
        """
        access_token = self._get_access_token()

        headers = {
            'x-acs-dingtalk-access-token': access_token,
            'Content-Type': 'application/json'
        }

        params = {'limit': limit}

        response = requests.get(
            self.CHAT_LIST_URL,
            headers=headers,
            params=params
        )
        response.raise_for_status()

        result = response.json()
        return result.get("chatList", [])

    def get_chat_info(self, chat_id: str) -> Dict:
        """
        获取群聊详情

        Args:
            chat_id: 群 ID

        Returns:
            群聊信息
        """
        access_token = self._get_access_token()

        headers = {
            'x-acs-dingtalk-access-token': access_token,
            'Content-Type': 'application/json'
        }

        response = requests.get(
            f"{self.CHAT_GET_URL}/{chat_id}",
            headers=headers
        )
        response.raise_for_status()

        return response.json()


def main():
    """示例：获取群聊 conversationId"""
    CLIENT_ID = os.getenv("DINGTALK_CLIENT_ID", "your_client_id")
    CLIENT_SECRET = os.getenv("DINGTALK_CLIENT_SECRET", "your_client_secret")

    manager = DingTalkConversationManager(CLIENT_ID, CLIENT_SECRET)

    # 获取置顶群聊列表
    print("获取置顶群聊列表...")
    chats = manager.list_top_chats()

    for chat in chats:
        print(f"\n群名称：{chat.get('title', 'N/A')}")
        print(f"群 ID: {chat.get('chatId', 'N/A')}")
        print(f"会话 ID: {chat.get('conversationId', 'N/A')}")
        print(f"群主：{chat.get('ownerNick', 'N/A')}")
        print("-" * 50)

    # 注意：conversationId 通常格式为 "cid-xxx"
    # 发送文件时需要使用完整的 conversationId


if __name__ == "__main__":
    main()
