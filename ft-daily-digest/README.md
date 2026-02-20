# FT 每日中文摘要生成器

自动抓取 Financial Times 最新新闻，生成中文摘要并发送邮件。

## 功能特点

- 📰 每日自动抓取 FT 最新 15 条精选新闻
- 🇨🇳 关键信息中文翻译
- 📧 HTML 精美格式邮件
- ⏰ 每天早晨 8 点自动发送
- 📱 钉钉提醒通知

## 快速开始

### 1. 安装依赖

```bash
cd ft-daily-digest
pip3 install requests beautifulsoup4
```

### 2. 配置账号

复制配置模板并填写：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填写：

- **FT_COOKIE**（推荐）：浏览器登录 FT.com 后复制 Cookie
- **SMTP_PASS**：163 邮箱的 SMTP 授权码

### 3. 获取 FT Cookie（推荐方式）

由于 FT 使用复杂的 OAuth 登录，建议使用 Cookie 方式：

1. 在浏览器中访问 [FT.com](https://www.ft.com) 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 **Network** 标签
4. 刷新页面，点击任意请求
5. 在 **Request Headers** 中找到 `Cookie` 字段
6. 复制整个 Cookie 值，填入 `.env` 文件的 `FT_COOKIE` 字段

### 4. 测试运行

```bash
python3 ft_digest.py
```

### 5. 设置定时任务（每天 8:00）

```bash
python3 setup_cron.py
```

## 文件结构

```
ft-daily-digest/
├── ft_digest.py          # 主程序
├── setup_cron.py         # 定时任务设置脚本
├── .env.example          # 配置模板
├── .env                  # 实际配置（需创建）
├── requirements.txt      # Python 依赖
└── output/               # 生成的 HTML 文件
```

## 邮件预览

每日邮件包含：
- 头部横幅（日期、天气）
- 新闻统计（覆盖板块、文章数量）
- 分类新闻列表（中国、经济、市场、科技、商业、全球）
- 每条新闻包含：标题（中文）、原文链接、摘要
- 页脚信息

## 定时任务管理

### 查看已设置的任务
```bash
crontab -l
```

### 删除定时任务
```bash
python3 setup_cron.py --remove
```

### 手动执行一次
```bash
python3 ft_digest.py
```

## 故障排查

### Cookie 失效
FT Cookie 可能定期过期，如发现问题：
1. 重新登录 FT.com
2. 按上述步骤获取新 Cookie
3. 更新 `.env` 文件

### 邮件发送失败
检查：
- SMTP 授权码是否正确（不是登录密码）
- 163 邮箱是否开启 SMTP 服务

### 钉钉提醒未收到
检查网络连接，Webhook 配置是否正确

## 自定义配置

### 修改发送时间
编辑 `setup_cron.py` 中的时间设置

### 修改新闻数量
在 `ft_digest.py` 中修改 `fetch_articles(limit=15)` 的参数

### 修改收件邮箱
在 `.env` 文件中修改 `EMAIL_TO`

## 技术说明

- 数据源：FT RSS Feed（无需登录）+ 首页抓取
- 翻译：关键词替换 + 简单规则（可扩展接入翻译 API）
- 邮件：SMTP 协议（163 邮箱）
- 提醒：钉钉机器人 Webhook

## 注意事项

1. 本工具仅供个人学习使用
2. FT 内容版权归 Financial Times 所有
3. 请勿用于商业用途
4. 建议合理使用，避免频繁请求
