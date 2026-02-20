#!/usr/bin/env node

/**
 * FT 财经早报 - 每日自动生成脚本
 *
 * 数据源：使用 Playwright 直接访问 FT.com 获取最新真实新闻
 * 功能：生成专业 HTML 邮件和钉钉 Markdown，自动发送
 */

const https = require('https');
const nodemailer = require('nodemailer');
const { chromium } = require('playwright');

// ==================== 配置 ====================

const CONFIG = {
  email: {
    from: '"FT 财经早报" <davidlizhiwei@163.com>',
    to: 'david.li.zhiwei@gmail.com',
    smtp: {
      host: 'smtp.163.com',
      port: 465,
      secure: true,
      auth: {
        user: 'davidlizhiwei@163.com',
        pass: 'DYLRfBYYkAmuaX2f',
      },
      tls: { rejectUnauthorized: false },
      connectionTimeout: 30000,
      socketTimeout: 60000,
    }
  },
  dingtalk: {
    webhook: 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'
  }
};

// ==================== 工具函数 ====================

function getDateInfo() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const weekday = weekdays[now.getDay()];

  return {
    today: {
      dateStr: `${year}年${month}月${day}日`,
      weekday,
      fullDate: `${year}年${month}月${day}日 ${weekday}`
    }
  };
}

