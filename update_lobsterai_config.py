#!/usr/bin/env python3
"""
更新 LobsterAI 配置，添加 custom1 和 custom2 自定义 API 端点
"""

import sqlite3
import json
import sys
import os

DB_PATH = os.path.expanduser("~/Library/Application Support/LobsterAI/lobsterai.sqlite")

def update_config():
    print(f"数据库路径：{DB_PATH}")

    if not os.path.exists(DB_PATH):
        print(f"错误：数据库文件不存在")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 获取当前配置
    cursor.execute("SELECT value FROM kv WHERE key = 'app_config'")
    row = cursor.fetchone()

    if not row:
        print("错误：未找到 app_config 配置")
        conn.close()
        return False

    config = json.loads(row[0])

    print("当前 providers:", list(config["providers"].keys()))

    # 添加 custom1 配置
    config["providers"]["custom1"] = {
        "enabled": False,
        "apiKey": "",
        "baseUrl": "https://api.custom1.com/v1",
        "apiFormat": "openai",
        "models": [
            {"id": "custom1-model-1", "name": "Custom1 Model 1", "supportsImage": True},
            {"id": "custom1-model-2", "name": "Custom1 Model 2", "supportsImage": False}
        ]
    }
    print("已添加 custom1")

    # 添加 custom2 配置
    config["providers"]["custom2"] = {
        "enabled": False,
        "apiKey": "",
        "baseUrl": "https://api.custom2.com/v1",
        "apiFormat": "openai",
        "models": [
            {"id": "custom2-model-1", "name": "Custom2 Model 1", "supportsImage": True},
            {"id": "custom2-model-2", "name": "Custom2 Model 2", "supportsImage": False}
        ]
    }
    print("已添加 custom2")

    # 更新配置到数据库
    new_value = json.dumps(config, ensure_ascii=False)

    cursor.execute("UPDATE kv SET value = ? WHERE key = 'app_config'", (new_value,))
    conn.commit()
    print(f"已更新 {cursor.rowcount} 行")

    # 验证更新
    cursor.execute("SELECT value FROM kv WHERE key = 'app_config'")
    verify_row = cursor.fetchone()
    verify_config = json.loads(verify_row[0])

    print("更新后 providers:", list(verify_config["providers"].keys()))

    conn.close()

    if "custom1" in verify_config["providers"] and "custom2" in verify_config["providers"]:
        print("\n✅ 配置更新成功！")
        print("\n已添加以下配置:")
        print("- custom1: 自定义 API 端点 1")
        print("- custom2: 自定义 API 端点 2")
        print("\n⚠️ 注意：您还需要修改 LobsterAI 应用的界面代码才能在设置页面看到这两个新选项")
        return True
    else:
        print("\n❌ 配置更新失败")
        return False

if __name__ == "__main__":
    success = update_config()
    sys.exit(0 if success else 1)
