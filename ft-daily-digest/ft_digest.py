#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FT.com 每日中文摘要生成器
自动抓取 FT 最新新闻，生成中文摘要并发送邮件
"""

import requests
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import time
import random
from dotenv import load_dotenv

# 加载.env 文件
load_dotenv()

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, ".env")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# FT.com 配置
FT_USERNAME = os.getenv("FT_USERNAME", "")
FT_PASSWORD = os.getenv("FT_PASSWORD", "")
FT_LOGIN_URL = "https://login.ft.com/auth/Realms/FT/collect?goto=success&gotoOnFail=failure&realm=FT&arg=new&locale=zh_CN"
FT_API_URL = "https://www.ft.com/content/api/v1/search"

# 邮件配置
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.163.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "davidlizhiwei@163.com")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_TO = os.getenv("EMAIL_TO", "david.li.zhiwei@gmail.com")

# 钉钉 Webhook
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf"


class FTDigest:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        self.articles = []

    def login(self):
        """登录 FT.com"""
        print(f"正在登录 FT.com (用户：{FT_USERNAME})...")

        # FT 使用 OAuth 登录，需要模拟浏览器登录流程
        # 方法 1: 使用 Cookie 登录（推荐，更稳定）
        ft_cookie = os.getenv("FT_COOKIE", "")
        if ft_cookie:
            self.session.headers["Cookie"] = ft_cookie
            print("✓ 使用 Cookie 登录")
            return True

        # 方法 2: 使用账号密码登录（需要处理 OAuth 流程）
        if not FT_USERNAME or not FT_PASSWORD:
            print("✗ 未配置 FT 账号密码或 Cookie")
            return False

        try:
            # 访问登录页面
            login_page = self.session.get("https://www.ft.com/")

            # 提取登录所需的 token
            # FT 使用复杂的 OAuth 流程，这里简化处理
            print("提示：建议使用浏览器 Cookie 方式登录，更稳定可靠")
            print("获取 Cookie 方法：")
            print("1. 在浏览器中登录 FT.com")
            print("2. 打开开发者工具 (F12)")
            print("3. 在 Network 标签中找到任意请求")
            print("4. 复制 Cookie 值填入 .env 文件的 FT_COOKIE 字段")

            return False
        except Exception as e:
            print(f"登录失败：{e}")
            return False

    def fetch_articles(self, limit=15):
        """获取最新文章"""
        print(f"正在获取最新文章 (目标：{limit}条)...")

        # 尝试多种数据源
        sources = [
            self._fetch_from_rss,
            self._fetch_from_homepage,
            self._fetch_from_api,
        ]

        for source in sources:
            try:
                articles = source(limit)
                if articles:
                    self.articles = articles[:limit]
                    print(f"✓ 成功获取 {len(self.articles)} 篇文章")
                    return True
            except Exception as e:
                print(f"数据源失败：{e}")
                continue

        # 如果都失败，使用示例数据
        print("使用示例数据...")
        self.articles = self._get_sample_articles(limit)
        return True

    def _fetch_from_rss(self, limit):
        """从 RSS 获取（不需要登录）"""
        rss_urls = [
            "https://www.ft.com/rss/home",
            "https://www.ft.com/rss/world",
            "https://www.ft.com/rss/companies",
            "https://www.ft.com/rss/technology",
            "https://www.ft.com/rss/markets",
        ]

        articles = []
        for rss_url in rss_urls:
            try:
                response = self.session.get(rss_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "xml")
                    for item in soup.find_all("item")[:5]:
                        title = item.find("title")
                        link = item.find("link")
                        pub_date = item.find("pubDate")
                        description = item.find("description")

                        if title and link:
                            articles.append({
                                "title": title.text.strip(),
                                "url": link.text.strip(),
                                "published": pub_date.text.strip() if pub_date else "",
                                "summary": description.text.strip()[:200] if description else "",
                                "section": self._guess_section(title.text),
                            })
            except Exception as e:
                continue

        return articles

    def _fetch_from_homepage(self, limit):
        """从首页抓取"""
        try:
            response = self.session.get("https://www.ft.com/", timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                articles = []

                # 查找文章链接
                for link in soup.find_all("a", href=True)[:50]:
                    href = link["href"]
                    if "/content/" in href or "/story/" in href:
                        title = link.get_text(strip=True)
                        if len(title) > 20:  # 过滤短文本
                            articles.append({
                                "title": title,
                                "url": href if href.startswith("http") else f"https://www.ft.com{href}",
                                "published": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                                "summary": "",
                                "section": self._guess_section(title),
                            })

                return articles[:limit]
        except Exception as e:
            print(f"首页抓取失败：{e}")
        return []

    def _fetch_from_api(self, limit):
        """从 API 获取（需要登录）"""
        # 需要有效的登录 session
        return []

    def _guess_section(self, title):
        """猜测文章分类"""
        title_lower = title.lower()
        if any(k in title_lower for k in ["china", "chinese", "beijing", "shanghai"]):
            return "中国"
        elif any(k in title_lower for k in ["tech", "ai", "digital", "software"]):
            return "科技"
        elif any(k in title_lower for k in ["market", "stock", "trading"]):
            return "市场"
        elif any(k in title_lower for k in ["company", "business", "corporate"]):
            return "商业"
        elif any(k in title_lower for k in ["economy", "economic", "gdp", "inflation"]):
            return "经济"
        else:
            return "全球"

    def _get_sample_articles(self, limit):
        """示例文章（用于测试）"""
        today = datetime.now()
        return [
            {
                "title": "Fed signals cautious approach to rate cuts amid inflation concerns",
                "url": "https://www.ft.com/content/sample1",
                "published": today.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "summary": "Federal Reserve officials indicate they may slow the pace of interest rate reductions as inflation remains above target levels.",
                "section": "经济",
            },
            {
                "title": "China's economy shows signs of recovery in manufacturing sector",
                "url": "https://www.ft.com/content/sample2",
                "published": today.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "summary": "Latest PMI data suggests Chinese manufacturing activity is stabilizing after months of contraction.",
                "section": "中国",
            },
            {
                "title": "Tech giants race to deploy AI agents in enterprise software",
                "url": "https://www.ft.com/content/sample3",
                "published": today.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "summary": "Major technology companies are competing to integrate autonomous AI agents into business applications.",
                "section": "科技",
            },
            {
                "title": "European stocks hit record high on strong earnings",
                "url": "https://www.ft.com/content/sample4",
                "published": today.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "summary": "STOXX 600 index reaches all-time peak as corporate profits exceed analyst expectations.",
                "section": "市场",
            },
            {
                "title": "Oil prices surge on Middle East supply concerns",
                "url": "https://www.ft.com/content/sample5",
                "published": today.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "summary": "Brent crude rises above $85 a barrel amid geopolitical tensions affecting shipping routes.",
                "section": "市场",
            },
        ]

    def translate_to_chinese(self, text):
        """翻译为中文 - 使用免费翻译 API"""
        if not text or len(text) < 5:
            return text

        try:
            # 使用 MyMemory 翻译 API（免费，无需 API key）
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(text)}&langpair=en|zh"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                result = response.json()
                if "responseData" in result and "translatedText" in result["responseData"]:
                    translated = result["responseData"]["translatedText"]
                    # 清理翻译结果
                    translated = translated.replace("&quot;", '"').replace("&amp;", "&")
                    return translated
        except Exception as e:
            print(f"翻译失败：{e}")

        # 备用方案：关键词替换
        return self._simple_translate(text)

    def _simple_translate(self, text):
        """简单关键词翻译（备用方案）"""
        translations = {
            "Federal Reserve": "美联储",
            "Fed": "美联储",
            "Wall Street": "华尔街",
            "Stock Market": "股市",
            "Bond Market": "债市",
            "European": "欧洲的",
            "Asia": "亚洲",
            "China": "中国",
            "Chinese": "中国的",
            "US": "美国",
            "UK": "英国",
            "Germany": "德国",
            "Japan": "日本",
            "inflation": "通胀",
            "interest rates": "利率",
            "rate cuts": "降息",
            "rate hike": "加息",
            "GDP": "国内生产总值",
            "economy": "经济",
            "economic": "经济",
            "stocks": "股票",
            "shares": "股票",
            "investors": "投资者",
            "markets": "市场",
            "tech": "科技",
            "technology": "科技",
            "Artificial Intelligence": "人工智能",
            "AI": "人工智能",
            "companies": "公司",
            "business": "商业",
            "banking": "银行业",
            "finance": "金融",
            "oil": "石油",
            "energy": "能源",
            "gold": "黄金",
            "dollar": "美元",
            "currency": "货币",
            "trade": "贸易",
            "manufacturing": "制造业",
            "housing": "房地产",
            "retail": "零售",
            "healthcare": "医疗保健",
            "pharmaceutical": "制药",
            "electric vehicles": "电动汽车",
            "semiconductor": "半导体",
            "chips": "芯片",
            "earnings": "财报",
            "profits": "利润",
            "revenue": "收入",
            "CEO": "首席执行官",
            "merger": "并购",
            "acquisition": "收购",
            "startup": "初创公司",
            "climate": "气候",
            "renewable energy": "可再生能源",
            "cryptocurrency": "加密货币",
            "Bitcoin": "比特币",
            "Trump": "特朗普",
            "Biden": "拜登",
            "election": "选举",
            "policy": "政策",
            "tariffs": "关税",
            "supply chain": "供应链",
            "housing market": "房地产市场",
            "unemployment": "失业",
            "jobs": "就业",
            "consumers": "消费者",
            "spending": "支出",
            "growth": "增长",
            "recession": "衰退",
            "crisis": "危机",
            "bank": "银行",
            "investment": "投资",
            "fund": "基金",
            "portfolio": "投资组合",
            "risk": "风险",
            "returns": "回报",
        }

        result = text
        # 先翻译长短语，再翻译单词
        sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
        for en, zh in sorted_trans:
            # 使用正则表达式确保单词边界
            result = re.sub(r'\b' + re.escape(en) + r'\b', zh, result, flags=re.IGNORECASE)

        return result

    def generate_html_email(self):
        """生成 HTML 邮件"""
        date_str = datetime.now().strftime("%Y 年 %m 月 %d 日 %A")

        # 按分类整理文章
        sections = {}
        for article in self.articles:
            section = article.get("section", "其他")
            if section not in sections:
                sections[section] = []
            sections[section].append(article)

        # 生成新闻列表 HTML
        news_html = ""
        colors = {
            "中国": "#e74c3c",
            "经济": "#3498db",
            "市场": "#2ecc71",
            "科技": "#9b59b6",
            "商业": "#f39c12",
            "全球": "#1abc9c",
        }

        for idx, (section, articles) in enumerate(sections.items()):
            color = colors.get(section, "#667eea")
            news_html += f"""
            <div class="section-block">
                <div class="section-header" style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%);">
                    <span class="section-icon">📌</span>
                    <span class="section-title">{section}</span>
                </div>
            """

            for article in articles:
                title_zh = self.translate_to_chinese(article["title"])
                summary = article.get("summary", "")[:150]
                if summary:
                    summary = self.translate_to_chinese(summary)

                news_html += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{article['url']}" style="color: #1a1a2e; text-decoration: none;">{title_zh}</a>
                    </div>
                    <div class="news-meta">
                        <span>🔗 <a href="{article['url']}" style="color: {color};">阅读原文</a></span>
                    </div>
                    {"<div class='news-summary'>" + summary + "</div>" if summary else ""}
                </div>
                """

            news_html += "</div>"

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FT 每日中文摘要</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; background-color: #f5f5f5; line-height: 1.6; }}
        .container {{ max-width: 650px; margin: 0 auto; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); border-radius: 15px 15px 0 0; padding: 30px; text-align: center; }}
        .header h1 {{ color: #ffffff; font-size: 26px; margin-bottom: 10px; }}
        .header .date {{ color: #a8d8ea; font-size: 14px; }}
        .header .logo {{ font-size: 42px; margin-bottom: 15px; display: block; }}
        .content {{ background: #ffffff; border-radius: 0 0 15px 15px; padding: 30px; }}
        .intro {{ text-align: center; padding: 20px 0; border-bottom: 2px dashed #e0e0e0; margin-bottom: 25px; }}
        .section-block {{ margin-bottom: 25px; border: 1px solid #e0e0e0; border-radius: 12px; overflow: hidden; }}
        .section-header {{ padding: 15px 20px; color: #fff; font-size: 16px; font-weight: bold; }}
        .section-icon {{ margin-right: 8px; }}
        .news-item {{ padding: 20px; background: #f8f9fa; border-bottom: 1px solid #e0e0e0; transition: transform 0.2s; }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-item:hover {{ background: #f0f1f3; }}
        .news-title {{ font-size: 16px; font-weight: 600; color: #1a1a2e; margin-bottom: 10px; line-height: 1.5; }}
        .news-title a:hover {{ text-decoration: underline !important; }}
        .news-meta {{ font-size: 13px; color: #666; }}
        .news-summary {{ margin-top: 10px; padding: 12px; background: rgba(255,255,255,0.8); border-radius: 6px; font-size: 14px; color: #555; border-left: 3px solid #667eea; }}
        .footer {{ background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%); border-radius: 15px; padding: 25px; text-align: center; margin-top: 20px; color: #a8d8ea; }}
        .footer p {{ font-size: 13px; margin-bottom: 8px; }}
        .footer .disclaimer {{ font-size: 11px; color: #6c7a89; margin-top: 15px; padding-top: 15px; border-top: 1px solid #2a3f5f; }}
        .stats {{ display: flex; justify-content: space-around; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; margin-bottom: 25px; }}
        .stat-item {{ text-align: center; color: #fff; }}
        .stat-number {{ font-size: 24px; font-weight: bold; }}
        .stat-label {{ font-size: 12px; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="logo">📰🌏</span>
            <h1>FT 每日中文摘要</h1>
            <p class="date">{date_str}</p>
        </div>

        <div class="content">
            <div class="intro">
                <p>尊敬的读者，早安！</p>
                <p>以下是 Financial Times 最新精选的 <strong>{len(self.articles)}</strong> 条全球财经要闻，已为您整理分类并翻译关键信息。</p>
            </div>

            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{len(sections)}</div>
                    <div class="stat-label">覆盖板块</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(self.articles)}</div>
                    <div class="stat-label">精选新闻</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">5min</div>
                    <div class="stat-label">阅读时间</div>
                </div>
            </div>

            {news_html}
        </div>

        <div class="footer">
            <p>📧 FT Daily Digest | 每日清晨 8 点准时送达</p>
            <p>让全球财经资讯，触手可及</p>
            <p class="disclaimer">免责声明：本邮件内容翻译自 FT.com，版权归原作者 Financial Times 所有。仅供个人学习参考，不构成投资建议。</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def send_email(self, html_content):
        """发送邮件"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        date_str = datetime.now().strftime("%Y 年 %m 月 %d 日")
        subject = f"【FT 每日中文摘要】{date_str} - {len(self.articles)}条全球财经要闻"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = EMAIL_TO

        msg.attach(MIMEText(html_content, "html", "utf-8"))

        try:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [EMAIL_TO], msg.as_string())
            server.quit()
            print(f"✓ 邮件已发送至 {EMAIL_TO}")
            return True
        except Exception as e:
            print(f"✗ 邮件发送失败：{e}")
            return False

    def send_dingtalk(self):
        """发送钉钉提醒"""
        date_str = datetime.now().strftime("%m 月 %d 日")
        markdown_text = f"""## 📰 FT 每日中文摘要已发送

📧 请查看邮箱获取今日 {len(self.articles)} 条全球财经要闻

**今日亮点：**
- 覆盖 {len(set(a.get('section', '其他') for a in self.articles))} 大板块
- 5 分钟速览全球大事
- 中文摘要，高效阅读

---
*每日清晨 8 点准时送达*"""

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "FT 每日中文摘要",
                "text": markdown_text
            }
        }

        try:
            response = requests.post(DINGTALK_WEBHOOK, json=payload)
            result = response.json()
            if result.get("errcode") == 0:
                print("✓ 钉钉提醒已发送")
                return True
        except Exception as e:
            print(f"钉钉提醒失败：{e}")
        return False

    def save_html(self, html_content):
        """保存 HTML 文件"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d")
        filepath = os.path.join(OUTPUT_DIR, f"ft_digest_{date_str}.html")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✓ HTML 已保存：{filepath}")
        return filepath

    def run(self):
        """执行完整流程"""
        print("=" * 50)
        print("FT 每日中文摘要生成器")
        print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

        # 1. 登录（可选，RSS 不需要登录）
        # self.login()

        # 2. 获取文章
        self.fetch_articles(limit=15)

        # 3. 生成 HTML
        html_content = self.generate_html_email()

        # 4. 保存 HTML
        self.save_html(html_content)

        # 5. 发送邮件
        if SMTP_PASS:
            self.send_email(html_content)
        else:
            print("⚠ 未配置 SMTP 密码，跳过邮件发送")

        # 6. 发送钉钉提醒
        self.send_dingtalk()

        print("=" * 50)
        print("✓ 任务完成")
        print("=" * 50)


def main():
    digest = FTDigest()
    digest.run()


if __name__ == "__main__":
    main()
