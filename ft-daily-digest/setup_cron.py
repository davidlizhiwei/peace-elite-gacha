#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置 FT 每日摘要定时任务
每天早晨 8:00 自动执行
"""

import os
import sys
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FT_DIGEST_SCRIPT = os.path.join(SCRIPT_DIR, "ft_digest.py")


def get_python_path():
    """获取 Python 解释器路径"""
    return sys.executable


def get_cron_job():
    """获取 cron 任务字符串"""
    python_path = get_python_path()
    # 每天 8:00 执行
    return f"0 8 * * * cd {SCRIPT_DIR} && {python_path} {FT_DIGEST_SCRIPT} >> {SCRIPT_DIR}/cron.log 2>&1"


def install_cron():
    """安装定时任务"""
    cron_job = get_cron_job()

    print("正在设置定时任务...")
    print(f"任务内容：{cron_job}")

    # 获取当前 cron
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""
    except Exception as e:
        print(f"获取当前 cron 失败：{e}")
        current_cron = ""

    # 检查是否已存在
    if FT_DIGEST_SCRIPT in current_cron:
        print("✓ 定时任务已存在")
        return

    # 添加新任务
    new_cron = current_cron.rstrip() + "\n" + cron_job if current_cron else cron_job

    # 写入 cron
    try:
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        print("✓ 定时任务设置成功")
        print("\n执行时间：每天早晨 8:00")
        print(f"日志文件：{SCRIPT_DIR}/cron.log")
        return True
    except Exception as e:
        print(f"设置 cron 失败：{e}")
        print("\n请手动执行以下命令：")
        print(f'echo "{cron_job}" | crontab -')
        return False


def remove_cron():
    """删除定时任务"""
    print("正在删除定时任务...")

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        current_cron = result.stdout if result.returncode == 0 else ""
    except Exception as e:
        print(f"获取当前 cron 失败：{e}")
        return False

    # 移除相关任务
    lines = current_cron.split("\n")
    new_lines = [line for line in lines if FT_DIGEST_SCRIPT not in line]
    new_cron = "\n".join(new_lines).strip()

    try:
        if new_cron:
            process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
            process.communicate(input=new_cron)
        else:
            subprocess.run(["crontab", "-r"], check=False)
        print("✓ 定时任务已删除")
        return True
    except Exception as e:
        print(f"删除 cron 失败：{e}")
        return False


def show_status():
    """显示当前状态"""
    print("=== FT 每日摘要定时任务状态 ===\n")

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0 and FT_DIGEST_SCRIPT in result.stdout:
            print("✓ 定时任务已安装")
            print("\n当前任务列表：")
            for line in result.stdout.split("\n"):
                if FT_DIGEST_SCRIPT in line:
                    print(f"  {line}")
        else:
            print("✗ 定时任务未安装")
    except Exception as e:
        print(f"无法获取状态：{e}")

    print(f"\n脚本位置：{FT_DIGEST_SCRIPT}")
    print(f"Python 路径：{get_python_path()}")


def test_run():
    """测试运行"""
    print("=== 测试运行 FT 摘要生成器 ===\n")
    result = subprocess.run([get_python_path(), FT_DIGEST_SCRIPT])
    if result.returncode == 0:
        print("\n✓ 测试运行成功")
    else:
        print(f"\n✗ 测试运行失败，退出码：{result.returncode}")


def main():
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "--remove":
            remove_cron()
        elif action == "--status":
            show_status()
        elif action == "--test":
            test_run()
        elif action == "--help":
            print("用法：python3 setup_cron.py [选项]")
            print("\n选项:")
            print("  (无参数)    安装定时任务")
            print("  --remove    删除定时任务")
            print("  --status    显示当前状态")
            print("  --test      测试运行")
            print("  --help      显示帮助")
    else:
        install_cron()


if __name__ == "__main__":
    main()