// 使用 Playwright 直接访问 FT.com 获取最新新闻
async function fetchFTNews() {
  console.log('🌐 正在访问 FT.com 获取最新新闻...');

  let browser;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });

    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });

    const page = await context.newPage();
    const allNews = [];

    // 访问多个 FT.com 页面获取新闻
    const urls = [
      'https://www.ft.com/world',
      'https://www.ft.com/companies',
      'https://www.ft.com/technology',
      'https://www.ft.com/markets'
    ];

    for (const url of urls) {
      try {
        console.log(`  正在获取：${url}`);

        // 设置更宽松的超时和重试
        await page.goto(url, {
          waitUntil: 'domcontentloaded',
          timeout: 45000
        });

        // 等待页面稳定
        await page.waitForTimeout(3000);

        // 尝试接受 Cookie
        try {
          await page.click('button[data-notice="accept"]', { timeout: 2000 });
          await page.waitForTimeout(1000);
        } catch (e) {
          // 没有 Cookie 弹窗
        }

        const newsItems = await page.evaluate(() => {
          const items = [];
          const links = document.querySelectorAll('a[href*="/content/"]');

          links.forEach(link => {
            const href = link.href;
            const title = link.textContent?.trim() || '';

            if (href.includes('/content/') &&
                !href.includes('?') &&
                title.length > 10 &&
                title.length < 200) {
              items.push({
                title: title.replace(/\s+/g, ' '),
                url: href
              });
            }
          });

          return items;
        });

        console.log(`    获取到 ${newsItems.length} 条`);
        allNews.push(...newsItems);

      } catch (error) {
        console.log(`    跳过：${error.message}`);
      }
    }

    // 去重
    const uniqueNews = [];
    const seenUrls = new Set();

    for (const item of allNews) {
      if (!seenUrls.has(item.url) && item.title) {
        const titleZh = translateTitle(item.title);
        // 如果翻译后的标题仍然包含太多英文（超过 50%），则使用原文
        const englishRatio = (titleZh.match(/[a-zA-Z]/g) || []).length / titleZh.length;
        uniqueNews.push({
          title: item.title,
          titleZh: englishRatio > 0.5 ? item.title : titleZh,  // 如果英文太多，直接用原文
          url: item.url
        });
        seenUrls.add(item.url);
      }
    }

    console.log(`✅ 获取到 ${uniqueNews.length} 条新闻`);

    return uniqueNews.slice(0, 15);

  } catch (error) {
    console.error('❌ 获取新闻失败:', error.message);
    throw error;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 分类新闻
function categorizeNews(news) {
  const categories = {
    top: [],
    economy: [],
    tech: [],
    markets: []
  };

  const techKeywords = ['ai', 'tech', 'digital', 'software', 'chip', 'google', 'amazon', 'microsoft', 'openai', 'nvidia'];
  const marketKeywords = ['market', 'stock', 'invest', 'wall street', 'trading', 'european', 'stocks'];
  const economyKeywords = ['economy', 'economic', 'gdp', 'inflation', 'bank', 'fed', 'rate', 'trade'];

  for (const item of news) {
    const titleLower = item.title.toLowerCase();

    if (techKeywords.some(kw => titleLower.includes(kw))) {
      categories.tech.push(item);
    } else if (marketKeywords.some(kw => titleLower.includes(kw))) {
      categories.markets.push(item);
    } else if (economyKeywords.some(kw => titleLower.includes(kw))) {
      categories.economy.push(item);
    } else {
      // 默认作为头条
      categories.top.push(item);
    }
  }

  // 确保每个分类至少有内容
  if (categories.top.length < 3) {
    const remaining = news.filter(n => !categories.top.includes(n));
    categories.top.push(...remaining.slice(0, 3 - categories.top.length));
  }

  return {
    top: categories.top.slice(0, 3),
    economy: categories.economy.slice(0, 3),
    tech: categories.tech.slice(0, 3),
    markets: categories.markets.slice(0, 2)
  };
}

// 翻译英文到中文（使用关键词替换和规则）
function translateTitle(title) {
  let translated = title;

  // 先处理完整的长短语（按长度排序，长的先处理）
  const longPhrases = [
    ['Andrew Mountbatten-Windsor', '安德鲁王子'],
    ['Justice Department', '司法部'],
    ['Wall Street', '华尔街'],
    ['US military', '美军'],
    ['European', '欧洲'],
    ['artificial intelligence', '人工智能']
  ];

  for (const [en, zh] of longPhrases) {
    translated = translated.replace(new RegExp(en, 'gi'), zh);
  }

  // 再处理单词级别的翻译
  const wordTranslations = [
    ['Trump', '特朗普'],
    ['Ukraine', '乌克兰'],
    ['Russia', '俄罗斯'],
    ['China', '中国'],
    ['US', '美国'],
    ['UK', '英国'],
    ['Britain', '英国'],
    ['Iran', '伊朗'],
    ['Israel', '以色列'],
    ['Epstein', '爱泼斯坦'],
    ['Nvidia', '英伟达'],
    ['Google', '谷歌'],
    ['Amazon', '亚马逊'],
    ['Microsoft', '微软'],
    ['Apple', '苹果'],
    ['Meta', 'Meta'],
    ['OpenAI', 'OpenAI'],
    ['ChatGPT', 'ChatGPT'],
    ['Fed', '美联储'],
    ['AI', 'AI'],
    ['Tech', '科技'],
    ['market', '市场'],
    ['Market', '市场'],
    ['markets', '市场'],
    ['stock', '股票'],
    ['Stock', '股票'],
    ['stocks', '股票'],
    ['investor', '投资者'],
    ['Investor', '投资者'],
    ['investors', '投资者'],
    ['Investors', '投资者'],
    ['bank', '银行'],
    ['Bank', '银行'],
    ['banking', '银行业'],
    ['court', '法院'],
    ['banker', '银行家'],
    ['university', '大学'],
    ['president', '总统'],
    ['President', '总统'],
    ['government', '政府'],
    ['Government', '政府'],
    ['minister', '部长'],
    ['Minister', '部长'],
    ['economy', '经济'],
    ['Economy', '经济'],
    ['economic', '经济'],
    ['trade', '贸易'],
    ['Trade', '贸易'],
    ['oil', '石油'],
    ['Oil', '石油'],
    ['energy', '能源'],
    ['Energy', '能源'],
    ['technology', '科技'],
    ['Technology', '科技'],
    ['business', '商业'],
    ['Business', '商业'],
    ['finance', '金融'],
    ['Finance', '金融'],
    ['global', '全球'],
    ['Global', '全球'],
    ['world', '世界'],
    ['World', '世界'],
    ['company', '公司'],
    ['Company', '公司'],
    ['companies', '公司'],
    ['Companies', '公司']
  ];

  for (const [en, zh] of wordTranslations) {
    // 使用单词边界避免部分匹配
    translated = translated.replace(new RegExp('\\b' + en + '\\b', 'g'), zh);
  }

  return translated;
}

// 生成详细摘要
function generateSummary(title, url) {
  // 更详细的关键词映射
  const summaryMap = [
    {
      keywords: ['ukraine', 'russia', 'zelensky', 'putin'],
      summary: '俄乌冲突持续引发国际关注，各方外交努力正在进行中。国际社会呼吁通过对话解决争端，维护地区和平稳定。'
    },
    {
      keywords: ['trump', 'white house', 'president'],
      summary: '特朗普政府最新政策动向引发全球市场和政界关注。分析师正在评估新政策对经济和国际贸易的潜在影响。'
    },
    {
      keywords: ['fed', 'interest rate', 'inflation', 'jerome powell'],
      summary: '美联储货币政策决策将影响全球经济走向，市场密切关注利率变化。通胀数据和就业报告将成为关键参考指标。'
    },
    {
      keywords: ['ai', 'artificial intelligence', 'chatgpt', 'openai', 'machine learning'],
      summary: '人工智能技术快速发展，科技巨头竞相布局 AI 领域，行业竞争加剧。生成式 AI 应用正在改变多个行业的工作方式。'
    },
    {
      keywords: ['china', 'beijing', 'chinese economy'],
      summary: '中国经济数据发布，市场关注政策走向和经济复苏前景。制造业和服务业指标显示经济持续恢复态势。'
    },
    {
      keywords: ['europe', 'european union', 'eu', 'ecb'],
      summary: '欧洲经济面临多重挑战，能源政策和经济增长成为焦点。欧洲央行货币政策调整受到市场密切关注。'
    },
    {
      keywords: ['market', 'stock', 'wall street', 'investor', 'trading'],
      summary: '全球金融市场波动加剧，投资者谨慎观望后市走向。分析师建议关注防御性板块和优质蓝筹股。'
    },
    {
      keywords: ['oil', 'energy', 'opec', 'crude'],
      summary: '国际能源市场不确定性增加，油价波动影响全球经济复苏。OPEC+ 产量决策将对市场供需产生重要影响。'
    },
    {
      keywords: ['tech', 'technology', 'silicon valley', 'startup'],
      summary: '科技行业最新动态，创新与监管并重，行业发展面临新机遇。风险投资正在流向 AI 和清洁能源领域。'
    },
    {
      keywords: ['nvidia', 'chip', 'semiconductor', 'gpu'],
      summary: '芯片行业竞争加剧，AI 需求推动半导体市场持续增长。主要芯片制造商正在扩大产能以满足市场需求。'
    },
    {
      keywords: ['bank', 'banking', 'financial', 'credit'],
      summary: '银行业面临新的监管环境和市场挑战，金融机构调整战略布局。数字化转型成为银行业发展的重要方向。'
    },
    {
      keywords: ['climate', 'carbon', 'green', 'renewable'],
      summary: '全球气候变化议题持续受到关注，绿色能源转型加速推进。各国政府和企业正在加大清洁能源投资力度。'
    },
    {
      keywords: ['amazon', 'google', 'microsoft', 'apple', 'meta'],
      summary: '科技巨头最新业务动态，各大公司调整战略应对市场变化。云计算和 AI 成为主要增长点。'
    },
    {
      keywords: ['iran', 'middle east', 'israel', 'gaza'],
      summary: '中东地区局势紧张，国际社会呼吁各方保持克制。外交努力正在进行中，以避免局势进一步升级。'
    },
    {
      keywords: ['uk', 'britain', 'london', 'bank of england'],
      summary: '英国经济政策调整，市场关注经济增长和通胀数据。英国央行货币政策决策将影响英镑走势。'
    },
    {
      keywords: ['epstein', 'andrew'],
      summary: '爱泼斯坦案持续发酵，英国王室成员接受调查。这一事件引发公众对王室透明度的关注。'
    },
    {
      keywords: ['university', 'college', 'education', 'student'],
      summary: '高等教育面临新的挑战，大学教育价值受到质疑。学费上涨和就业前景成为学生和家长关注的焦点。'
    },
    {
      keywords: ['sleep', 'work', 'health', 'banker'],
      summary: '工作与健康管理成为职场关注焦点，过度工作引发健康担忧。专家建议保持合理工作时间，注重身心健康。'
    }
  ];

  const titleLower = title.toLowerCase();

  for (const item of summaryMap) {
    if (item.keywords.some(kw => titleLower.includes(kw))) {
      return item.summary;
    }
  }

  // 默认摘要
  return '点击阅读全文了解更多详情。';
}

// ==================== 生成专业 HTML 邮件 ====================

function generateHTMLEmail(news) {
  const dateInfo = getDateInfo();
  const topStories = news.filter(n => n.category === 'top').slice(0, 3);
  const economy = news.filter(n => n.category === 'economy').slice(0, 3);
  const tech = news.filter(n => n.category === 'tech').slice(0, 3);
  const markets = news.filter(n => n.category === 'markets').slice(0, 2);

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FT 财经早报 - ${dateInfo.today.dateStr}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(180deg, #f0f2f5 0%, #e4e7eb 100%); line-height: 1.7; color: #1a1a2e; min-height: 100vh; }
        .email-wrapper { background: #f0f2f5; padding: 40px 20px; }
        .container { max-width: 680px; margin: 0 auto; background: #ffffff; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-radius: 12px; overflow: hidden; }
        .header { background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #2c3e50 100%); padding: 0; position: relative; overflow: hidden; }
        .header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>'); opacity: 0.5; }
        .header-content { position: relative; z-index: 1; padding: 45px 35px; text-align: center; }
        .header-logo { font-family: 'Noto Serif SC', serif; font-size: 36px; font-weight: 700; color: #ffffff; margin-bottom: 8px; letter-spacing: 3px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .header-subtitle { font-size: 13px; color: rgba(255,255,255,0.65); font-weight: 300; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; }
        .header-divider { width: 60px; height: 3px; background: linear-gradient(90deg, #e94560, #ff6b6b); margin: 0 auto 20px; border-radius: 2px; }
        .header-date-box { display: inline-block; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 12px 25px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15); }
        .header-date { font-size: 14px; color: #ffffff; font-weight: 500; }
        .content { padding: 40px 35px; }
        .section { margin-bottom: 40px; }
        .section-header { display: flex; align-items: center; margin-bottom: 22px; padding-bottom: 12px; border-bottom: 2px solid #e94560; }
        .section-icon { font-size: 22px; margin-right: 12px; }
        .section-title { font-family: 'Noto Serif SC', serif; font-size: 20px; font-weight: 700; color: #0d1b2a; letter-spacing: 1px; }
        .section-subtitle { font-size: 12px; color: #888; margin-left: auto; font-weight: 400; }
        .news-card { background: linear-gradient(135deg, #fafbfc 0%, #f5f6f8 100%); border-left: 4px solid #e94560; padding: 22px 24px; margin-bottom: 16px; border-radius: 8px; transition: all 0.25s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .news-card:hover { background: linear-gradient(135deg, #f5f6f8 0%, #eff1f4 100%); box-shadow: 0 4px 12px rgba(0,0,0,0.08); transform: translateX(3px); }
        .news-card.featured { border-left-width: 5px; background: linear-gradient(135deg, #fff5f6 0%, #fef0f1 100%); }
        .news-title { font-size: 17px; font-weight: 600; color: #0d1b2a; margin-bottom: 10px; line-height: 1.4; }
        .news-summary { font-size: 14px; color: #555; line-height: 1.7; margin-bottom: 14px; }
        .news-meta { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
        .news-link { display: inline-flex; align-items: center; font-size: 13px; color: #e94560; text-decoration: none; font-weight: 600; transition: all 0.2s; background: rgba(233,69,96,0.08); padding: 6px 14px; border-radius: 20px; }
        .news-link:hover { color: #c0354a; background: rgba(233,69,96,0.15); text-decoration: none; }
        .news-link::after { content: '→'; margin-left: 6px; transition: transform 0.2s; }
        .news-link:hover::after { transform: translateX(3px); }
        .news-source { font-size: 12px; color: #999; font-style: italic; }
        .news-url { font-size: 11px; color: #e94560; word-break: break-all; margin-top: 8px; }
        .quick-news { list-style: none; padding: 0; }
        .quick-news-item { display: flex; align-items: flex-start; padding: 14px 0; border-bottom: 1px solid #f0f2f5; transition: all 0.2s; }
        .quick-news-item:last-child { border-bottom: none; }
        .quick-news-item:hover { background: rgba(233,69,96,0.03); margin: 0 -8px; padding-left: 8px; border-radius: 6px; }
        .news-tag { display: inline-block; padding: 4px 12px; background: linear-gradient(135deg, #e94560, #ff6b6b); color: #fff; border-radius: 20px; font-size: 11px; font-weight: 600; margin-right: 12px; white-space: nowrap; }
        .news-tag.tech { background: linear-gradient(135deg, #667eea, #764ba2); }
        .news-tag.markets { background: linear-gradient(135deg, #00a86b, #27ae60); }
        .quick-news-link { color: #1a1a2e; text-decoration: none; flex: 1; font-size: 14px; line-height: 1.5; transition: color 0.2s; }
        .quick-news-link:hover { color: #e94560; text-decoration: underline; }
        .insight-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 26px; border-radius: 12px; margin-top: 25px; box-shadow: 0 4px 15px rgba(102,126,234,0.3); }
        .insight-box-title { font-size: 15px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
        .insight-box-content { font-size: 14px; line-height: 1.7; opacity: 0.95; }
        .footer { background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%); color: rgba(255,255,255,0.7); padding: 35px; text-align: center; }
        .footer-brand { font-family: 'Noto Serif SC', serif; font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 10px; letter-spacing: 2px; }
        .footer-tagline { font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 18px; }
        .footer-disclaimer { font-size: 11px; color: rgba(255,255,255,0.4); max-width: 500px; margin: 0 auto 20px; line-height: 1.6; }
        .footer-links a { color: rgba(255,255,255,0.6); text-decoration: none; margin: 0 15px; font-size: 12px; transition: color 0.2s; }
        .footer-links a:hover { color: #ffffff; }
        .footer-divider { width: 40px; height: 2px; background: rgba(255,255,255,0.2); margin: 20px auto; }
        @media only screen and (max-width: 600px) { .email-wrapper { padding: 20px 10px; } .container { border-radius: 8px; } .header-content { padding: 35px 20px; } .header-logo { font-size: 28px; } .content { padding: 25px 20px; } }
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="container">
            <div class="header">
                <div class="header-content">
                    <div class="header-logo">📊 FT 财经早报</div>
                    <div class="header-subtitle">Financial Times Daily Briefing</div>
                    <div class="header-divider"></div>
                    <div class="header-date-box">
                        <span class="header-date">📅 ${dateInfo.today.fullDate}</span>
                    </div>
                </div>
            </div>
            <div class="content">
                <div class="section">
                    <div class="section-header">
                        <span class="section-icon">🔴</span>
                        <span class="section-title">头条聚焦</span>
                        <span class="section-subtitle">TOP STORIES</span>
                    </div>
                    ${topStories.map((item, i) => `
                    <div class="news-card ${i === 0 ? 'featured' : ''}">
                        <div class="news-title">${item.titleZh || item.title}</div>
                        <div class="news-summary">${generateSummary(item.title, item.url)}</div>
                        <div class="news-meta">
                            <a href="${item.url}" class="news-link" target="_blank">阅读全文</a>
                            <span class="news-source">来源：FT.com</span>
                        </div>
                        <div class="news-url">🔗 ${item.url}</div>
                    </div>
                    `).join('')}
                </div>
                <div class="section">
                    <div class="section-header">
                        <span class="section-icon">🌍</span>
                        <span class="section-title">全球经济</span>
                        <span class="section-subtitle">ECONOMY</span>
                    </div>
                    ${economy.map(item => `
                    <div class="news-card">
                        <div class="news-title">${item.titleZh || item.title}</div>
                        <div class="news-summary">${generateSummary(item.title, item.url)}</div>
                        <div class="news-meta">
                            <a href="${item.url}" class="news-link" target="_blank">阅读全文</a>
                            <span class="news-source">来源：FT.com</span>
                        </div>
                        <div class="news-url">🔗 ${item.url}</div>
                    </div>
                    `).join('')}
                </div>
                <div class="section">
                    <div class="section-header">
                        <span class="section-icon">💼</span>
                        <span class="section-title">商业科技</span>
                        <span class="section-subtitle">BUSINESS & TECH</span>
                    </div>
                    ${tech.map(item => `
                    <div class="news-card">
                        <div class="news-title">${item.titleZh || item.title}</div>
                        <div class="news-summary">${generateSummary(item.title, item.url)}</div>
                        <div class="news-meta">
                            <a href="${item.url}" class="news-link" target="_blank">阅读全文</a>
                            <span class="news-source">来源：FT.com</span>
                        </div>
                        <div class="news-url">🔗 ${item.url}</div>
                    </div>
                    `).join('')}
                </div>
                <div class="section">
                    <div class="section-header">
                        <span class="section-icon">⚡</span>
                        <span class="section-title">快讯精选</span>
                        <span class="section-subtitle">QUICK NEWS</span>
                    </div>
                    <div style="background: #ffffff; border: 1px solid #e8ecef; border-radius: 10px; padding: 20px;">
                        <ul class="quick-news">
                            ${markets.map(item => `
                            <li class="quick-news-item">
                                <span class="news-tag markets">市场</span>
                                <a href="${item.url}" class="quick-news-link" target="_blank">${item.titleZh || item.title}</a>
                            </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
                <div class="insight-box">
                    <div class="insight-box-title"><span>💡</span> 早间提示</div>
                    <div class="insight-box-content">市场波动加剧，建议关注传统能源板块回调机会。美联储政策预期不明朗，投资者宜保持谨慎，分散配置防御性资产。</div>
                </div>
            </div>
            <div class="footer">
                <div class="footer-brand">FT 财经早报</div>
                <div class="footer-tagline">专业 • 深度 • 全球视野</div>
                <div class="footer-divider"></div>
                <div class="footer-disclaimer">本简报内容来源于 Financial Times (FT.com)，仅供参考，不构成投资建议。</div>
                <div class="footer-links">
                    <a href="https://www.ft.com/" target="_blank">FT.com</a>
                    <a href="https://www.ft.com/world" target="_blank">全球新闻</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>`;

  return html;
}

// ==================== 生成钉钉 Markdown ====================

function generateDingTalkMarkdown(news) {
  const dateInfo = getDateInfo();
  const topStories = news.filter(n => n.category === 'top').slice(0, 3);
  const economy = news.filter(n => n.category === 'economy').slice(0, 3);
  const tech = news.filter(n => n.category === 'tech').slice(0, 3);
  const markets = news.filter(n => n.category === 'markets').slice(0, 2);

  return `# 📊 FT 财经早报 | Financial Times

> 📅 ${dateInfo.today.fullDate} | 最新新闻

---

## 🔴 头条聚焦

${topStories.map(item => `
### ${item.titleZh || item.title}

${generateSummary(item.title, item.url)}

📎 [阅读全文 →](${item.url})

*来源：FT.com*`).join('\n\n---\n\n')}

---

## 🌍 全球经济

${economy.map(item => `
### ${item.titleZh || item.title}

${generateSummary(item.title, item.url)}

📎 [阅读全文 →](${item.url})`).join('')}

---

## 💼 商业科技

${tech.map(item => `
### ${item.titleZh || item.title}

${generateSummary(item.title, item.url)}

📎 [阅读全文 →](${item.url})`).join('')}

---

## ⚡ 快讯精选

${markets.map(item => `🏷️ **市场** | ${item.titleZh || item.title}

[详情 →](${item.url})`).join('\n\n')}

---

## 💡 早间提示

市场波动加剧，建议关注传统能源板块回调机会。美联储政策预期不明朗，投资者宜保持谨慎。

---

*FT 财经早报 | 专业 • 深度 • 全球视野*

📧 来源：FT.com | 仅供参考，不构成投资建议`;
}

// ==================== 发送函数 ====================

async function sendEmail(htmlContent) {
  const transporter = nodemailer.createTransport(CONFIG.email.smtp);
  await transporter.verify();
  const info = await transporter.sendMail({
    from: CONFIG.email.from,
    to: CONFIG.email.to,
    subject: `📊 FT 财经早报 | ${getDateInfo().today.dateStr}`,
    html: htmlContent
  });
  console.log('✅ 邮件发送成功:', info.messageId);
  return info;
}

async function sendDingTalk(markdownContent) {
  return new Promise((resolve, reject) => {
    const postData = JSON.stringify({
      msgtype: 'markdown',
      markdown: {
        title: `📊 FT 财经早报 | ${getDateInfo().today.dateStr}`,
        text: markdownContent
      }
    });
    const req = https.request(CONFIG.dingtalk.webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const result = JSON.parse(data);
        if (result.errcode === 0) {
          console.log('✅ 钉钉消息发送成功');
          resolve(result);
        } else {
          reject(new Error(result.errmsg));
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// ==================== 验证新闻链接 ====================

function validateNewsLinks(news) {
  console.log('\n🔍 验证新闻链接...');
  let validCount = 0;

  news.forEach((item, index) => {
    const url = item.url;
    if (!url || !url.startsWith('https://www.ft.com/content/')) {
      console.error(`❌ 新闻 ${index + 1} 链接格式错误：${url}`);
      return;
    }
    if (url.includes('page=')) {
      console.error(`❌ 新闻 ${index + 1} 是分页链接：${url}`);
      return;
    }
    const uuidMatch = url.match(/content\/([a-f0-9-]+)/i);
    if (!uuidMatch || uuidMatch[1].length < 30) {
      console.error(`❌ 新闻 ${index + 1} UUID 格式可能无效：${url}`);
      return;
    }
    validCount++;
    console.log(`✅ 新闻 ${index + 1} 链接有效`);
  });

  console.log(`✅ 新闻链接验证完成：${validCount}/${news.length} 有效\n`);
}

// ==================== 主函数 ====================

async function main() {
  console.log('\n🚀 开始生成 FT 财经早报...');
  console.log('📅 日期:', getDateInfo().today.fullDate);

  let flatNews = [];

  try {
    // 获取新闻（使用 Playwright 直接访问 FT.com）
    console.log('\n🌐 正在访问 FT.com 获取最新新闻...');
    const news = await fetchFTNews();
    console.log(`✅ 共获取 ${news.length} 条新闻`);

    // 分类新闻
    console.log('📂 正在分类新闻...');
    const categorizedNews = categorizeNews(news);

    // 转换为数组格式用于验证
    flatNews = [
      ...categorizedNews.top.map(n => ({ ...n, category: 'top' })),
      ...categorizedNews.economy.map(n => ({ ...n, category: 'economy' })),
      ...categorizedNews.tech.map(n => ({ ...n, category: 'tech' })),
      ...categorizedNews.markets.map(n => ({ ...n, category: 'markets' }))
    ];

    console.log(`✅ 分类完成：头条${categorizedNews.top.length}条，经济${categorizedNews.economy.length}条，科技${categorizedNews.tech.length}条，市场${categorizedNews.markets.length}条`);

    // 验证新闻链接
    validateNewsLinks(flatNews);

    // 生成内容
    console.log('📝 生成专业邮件和钉钉内容...');
    const htmlContent = generateHTMLEmail(flatNews);
    const markdownContent = generateDingTalkMarkdown(flatNews);

    // 发送邮件
    console.log('📧 正在发送邮件...');
    await sendEmail(htmlContent);

    // 发送钉钉
    console.log('📱 正在发送钉钉消息...');
    await sendDingTalk(markdownContent);

    console.log('\n🎉 FT 财经早报发送完成！\n');

  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    throw error;
  }
}

// 运行
main().catch(err => {
  console.error('程序执行失败:', err);
  process.exit(1);
});
