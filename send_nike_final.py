#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送 Nike 跑鞋图片到钉钉群
使用之前成功的 dingtalk_file_sender 模块
"""

import os
import sys
import json

# 添加路径
sys.path.insert(0, "/Users/davidli/lobsterai/project/dingtalk-file-sender")

from dingtalk_file_sender import DingTalkFileSender

# 配置
CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"
ROBOT_CODE = "dingdwlipjehprtrzc6s"

# 图片路径（使用压缩后的）
IMAGE_PATH = "/Users/davidli/lobsterai/project/nike_shoe_small.png"

# 可能的 conversation_id 列表（需要尝试）
POSSIBLE_CONVERSATION_IDS = [
    "cid1AQDi~eF8CQoMCogBjCQCoEoEoEoE",  # 之前用过的
]


def try_send(conversation_id):
    """尝试发送到指定会话"""
    sender = DingTalkFileSender(CLIENT_ID, CLIENT_SECRET)

    try:
        print(f"📤 准备发送图片：{os.path.basename(IMAGE_PATH)}")
        print(f"📍 目标会话：{conversation_id}")
        print()

        result = sender.send_file_to_group(
            robot_code=ROBOT_CODE,
            conversation_id=conversation_id,
            file_path=IMAGE_PATH
        )

        print()
        print("✅ 发送成功！")
        print(f"响应：{json.dumps(result, ensure_ascii=False)}")
        return True

    except Exception as e:
        print()
        print(f"❌ 发送失败：{e}")
        return False


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print("=== 发送 Nike 跑鞋图片到钉钉 ===\n")

    # 尝试每个可能的 conversation_id
    for conv_id in POSSIBLE_CONVERSATION_IDS:
        print(f"\n尝试会话：{conv_id}")
        print("=" * 50)
        if try_send(conv_id):
            return

    # 如果都失败了，尝试获取新的 conversation_id
    print("\n所有已知会话 ID 都失败了，尝试获取新的...")

    # 使用 webhook 发送一个测试消息，看看能否获取信息
    import requests
    import time
    import hmac
    import hashlib
    import base64
    import urllib.parse

    WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"

    def generate_sign(secret: str) -> str:
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return f"&timestamp={timestamp}&sign={sign}"

    # 发送测试消息
    payload = {
        "msgtype": "text",
        "text": {"content": "测试消息"}
    }
    resp = requests.post(WEBHOOK_URL, json=payload)
    print(f"Webhook 测试：{resp.json()}")


if __name__ == "__main__":
    main()
