#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 LobsterAI 钉钉配置脚本
"""

import sqlite3
import json
from pathlib import Path

# 数据库路径
DB_PATH = Path.home() / "Library/Application Support/LobsterAI/lobsterai.sqlite"

def update_dingtalk_config():
    """更新钉钉配置"""

    if not DB_PATH.exists():
        print(f"数据库不存在：{DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 读取当前配置
    cursor.execute("SELECT key, value FROM im_config WHERE key='dingtalk'")
    row = cursor.fetchone()

    if not row:
        print("未找到钉钉配置")
        return

    config = json.loads(row[1])
    print("当前配置:")
    print(json.dumps(config, indent=2, ensure_ascii=False))

    # 添加回调配置
    config['callbackUrl'] = 'http://localhost:8888/dingtalk/callback'
    config['port'] = 8888
    config['host'] = 'localhost'
    config['token'] = 'LOBSTER_AI_TOKEN'  # 需要与钉钉后台一致

    # 更新配置
    new_value = json.dumps(config, ensure_ascii=False)
    updated_at = int(json.dumps(1771569999999))

    cursor.execute(
        "UPDATE im_config SET value = ?, updated_at = ? WHERE key = ?",
        (new_value, 1771570000000, 'dingtalk')
    )

    conn.commit()

    # 验证更新
    cursor.execute("SELECT value FROM im_config WHERE key='dingtalk'")
    new_row = cursor.fetchone()
    print("\n更新后配置:")
    print(json.dumps(json.loads(new_row[0]), indent=2, ensure_ascii=False))

    conn.close()
    print("\n配置已更新！请重启 LobsterAI 应用以生效。")

if __name__ == '__main__':
    update_dingtalk_config()
