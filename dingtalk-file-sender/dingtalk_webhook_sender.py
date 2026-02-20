#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉 Webhook 机器人文件发送工具
注意：Webhook 方式不支持直接发送文件，需要通过文件链接方式
适用于简单的通知场景
"""

import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
from typing import Optional


class DingTalkWebhookSender:
    """钉钉 Webhook 消息发送器"""

    def __init__(self, webhook_url: str, secret: Optional[str] = None):
        """
        初始化 Webhook 发送器

        Args:
            webhook_url: 机器人 Webhook URL
            secret: 加签密钥（如果启用了安全设置）
        """
        self.webhook_url = webhook_url
        self.secret = secret

    def _generate_sign(self) -> str:
        """生成加签参数"""
        if not self.secret:
            return ""

        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')

        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256
        ).digest()

        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return f"&timestamp={timestamp}&sign={sign}"

    def send_text(self, content: str, mentioned_all: bool = False) -> dict:
        """
        发送文本消息

        Args:
            content: 消息内容
            mentioned_all: 是否@所有人

        Returns:
            API 响应
        """
        url = self.webhook_url
        if self.secret:
            url += self._generate_sign()

        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "isAtAll": mentioned_all
            }
        }

        response = requests.post(url, json=payload)
        return response.json()

    def send_markdown(self, title: str, text: str) -> dict:
        """
        发送 Markdown 消息

        Args:
            title: 消息标题
            text: Markdown 格式内容

        Returns:
            API 响应
        """
        url = self.webhook_url
        if self.secret:
            url += self._generate_sign()

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }

        response = requests.post(url, json=payload)
        return response.json()

    def send_file_link(
        self,
        title: str,
        text: str,
        message_url: str,
        image_url: str
    ) -> dict:
        """
        发送文件链接卡片消息
        （通过链接方式分享文件，文件需托管在可访问的 URL）

        Args:
            title: 标题
            text: 描述
            message_url: 文件下载链接
            image_url: 封面图片 URL

        Returns:
            API 响应
        """
        url = self.webhook_url
        if self.secret:
            url += self._generate_sign()

        payload = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": message_url,
                "picUrl": image_url
            }
        }

        response = requests.post(url, json=payload)
        return response.json()


def main():
    """示例用法"""
    # 从环境变量获取配置
    WEBHOOK_URL = os.getenv("DINGTALK_WEBHOOK_URL", "")
    WEBHOOK_SECRET = os.getenv("DINGTALK_WEBHOOK_SECRET", "")

    sender = DingTalkWebhookSender(WEBHOOK_URL, WEBHOOK_SECRET)

    # 发送文本消息
    result = sender.send_text("你好，这是一条测试消息")
    print(f"发送结果：{result}")

    # 发送 Markdown 消息
    markdown_text = """## 文件上传通知
- 文件名：report.pdf
- 大小：2.5MB
- 时间：2026-02-20

[点击下载文件](https://example.com/files/report.pdf)"""

    result = sender.send_markdown("文件通知", markdown_text)
    print(f"发送结果：{result}")


if __name__ == "__main__":
    main()
