#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉机器人文件发送工具
支持通过钉钉 API 上传并发送文件到群聊
"""

import os
import time
import requests
import json
from typing import Optional, Dict


class DingTalkFileSender:
    """钉钉文件发送器"""

    # API 端点
    TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
    UPLOAD_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/upload"
    SEND_URL = "https://api.dingtalk.com/v1.0/robot/messageFiles/send"

    def __init__(self, client_id: str, client_secret: str):
        """
        初始化钉钉文件发送器

        Args:
            client_id: 钉钉应用的 client_id (AppKey)
            client_secret: 钉钉应用的 client_secret (AppSecret)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token: Optional[str] = None
        self._token_expire_time: float = 0

    def _get_access_token(self) -> str:
        """获取 access token（带缓存）"""
        # 检查 token 是否有效（提前 5 分钟过期）
        if self._access_token and time.time() < self._token_expire_time - 300:
            return self._access_token

        # 请求新的 access token
        headers = {"Content-Type": "application/json"}
        payload = {
            "appKey": self.client_id,
            "appSecret": self.client_secret
        }

        response = requests.post(self.TOKEN_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        if "accessToken" not in result:
            raise Exception(f"获取 access token 失败：{result}")

        self._access_token = result["accessToken"]
        # token 有效期（秒），提前 5 分钟过期
        expire_in = result.get("expireIn", 7200)
        self._token_expire_time = time.time() + expire_in

        print(f"✓ 已获取 access token（有效期 {expire_in} 秒）")
        return self._access_token

    def upload_file(self, file_path: str) -> Dict:
        """
        上传文件到钉钉

        Args:
            file_path: 本地文件路径

        Returns:
            包含 mediaId 和 fileName 的字典
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        # 检查文件大小（最大 20MB）
        file_size = os.path.getsize(file_path)
        if file_size > 20 * 1024 * 1024:
            raise ValueError(f"文件大小超过限制（20MB）：{file_size / 1024 / 1024:.2f}MB")

        access_token = self._get_access_token()

        # 准备文件
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            headers = {
                'x-acs-dingtalk-access-token': access_token
            }

            print(f"↑ 正在上传文件：{os.path.basename(file_path)} ...")
            response = requests.post(
                self.UPLOAD_URL,
                headers=headers,
                files=files
            )

        response.raise_for_status()
        result = response.json()

        if "mediaId" not in result:
            raise Exception(f"文件上传失败：{result}")

        print(f"✓ 文件上传成功，mediaId: {result['mediaId']}")
        return result

    def send_file(
        self,
        robot_code: str,
        conversation_id: str,
        media_id: str,
        file_name: str
    ) -> Dict:
        """
        发送文件消息到群聊

        Args:
            robot_code: 机器人 code
            conversation_id: 群聊会话 ID
            media_id: 文件 media_id（通过 upload_file 获取）
            file_name: 文件名

        Returns:
            API 响应结果
        """
        access_token = self._get_access_token()

        headers = {
            'x-acs-dingtalk-access-token': access_token,
            'Content-Type': 'application/json'
        }

        payload = {
            "robotCode": robot_code,
            "msgKey": "sampleFile",
            "msgParam": {
                "mediaId": media_id,
                "fileName": file_name
            },
            "conversationId": conversation_id
        }

        print(f"→ 正在发送文件到群聊：{conversation_id} ...")
        response = requests.post(
            self.SEND_URL,
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"发送消息失败：{result}")

        print(f"✓ 文件发送成功！")
        return result

    def send_file_to_group(
        self,
        robot_code: str,
        conversation_id: str,
        file_path: str
    ) -> Dict:
        """
        一站式发送文件到群聊（上传 + 发送）

        Args:
            robot_code: 机器人 code
            conversation_id: 群聊会话 ID
            file_path: 本地文件路径

        Returns:
            API 响应结果
        """
        # 上传文件
        upload_result = self.upload_file(file_path)

        # 发送文件
        send_result = self.send_file(
            robot_code=robot_code,
            conversation_id=conversation_id,
            media_id=upload_result["mediaId"],
            file_name=upload_result["fileName"]
        )

        return send_result


def main():
    """示例用法"""
    # 配置信息（建议从环境变量读取）
    CLIENT_ID = os.getenv("DINGTALK_CLIENT_ID", "your_client_id")
    CLIENT_SECRET = os.getenv("DINGTALK_CLIENT_SECRET", "your_client_secret")
    ROBOT_CODE = os.getenv("DINGTALK_ROBOT_CODE", "your_robot_code")
    CONVERSATION_ID = os.getenv("DINGTALK_CONVERSATION_ID", "your_conversation_id")

    # 创建发送器
    sender = DingTalkFileSender(CLIENT_ID, CLIENT_SECRET)

    # 示例 1：一站式发送文件
    file_path = "test.pdf"  # 替换为你的文件路径
    if os.path.exists(file_path):
        try:
            result = sender.send_file_to_group(
                robot_code=ROBOT_CODE,
                conversation_id=CONVERSATION_ID,
                file_path=file_path
            )
            print(f"发送成功：{json.dumps(result, ensure_ascii=False)}")
        except Exception as e:
            print(f"发送失败：{e}")

    # 示例 2：分步操作（可复用 media_id）
    # 1. 上传文件
    # upload_result = sender.upload_file(file_path)
    # media_id = upload_result["mediaId"]
    #
    # 2. 发送文件（media_id 3 天内有效）
    # sender.send_file(
    #     robot_code=ROBOT_CODE,
    #     conversation_id=CONVERSATION_ID,
    #     media_id=media_id,
    #     file_name=upload_result["fileName"]
    # )


if __name__ == "__main__":
    main()
