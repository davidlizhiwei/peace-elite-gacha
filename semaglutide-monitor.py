#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
司美格鲁肽 (Semaglutide) 实验 Readout 监控脚本
定期检查最新临床试验结果并发送钉钉通知
"""

import requests
import json
import hashlib
import os
from datetime import datetime

# 配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"
DATA_FILE = os.path.join(os.path.dirname(__file__), "semaglutide-cache.json")
SEARCH_QUERIES = [
    "司美格鲁肽 semaglutide 临床试验 readout 2026",
    "semaglutide clinical trial results 2026",
    "诺和诺德 司美格鲁肽 新药 获批 2026",
    "Wegovy Ozempic FDA approval 2026",
]

# 搜索脚本路径
SKILLS_ROOT = os.environ.get("SKILLS_ROOT", "/Users/davidli/Library/Application Support/LobsterAI/SKILLs")
SEARCH_SCRIPT = os.path.join(SKILLS_ROOT, "web-search/scripts/search-hybrid.sh")


def load_cache():
    """加载已通知的记录"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"notified_urls": [], "last_check": None}


def save_cache(data):
    """保存已通知的记录"""
    data["last_check"] = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_search(query):
    """执行搜索"""
    import subprocess
    try:
        result = subprocess.run(
            ["bash", SEARCH_SCRIPT, query, "10"],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout
    except Exception as e:
        print(f"搜索失败：{e}")
        return ""


def parse_search_results(output):
    """解析搜索结果"""
    results = []
    lines = output.split("\n")

    current_item = {}
    for line in lines:
        if line.startswith("## "):
            if current_item.get("title"):
                results.append(current_item)
            current_item = {"title": line[3:].strip()}
        elif line.startswith("**URL:**"):
            url = line.replace("**URL:**", "").strip()
            # 提取纯 URL
            if "[" in url and "]" in url:
                url = url.split("](")[-1].replace(")", "")
            current_item["url"] = url
        elif line.startswith("**Date:**"):
            current_item["date"] = line.replace("**Date:**", "").strip()

    if current_item.get("title"):
        results.append(current_item)

    return results


def send_dingtalk_notification(new_items):
    """发送钉钉通知"""
    if not new_items:
        return False

    # 构建消息内容
    text = "## 💊 司美格鲁肽实验 Readout 更新\n\n"
    text += f"发现 **{len(new_items)}** 条新进展：\n\n"

    for i, item in enumerate(new_items[:5], 1):  # 最多显示 5 条
        text += f"{i}. **{item.get('title', '无标题')}**\n"
        text += f"   🔗 [查看详情]({item.get('url', '#')})\n"
        if item.get('date'):
            text += f"   📅 {item['date']}\n\n"

    if len(new_items) > 5:
        text += f"\n... 还有 {len(new_items) - 5} 条，请访问完整报告\n"

    text += "\n---\n_监控时间：" + datetime.now().strftime("%Y-%m-%d %H:%M") + "_"

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "司美格鲁肽实验 Readout 更新",
            "text": text
        }
    }

    try:
        response = requests.post(
            DINGTALK_WEBHOOK,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        result = response.json()
        if result.get("errcode") == 0:
            print(f"✓ 钉钉通知已发送 ({len(new_items)} 条)")
            return True
        else:
            print(f"✗ 钉钉通知失败：{result}")
            return False
    except Exception as e:
        print(f"✗ 发送通知异常：{e}")
        return False


def check_updates():
    """检查更新"""
    print(f"[{datetime.now().isoformat()}] 开始检查司美格鲁肽实验 readout...")

    cache = load_cache()
    notified_urls = set(cache.get("notified_urls", []))
    new_items = []

    for query in SEARCH_QUERIES:
        print(f"  搜索：{query}")
        output = run_search(query)
        results = parse_search_results(output)

        for item in results:
            url = item.get("url", "")
            if url and url not in notified_urls:
                # 检查是否是新的（URL 不在缓存中）
                # 且日期是近期的（2026 年）
                date_str = item.get("date", "")
                if "2026" in date_str or "hours ago" in date_str.lower() or "days ago" in date_str.lower():
                    item["query"] = query
                    new_items.append(item)
                    notified_urls.add(url)

    # 去重（按 URL）
    seen_urls = set()
    unique_new_items = []
    for item in new_items:
        if item.get("url") not in seen_urls:
            seen_urls.add(item.get("url"))
            unique_new_items.append(item)

    print(f"  发现 {len(unique_new_items)} 条新内容")

    if unique_new_items:
        send_dingtalk_notification(unique_new_items)

        # 更新缓存
        cache["notified_urls"] = list(notified_urls)
        save_cache(cache)

    return len(unique_new_items)


if __name__ == "__main__":
    count = check_updates()
    print(f"完成！新增：{count} 条")
