#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本：发送文件到钉钉群
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dingtalk_file_sender import DingTalkFileSender


def main():
    # 配置（建议从环境变量读取）
    CLIENT_ID = os.getenv("DINGTALK_CLIENT_ID")
    CLIENT_SECRET = os.getenv("DINGTALK_CLIENT_SECRET")
    ROBOT_CODE = os.getenv("DINGTALK_ROBOT_CODE")
    CONVERSATION_ID = os.getenv("DINGTALK_CONVERSATION_ID")

    # 检查配置
    if not all([CLIENT_ID, CLIENT_SECRET, ROBOT_CODE, CONVERSATION_ID]):
        print("❌ 请配置以下环境变量：")
        print("  - DINGTALK_CLIENT_ID")
        print("  - DINGTALK_CLIENT_SECRET")
        print("  - DINGTALK_ROBOT_CODE")
        print("  - DINGTALK_CONVERSATION_ID")
        print("\n或者在脚本中直接设置这些值")
        sys.exit(1)

    # 要发送的文件
    file_path = sys.argv[1] if len(sys.argv) > 1 else "test.pdf"

    if not os.path.exists(file_path):
        print(f"❌ 文件不存在：{file_path}")
        sys.exit(1)

    # 创建发送器并发送文件
    sender = DingTalkFileSender(CLIENT_ID, CLIENT_SECRET)

    try:
        print(f"📤 准备发送文件：{file_path}")
        print(f"📍 目标群聊：{CONVERSATION_ID}")
        print()

        result = sender.send_file_to_group(
            robot_code=ROBOT_CODE,
            conversation_id=CONVERSATION_ID,
            file_path=file_path
        )

        print()
        print("✅ 发送成功！")
        print(f"响应：{json.dumps(result, ensure_ascii=False)}")

    except Exception as e:
        print()
        print(f"❌ 发送失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    import json
    main()
