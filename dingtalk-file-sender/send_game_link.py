#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送太空射击游戏链接到钉钉群
"""

import requests
import json

# 配置
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"


def send_link_by_webhook(title, text, message_url, pic_url=""):
    """发送链接卡片消息"""
    payload = {
        "msgtype": "link",
        "link": {
            "title": title,
            "text": text,
            "messageUrl": message_url,
            "picUrl": pic_url
        }
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    return response.json()


def main():
    print("正在发送太空射击游戏链接到钉钉...")

    # 发送链接消息
    result = send_link_by_webhook(
        title="🚀 太空射击游戏 - 专为 12 岁男孩设计",
        text="这是一款有趣的手机端太空射击游戏！触摸屏幕控制飞船，自动射击消灭敌人。适合 12 岁孩子，安全无暴力，快来挑战高分吧！",
        message_url="https://davidlizhiwei.github.io/memory-game/",
        pic_url="https://davidlizhiwei.github.io/memory-game/"
    )

    if result.get("errcode") == 0:
        print("✓ 游戏链接发送成功！")
        print(f"游戏链接：https://davidlizhiwei.github.io/memory-game/")
    else:
        print(f"✗ 发送失败：{result}")


if __name__ == "__main__":
    main()
